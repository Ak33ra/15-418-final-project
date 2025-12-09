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

## Setup on Rented GPUs
1. `chmod +x scripts/*`
2. Run `./scripts/pip_setup.sh` to install necessary packages
3. Perform desired benchmarks

## Running benchmarks
Run `./scripts/bench_all_multitenants.sh` to run all configs in `configs/multitenant/`.

Similarly, run `./scripts/bench_all_solo.sh` to generate solo baselines.

Data is saved in the `data` directory, with the format described below.

It should be noted that NVIDIA MPS is used for the multitenant experiments by default. This requires root privileges to run. You can disable MPS by setting `mps: false` in the desired config file.

To run the Llama experiments, an authorized Hugging Face token is needed, with approval from Meta. You can request access via Hugging Face here: https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct.

## Using Nsight
Install the correct distribution for your platform to a user-writable directory (works if you don't have root privileges). If on Linux, you can use `/scripts/nsys_setup.sh` to install from a `.deb` file. Add nsys to PATH as described in the output.

Use `nsys profile` or the `/scripts/profile_*.sh` scripts to examine how each experiment runs on your GPU. Outputs are in `/out/nsys/` by default.

## Pushing from other devices
Use personal access token

## Useful Links

[LLM benchmarking fundamental concepts](https://developer.nvidia.com/blog/llm-benchmarking-fundamental-concepts/)

https://apxml.com/courses/quantized-llm-deployment/chapter-3-performance-evaluation-quantized-llms/measuring-inference-latency-throughput

## Config Format

Store experiment parameters (e.g. warmup, experiment name, number of iterations) in YAML config files for easier running and reproductibility.

See `configs/solo_template.yaml` for the expected format when benchmarking an individual model.

See `configs/multitenant_template.yaml` for the expected format of a multitenant experiment.

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

## TODO

Comprehensive analysis, write final report.
