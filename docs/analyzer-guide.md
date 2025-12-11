---
layout: default
title: "Analysis Notebook Guide"
---

[Home](index.html) |
[Proposal](proposal.html) |
[Milestone](milestone.html) |
[Final](final.html) | 
[Analysis Notebook Guide](analyzer-guide.html)

# Data Analyzer Guide

This guide explains how to use the `DataAnalyzer` class and related functions to load and analyze performance data from multi-tenant GPU experiments.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Loading Data](#loading-data)
3. [Computing Statistics](#computing-statistics)
4. [Visualization](#visualization)
5. [Multi-Tenant Analysis](#multi-tenant-analysis)
6. [Fairness & Statistical Significance](#fairness--statistical-significance)
7. [Resource Hogging Detection](#resource-hogging-detection)
8. [Complete Example Workflow](#complete-example-workflow)

## Quick Start

The analyzer is implemented in the Jupyter notebook at [notebooks/analysis.ipynb](../notebooks/analysis.ipynb). To get started:

```python
# Run the notebook to load the DataAnalyzer class
# Then create an instance
analyzer = DataAnalyzer()

# Load data
analyzer.load_files('path/to/data.csv', dataset_name='experiment1')

# Compute statistics
stats = analyzer.compute_statistics(column='latency_ms')

# Visualize
analyzer.plot_distributions(column='latency_ms')
```

## Loading Data

### Basic File Loading

The `DataAnalyzer` class supports CSV, JSON, and JSONL file formats.

#### Load a Single File

```python
analyzer = DataAnalyzer()
analyzer.load_files('data/experiment/events.jsonl', dataset_name='experiment1')
```

#### Load Multiple Files

```python
analyzer.load_files(
    ['data/exp1/events.jsonl', 'data/exp2/events.jsonl'],
    label_extractor=lambda path: path.parent.name
)
```

#### Load Files Matching a Pattern

```python
# Load all JSONL files under a directory tree
analyzer.load_pattern(
    '../data/3_distilgpt2_mps/**/events.jsonl',
    label_extractor=lambda name: name.parent.name
)
```

### Label Extractors

Label extractors help organize datasets by extracting meaningful names from file paths. Two helper functions are provided:

```python
# Extract batch size from filename like 'model_b8_L128_latencies_ms.csv'
analyzer.load_pattern('*.csv', label_extractor=extract_batch_size)

# Extract model name and batch size
analyzer.load_pattern('*.csv', label_extractor=extract_model_and_batch)
```

### Supported File Formats

- **CSV**: Standard comma-separated values
- **JSON**: Single JSON object or array
- **JSONL**: Newline-delimited JSON (one object per line)

## Computing Statistics

### Basic Statistics

```python
# Compute statistics for all loaded datasets
stats = analyzer.compute_statistics(
    column='latency_ms',
    percentiles=[50, 90, 95, 99]
)
print(stats.to_string())
```

Returns a DataFrame with:
- `count`: Number of samples
- `mean`: Average value
- `std`: Standard deviation
- `min` / `max`: Minimum and maximum values
- `p50`, `p90`, `p95`, `p99`: Percentiles

### Compute Statistics for Specific Datasets

```python
stats = analyzer.compute_statistics(
    column='latency_ms',
    datasets=['experiment1', 'experiment2']
)
```

### Adding Throughput Column

Convert latency measurements to throughput (tokens/second):

```python
analyzer.add_throughput_column(
    latency_column='latency_ms',
    batch_size=8,
    seq_len=128,
    throughput_column='throughput'
)
```

Formula: `throughput = (batch_size * seq_len) / (latency_ms / 1000)`

## Visualization

### Distribution Plots

#### Histogram and KDE (Kernel Density Estimation)

```python
analyzer.plot_distributions(
    column='latency_ms',
    plot_type='both',  # Options: 'hist', 'kde', 'both'
    bins=50
)
```

#### Histogram Only

```python
analyzer.plot_distributions(
    column='latency_ms',
    plot_type='hist',
    bins=30
)
```

### Box Plots

Compare distributions across datasets:

```python
analyzer.plot_boxplot(column='latency_ms')
```

### Metric Comparison Bar Charts

Compare multiple metrics for a single dataset:

```python
analyzer.plot_comparison(
    dataset='experiment1',
    column='latency_ms',
    metrics=['mean', 'median', 'p95', 'p99', 'max']
)
```

### Export Summary to CSV

```python
analyzer.export_summary(
    column='latency_ms',
    output_file='results/summary.csv',
    percentiles=[50, 90, 95, 99]
)
```

## Multi-Tenant Analysis

### Computing Total Throughput

For multi-tenant scenarios where multiple models share one GPU:

```python
total_throughput_df = compute_total_throughput(
    analyzer,
    latency_column='latency_ms',
    batch_size=8,
    seq_len=128,
    datasets=None  # None = all datasets
)
```

This function:
- Computes throughput for each model
- Sums throughputs across all models per iteration
- Returns a DataFrame with total throughput statistics

### Comparing Multi-Tenant vs Single-Tenant

```python
# Load multi-tenant data
multi_analyzer = DataAnalyzer()
multi_analyzer.load_pattern('../data/3_distilgpt2_mps/**/events.jsonl',
                             label_extractor=lambda name: name.parent.name)

# Load single-tenant baseline data
single_analyzer = DataAnalyzer()
single_analyzer.load_files('../data/solo_distilgpt2_b8_128/distilgpt2/events.jsonl',
                            dataset_name='solo_distilgpt2')

# Compare
comparison = compare_multi_vs_single_tenant(
    multi_tenant_analyzer=multi_analyzer,
    single_tenant_analyzer=single_analyzer,
    batch_size=8,
    seq_len=128
)
```

Returns:
- Mean throughput for multi-tenant and single-tenant
- Improvement percentage
- Visualizations comparing distributions and means

## Fairness & Statistical Significance

### Fairness Metrics

Analyze whether GPU resources are shared fairly among models:

```python
fairness = compute_fairness_metrics(
    analyzer,
    column='latency_ms',
    datasets=None  # None = all datasets
)
```

**Key Metrics:**
- **Coefficient of Variation (CV)**: `std/mean`
  - < 0.05: Excellent fairness
  - < 0.10: Good fairness
  - < 0.20: Moderate fairness
  - ≥ 0.20: Poor fairness
- **Gini Coefficient**: 0 (perfect equality) to 1 (perfect inequality)
- **Max/Min Ratio**: How many times slower is the slowest vs fastest model
- **Max Deviation %**: Worst-case deviation from average

### Statistical Significance Testing

Test whether performance differences are statistically significant:

```python
sig_results = test_statistical_significance(
    analyzer,
    column='latency_ms',
    datasets=None,
    alpha=0.05  # Significance level
)
```

**Tests Performed:**
1. **Levene's Test**: Tests for equal variances (homoscedasticity)
2. **One-way ANOVA** (or Kruskal-Wallis if variances unequal): Tests if any groups differ
3. **Pairwise t-tests with Bonferroni correction**: Identifies which specific pairs differ

**Returns:**
- Test statistics and p-values
- Significant pairs of models
- Effect sizes (Cohen's d)

### Combined Visualization

```python
visualize_fairness_and_significance(
    analyzer,
    column='latency_ms',
    datasets=None,
    fairness_metrics=None,  # Auto-computed if None
    sig_results=None,       # Auto-computed if None
    figsize=(16, 10)
)
```

Creates a comprehensive 6-panel visualization showing:
1. Mean ± standard deviation comparison
2. Box plot distributions
3. Within-model variability (coefficient of variation)
4. Fairness metrics summary
5. Pairwise p-values heatmap
6. Statistical test summary

## Resource Hogging Detection

Detect if one model is monopolizing GPU resources at the expense of others.

### Normalized (Baseline-Aware) Detection

This method accounts for different model architectures having different baseline speeds:

```python
hogging = detect_resource_hogging_normalized(
    analyzer=multi_analyzer,        # Multi-tenant data
    baseline_analyzer=single_analyzer,  # Solo baseline data
    column='latency_ms',
    hogging_threshold=0.15  # 15% difference threshold
)
```

**How It Works:**
1. Compares each model's slowdown from its solo baseline
2. Detects models with abnormal slowdown patterns
3. Identifies both hogging (getting priority) and starvation (being starved)

**Returns:**
- `hogging_models`: Models getting priority access
- `starved_models`: Models being starved of resources
- `fair_models`: Models with fair resource allocation
- Visualizations showing baseline vs multi-tenant performance

## Complete Example Workflow

Here's a complete example analyzing a 3-model multi-tenant experiment:

```python
# 1. Create analyzer and load data
triple_analyzer = DataAnalyzer()
triple_analyzer.load_pattern(
    '../data/3_distilgpt2_mps/**/events.jsonl',
    label_extractor=lambda name: name.parent.name
)

# 2. View basic statistics
stats = triple_analyzer.compute_statistics(
    column='latency_ms',
    percentiles=[50, 90, 95, 99]
)
print(stats.to_string())

# 3. Visualize distributions
triple_analyzer.plot_distributions(column='latency_ms', plot_type='both')

# 4. Add throughput column
triple_analyzer.add_throughput_column(
    latency_column='latency_ms',
    batch_size=8,
    seq_len=128
)

# 5. Analyze fairness
fairness = compute_fairness_metrics(triple_analyzer, column='latency_ms')

# 6. Test statistical significance
sig_results = test_statistical_significance(triple_analyzer, column='latency_ms')

# 7. Create comprehensive visualization
visualize_fairness_and_significance(triple_analyzer, column='latency_ms')

# 8. Load baseline data for comparison
single_analyzer = DataAnalyzer()
single_analyzer.load_files(
    '../data/solo_distilgpt2_b8_128/distilgpt2/events.jsonl',
    dataset_name='solo_distilgpt2'
)

# 9. Compare multi-tenant vs single-tenant
comparison = compare_multi_vs_single_tenant(
    triple_analyzer,
    single_analyzer,
    batch_size=8,
    seq_len=128
)

# 10. Detect resource hogging
hogging = detect_resource_hogging_normalized(
    analyzer=triple_analyzer,
    baseline_analyzer=single_analyzer,
    column='latency_ms'
)
```

## Utility Functions

### List Loaded Datasets

```python
datasets = analyzer.list_datasets()
print(datasets)  # ['experiment1', 'experiment2', ...]
```

### Get Raw Data

```python
df = analyzer.get_data('experiment1')
print(df.head())
```

### Get Available Columns

```python
columns = analyzer.get_columns('experiment1')
print(columns)  # ['iter', 'latency_ms', 'timestamp', ...]
```

### Clear All Data

```python
analyzer.clear()
```

## Tips and Best Practices

1. **Always load baseline data**: For meaningful multi-tenant analysis, load single-tenant baseline data for comparison.

2. **Use consistent parameters**: When comparing experiments, ensure batch_size and seq_len are consistent.

3. **Check for missing data**: The analyzer will warn about missing columns or files, but always verify your data loaded correctly.

4. **Use descriptive labels**: Label extractors help organize data - use meaningful names for easier analysis.

5. **Combine visualizations**: Use multiple visualization types (histograms, box plots, bar charts) to understand different aspects of the data.

6. **Statistical significance matters**: Just because numbers differ doesn't mean they're statistically significant - always run significance tests.

7. **Fairness vs performance**: A "fair" system might have lower total throughput - consider both metrics.

## Common Data Paths

Based on the example in the notebook, common data patterns:

- Multi-tenant data: `../data/{N}_distilgpt2_mps/**/events.jsonl`
- Single-tenant data: `../data/solo_distilgpt2_b8_128/distilgpt2/events.jsonl`
- Pair experiments: `../data/pair_distilgpt2/**/events.jsonl`

## Expected Data Format

The analyzer expects data files (CSV, JSON, or JSONL) with at least:
- `latency_ms`: Latency measurements in milliseconds
- `iter` (optional): Iteration number for tracking

Additional columns are preserved and accessible for custom analysis.
