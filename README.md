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

## Useful Links

[LLM benchmarking fundamental concepts](https://developer.nvidia.com/blog/llm-benchmarking-fundamental-concepts/)

https://apxml.com/courses/quantized-llm-deployment/chapter-3-performance-evaluation-quantized-llms/measuring-inference-latency-throughput
