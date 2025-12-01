---
layout: default
title: "Milestone"
---

<nav>
  [Home](index.html) |
  [Proposal](proposal.html) |
  [Milestone](milestone.html) |
  [Final](final.html)
</nav>

# Milestone Report

## Progress So Far
We have been able to run some tests on distilBERT, distalGPT2, and the mistral7b models. We have collected some preliminary test results running individual models on the GPUs and running pairs of models together. We have collected metrics for latency and throughput with varying batchsizes, but it is all oneshot. 

## Current Bottlenecks
We have a few different limitations in different aspects of the project. For the data collection, we are severely limited in the metrics that we are able to collect. We do not have permissions to collect the gpu utilization and such? For running the different models we are unable to use MPS also due to a lack of permissions. This is slightly concerning because this is a key tool for running models in parallel. This is an issue because we are currenlty creating multiple processes to run multiple models, but this creates a lot of overhead and doesn't necessarily run the models in parallel as desired. With these issues we are hardcapped in how deep our research is able to analyze the data and run time conditions of the models. We would like to use Nvidia Nsight to measure performance, but we also don't have permissions to run this. We are currently to acquire more GPU hours for PSC machines, but it is uncertain how long this process will take.


## Updated Goals & Schedule
We will continue testing with the resources we have and try to collect as much data as possible. For our testing we are considering testing a more realistic workload with a random distribution to more accurately represent how multiple models are run on a single GPU. This would allow for a far more realistic representation and useful data. We will also need to run more tests in order run proper statistical analysis of the model performance. We also would like to figure out how to run the models in parallel for a more realistic testing. We are unlikely to create a schedular of any sort within the next week, so our goal is to just finish the data collection and analysis. 

