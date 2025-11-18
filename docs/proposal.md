---
layout: default
title: "Multi Model Tenancy Performance on GPUs"
---

[Home](index.html) |
[Proposal](proposal.html) |
[Milestone](milestone.html) |
[Final](final.html)

# Project Proposal

## Title
**Authors:** Akira van de Groenendaal, Tianyou Zhang

**URL:** https://ak33ra.github.io/15-418-final-project/

## Summary

We will experimentally evaluate how multiple deep learning models running concurrently on a single GPU impact each other’s performance. Using real NVIDIA GPUs and inference workloads, we will measure throughput, latency, slowdown, fairness, and GPU utilization when different models—varying in size and compute vs. bandwidth bottlenecks—share the device simultaneously. Our goal is to characterize bottlenecks and identify patterns that inform better GPU multi-tenancy strategies.

## Background

Modern AI systems frequently need co-locate multiple models on the same GPU to improve device utilization, or to make better use to limited computing resources. Ideally, models can run independently and provide speedups directly proportional to the number of models we can fit on a GPU. However, GPU kernels from separate models often interfere with each other, competing for shared resources. While tools like CUDA Streams and MPS further enable concurrency, they offer only basic resource partitioning, and programmers also have very little (or no) control over the exact allocation of memory, SMs, and work schedules.

Different models also stress different resources. Some might be compute heavy, while others are bandwidth heavy. In addition, different types of models are dominated by different types of operations.
- Large transformer LLMs are primarily compute-bound, saturating Tensor Cores and SMs.
- Encoder models like BERT may exhibit mixed compute/memory behavior.
- Lightweight CNNs or MLPs may be bandwidth-limited and launch many small kernels.

When these workloads execute together, we'd expect more complex contention patterns to emerge:
- Small models may suffer when large kernels monopolize SMs.
- Compute-bound and memory-bound models may interfere asymmetrically.
- Batch size interacts with stream concurrency in non-obvious ways.

Studying this problem is interesting, and characterizing these problems in specific ways can help us better understand how to effectively use a fixed amount of compute, as well as suggest future directions for improvement.

## The Challenge
One significant challenge is the open-endedness of this project- there isn't a concrete algorithm to implement and benchmark vs a known sequential version. Additionally, the nature of this work is new to us, and part of the learning will be figuring out efficient pipelines for running experiments, collecting, and plotting data in order to extract meaningful conclusions. We'll also have to deepen our understanding of GPUs and the models we'll be running. In particular, we need to learn about how various types of models actually run on a GPU, and how changing various parameters affects the compute/ memory patterns.

We want comprehensive metrics and analysis that is able to provide beneficial data for the research field, which is multi-dimensional due to the many factors that can affect model performance.

## Goals and Deliverables
Plan to Achieve
- Create a full benchmark for how different sized models on different GPUs perform and find possible areas of improvement.
- There are multiple combinations of different models and GPUs that we want to analyze to see how performance metrics are impacted.
- For each combination we will obtain the following metrics: latency, throughput, tail latency, slowdown, fairness, SM utliziation, TensorCore utilization, bandwidth utilization.
- The combinations of models we will be testing on are small model, big model, small + big models.
- For these models we will also vary the the models that are arithmeticlly intensive and models that are bandwidth limited.
- We hope to find patterns in the different bottlenecks of the varying combinations of models, and provide key insights for how to improve performance. Specifically, we want to find patterns for how the GPU usage and model performance can be optimized in terms of efficiency and latency, which are key metrics for real world metrics. Some questions that we hope to find answers for what are key bottlenecks that programmers need to watch out for, and what are posssible research areas for improving performance.

Hope to Achieve:
- Create a scheduler or theoretical scheduler for the models on different GPUs to optimize GPU utilization and performance that controls launch order or batch grouping. This would be creating a wrapper of some sort for kernel launches and inference handling, which would allow for more optimized usage of the GPU. The scheduler would be optimized for multi model inference on a single GPU. See how this compares to default CUDA.
- Predictive modeling via a queueing-based model to estimate interference

## Platform
Tools: C++, Python, NVIDIA GeForce RTX 2080, NVIDIA V100, Other research GPUs like A100, Nsight Systems.

Models: GPT-2, BERT, LLAMA, DeepSeek

Most models can be run through C++ and Python, which have many libraries for gathering metris. We will will also be using a variety of different GPUs in order to explore how mult-tenancy can impact GPUs with varying power. We also want to run varying sized models to see how parameter count and model size affect multi-tenancy results.

Using GPUs is the natural choice since most models in deployment run on GPUs and utilize resources like Tensor Cores and SMs. Additionally, Nvidia's tooling provides good visibility into kernel-level interactions.

## Schedule
Week of Nov 17th: Explore research in this area and understand how to run and benchmark the different models Understand how to use MPS and running multiple models with batch requests. Set up infrastructure/ environment for running multiple models concurrently, controlling batch sizes, timing and logging.

Week of Nov 24th: Obtain different benchmarks for the models. Start with isolated base lines (model running alone), before investigating different combinations and variables. Collect Nsight data (if available).

Week of Dec 1st: Analyze the data and find possible areas of optimization. Possibly create scheduler or scheduling ideas. Write up insights and patterns.
