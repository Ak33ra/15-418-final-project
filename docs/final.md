---
layout: default
title: "Final"
---

<nav>
  [Home](index.html) |
  [Proposal](proposal.html) |
  [Milestone](milestone.html) |
  [Final](final.html)
</nav>

# Final Report

## Summary
The goal of our project was to examine how multi tenancy on GPUs affected model performance, and if there were any exploitable patterns.

---

## Background
Large language models have become a crucial part of society for several industries and even in everyday life. There are many cases where balancing between performance and saving on costs is vital to a business, such as datacenters which are forced to balance between QoS agreements and costs. There are also scenarios of edge computing where the resources are limited, so multiple models have to be run on the same GPU. Our aim for this project is to gather data for how multi tenancy on a single GPU affects key metrics, so that users are able to optimize how they run models on their GPUs. 

There are many different types of machine learning models, and for LLMs there are 2 main stream architectures: encoders and decoders. In doing so we aim to get a more accurate representation of running various types of models on GPUs for edge computing. Another reason is that encoders and decoders stress different parts of the GPU resources, so we hope to see if there are optimal ways of organizing various models depending on the resources that limit them. 

Overview for Encoders and Decoders
Encoders are bidirectional and compute all tokens at the same time. Being bidirectional means that each attention layer sees all tokens before and after the token it is being applied to. Also, the tokens are generated in parallel, which means that the models have low arithmetic intensity. Furthermore, encoders are normally used for smaller sequences, so the compute requirements are smaller. Since the models are extremely fast during the compute portion and the memory reads and writes become a larger portion of the job time. Therfore, encoders become memory bandwidth bound.

Decoders have an encoding step first, which is memory intensive, but very quick. The main chunk of computation is in the second decode phase where tokens are generated sequentially because each token depends on the previous token. Since the tokens are generated sequentially, results the decoder models become compute bound.

As explained above encoders and decoders have different resource demands, so there is potential in different combinations of the models becoming more efficient than other pairings. 

---

## Approach
We tested how running multiple models affected key metrics: latency, throughput, and GPU utilization.


---

## Results
There is a reduciton in throughput and increase in latency as we add more models onto the GPU.

---

## Artifacts

