---
layout: default
title: "Milestone"
---

[Home](index.html) |
[Proposal](proposal.html) |
[Milestone](milestone.html) |
[Final](final.html)

# Milestone Report

## Progress So Far
We have set up scripts to to set up environment variables and run mutliple models. We were struggling with issues of getting metrics from the GPU through Nsight, but this has been resolved. There was another issue of not having permissions to run Nvidia MPS, which we are resolving through using outside services to acquire GPUS. For running the tests we have written some code to create the random batched inputs for the input models. We have been able to run some tests on distilBERT, distalGPT2, and the mistral7b models and have collected some preliminary data for the different models. We have also run combinations of models, although it was with multiple processes. This is not ideal since the context switching in the GPU results in extra overhead and results in slower run time, which is inaccurate for our needs. We have collected metrics for latency and throughput with varying batchsizes, but it is all oneshot test data so far. 

## Current Bottlenecks
All bottlenecks have been resolved.

## Updated Goals & Schedule
We will continue testing with the resources we have and try to collect as much data as possible. For our testing we are considering testing a more realistic workload with a random distribution overtime to more accurately represent how multiple models are run on a single GPU. This would allow for a far more realistic representation and useful data. With Nsight we hope to collect more metrics about how the GPU is being used and find and possible bottlenecks or interesting patterns in the GPu usage. Since we are able to use MPS now, we will be rerunning all of mutimodal tests and collecting proper test data. In terms of our extra goal, we are unlikely to create a schedular of any sort within the next week, so our goal is to just finish the data collection and analysis. 

