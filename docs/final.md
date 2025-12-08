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

Another aspect to consider is the size of the model, or the number of parameters for each model, which affects the arithmetic intensity. In order to get a broad dataset, we used models of a few different sizes. 

Another important aspect to consider is how to run multiple models on the same GPU. There is the simple method of just using multiple processes and making multiple calls to the GPU. However, this results in heavy overhead for context switching. There are a few different strategies such as Multi-instance GPU by Nvidia, which allows users to partition the resources of the GPU. However, not all GPU's have this resource and is a fairly new tool. Also, it is limited to 7 partitions, which is smaller than what we wanted to test. There is also the decision between CUDA streams and Multi-Process Service(MPS). MPS is available on fewer devices, but it is widely used in datacenters or other multi-process/application situations. Therefore, we decided that performing tests with MPS would be the best concurrency tool to use.

---

## Approach
We are renting an A100 GPU in order to perform our tests. We were planning on testing on other GPUs, but we were limited in the GPUs that we could access, so we limited it to just the A100. Furthermore, the only extra experimentation we would get is if different GPU architectures affected the concurrency results of the multi-tenancy. However, MPS is a software level scheduler, so the results should be similar across devices. 

As explained above we need different models with encoder and decoder architectures, and various parameter sizes. For our decoder models we decided on distilGPT2, llama.3.2, and mistral7b. The models are increasing in size. For the encoders we picked BERT and deBERTa. With deBERTa being the larger model. Our criteria for choosing the models, were varying model sizes which were also able to fit on GPU, which had a memory limit of 40GB. We also needed the models small enough so that we could multiple models on the same GPU. We were not too worried about the specific layers and model architecture other than whether or not the models were encoders or decoders because we did not understand it too that level. Additionally, we were mainly choosing models based off of the parameter count, which should correlate with the amount of computation needed. 

Explain how we run our tests with the timing and nsight

Explain the test cases we created the solo models, pairs as baseline, and the different model combinations for experimentation of how multitenancy scales and performs in a variety of cases


---

## Results
Explain the results that we see and if it is expected, unexpected, and what are some possible design principles and such that should be implemented.
There is a reduciton in throughput and increase in latency as we add more models onto the GPU.

---

## Artifacts

