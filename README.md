# 15-418-final-project

https://ak33ra.github.io/15-418-final-project/proposal.html

## Setup

1. Clone the repo
2. Set up the environment with conda: `conda env create -f environment-yaml`
3. Activate with `conda activate mps-multitenant`
4. Treat `src` as a package by running `pip install -e .` in the root directory with the conda env active
5. From anywhere, you can use `from multitenant import _` to access source code and run scripts/analysis

### Alternatives

Conda takes up a large amount of disk space and is impractical for AFS, so consider [micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html).

Install it and run `micromamba env create -f environment.yml`.

Alternatively to conda, you can install the env using `pip install -r requirements.txt`.

## Running on Rented GPUs
1. `chmod +x scripts/*`
2. Run `./scripts/pip_setup.sh` to install necessary packages
3. Perform desired benchmarks

## Pushing from other devices
Use personal access token

## Useful Links

[LLM benchmarking fundamental concepts](https://developer.nvidia.com/blog/llm-benchmarking-fundamental-concepts/)

https://apxml.com/courses/quantized-llm-deployment/chapter-3-performance-evaluation-quantized-llms/measuring-inference-latency-throughput

## Config Format

Store experiment parameters (e.g. warmup, experiment name, number of iterations) in YAML config files for easier running and reproductibility.

See `configs/solo/solo_template.yaml` for the expected format when benchmarking an individual model.

See `configs/multitenant/multitenant_template.yaml` for the expected format of a multitenant experiment.

## Data Format

Each experiment should create a new directory for organization. An explicit out_dir should be provided if you don't want to override old results of an identical experiment.

For each model in the experiment, we create a jsonl file in the experiment directory (TODO). This will track events per model and report its performance metrics.

The YAML config used should be copied into the experiment data folder.

## Data Metrics
- Latency
- Throughput per model in tokens/sec
- GPU throughput: sum of model throughputs divided by max completion time (tokens/sec)
- GPU utilization
- time to first token
- time per output token

## Data Analysis

In the data analysis script, the config file or experiment folder should be passed in. From there, the script should be able to access the appropriate directory and jsonl files in order to make plots, and output them in the `plots` directory.
