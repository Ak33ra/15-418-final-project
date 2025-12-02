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
We have set up scripts to to set up environment variables and run mutliple models. We were struggling with issues of getting metrics from the GPU through Nsight, but this has been resolved. There was another issue of not having permissions to run Nvidia MPS, which we are resolving through using outside services to acquire GPUS. For running the tests we have written some code to create the random batched inputs for the input models. We have been able to run some tests on distilBERT, distalGPT2, and the mistral7b models and have collected some preliminary data for the different models. There is not too much analysis to be done yet, but some interesting data points are that the models run slower as the batch progresses and the last few inputs in the batch have substantially higher latency than the rest of the batch. We have also run combinations of models, although it was with multiple processes. This is not ideal since the context switching in the GPU results in extra overhead and results in slower run time, which is inaccurate for our needs. We have collected metrics for latency and throughput with varying batchsizes, but it is all oneshot test data so far. 

## Current Bottlenecks
All bottlenecks have been resolved.

## Updated Goals & Schedule
We will continue testing with the resources we have and try to collect as much data as possible. For our testing we are considering testing a more realistic workload with a random distribution overtime to more accurately represent how multiple models are run on a single GPU. This would allow for a far more realistic representation and useful data. With Nsight we hope to collect more metrics about how the GPU is being used and find possible bottlenecks or interesting patterns in the GPU usage. Since we are able to use MPS now, we will be rerunning all of mutimodal tests and collecting proper test data. We also plan on running tests on other models as well such as CV, for a more realistic comprehensive analysis of how the GPU usage is affected by varying models. We believe that we will be able to achieve all of the main goals that we have listed, since we have figured out the resources that we need to run our experiment and the majority of the remaining work should be data collection.

By Thursday:
 - Finish data pipeline for running tests and creating data files
 - Finish running tests for distilGPT2, distilBERT, mistral7b

By Saturday:
 - Finish running tests on any other models needed
 - Finish majority of analyis for earlier models

By Sunday:
 - Finish analysis
 - Start final report

By Monday:
 - finish

In terms of our nice to have goal, we are unlikely to create a schedular of any sort within the next week, so our goal is to just finish the data collection and analysis. 

