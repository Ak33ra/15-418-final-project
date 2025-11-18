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

We are going to investigate the effects of multiple models inhabiting the same GPU. We will look at how performance metrics such as throughput, latency, slowdown, and load change as a function of number and size (batches, parameter count, etc) of models. Another question to think about is which models benefit or suffer more from this setup?

## Background
With the age of AI and cloud computing it is very common for multiple models to be running on the same GPU. With edge computing resources can be limited, so multiple models are forced to run on the same GPU. Ideally the resources would be efficiently utilized, but this is still an developing research area for how to efficiently concurrently run models on the same device. There are tools such as CUDA Streams and MPS, which allow programmers to have concurrent kernels, but it provides little benefit for the programmer to efficiently run multiple kernels.


## The Challenge
This is a current research problem for how to efficiently utilize all of the resources on a GPU while maintaining performance metrics. We do not have an experience in optimizing machine learning model performance on GPUs. <br>
We want comprehensive metrics and analysis that is able to provide beneficial data for the research field, which is multi-dimensional due to the many factors that can affect model performance.

## Goals and Deliverables
Plan to Achieve: Create a full benchmark for how different sized models on different GPUs perform and find possible areas of improvement.
There are multiple combinations of different models and GPUs that we want to analyze to see how performance metrics are impacted. 
For each combination we will obtain the following metrics: latency, throughput, tail latency, slowdown, fairness, SM utliziation, TensorCore utilization, 
bandwidth utilization. <br>
The combinations of models we will be testing on are small model, big model, small + big models.
For these models we will also vary the the models that are arithmeticlly intensive and models that are bandwidth limited. <br>
We hope to find patterns in the different bottlenecks of the varying combinations of models, and provide key insights for how to improve performance. <br />
Hope to Achieve: Create a scheduler or theoretical schedular for the models on different GPUs to optimize GPU utilization and performance.
This would be creating a wrapper of some sort for kernel launches and inference handling, which would allow for more optimized usage of the GPU.

## Platform
Tools: C++, Python, NVIDIA GeForce RTX 2080, NVIDIA V100, Other research GPUs, Nsight Systems. <br>
Models: GPT-2, BERT, LLAMA, DeepSeek <br>
Most models can be run through C++ and Python, which have many libraries for gathering metris. We will will also be using a variety of different GPUs in order to explore how mult-tenancy can impact GPUs with varying power. We also want to run varying sized models to see how parameter count and model size affect multi-tenancy results.

## Schedule
Week of Nov 17th: Explore research in this area and understand how to run and benchmark the different models Understand how to use MPS and running multiple models with batch requests. <br>
Week of Nov 24th: Obtain different benchmarks for the models <br>
Week of Dec 1st: Analyze the data and find possible areas of optimization. Possibly create scheduler or scheduling ideas. <br>