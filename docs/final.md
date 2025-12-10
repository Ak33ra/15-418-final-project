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

# Experimentation Setup
For our testing suite we needed a way to consistently test for latency, throughput, and GPU utilitzation times. Our throughput can be calculated with latency, so we essentially only needed a timing mechanism. The timing tool we decided on was a timer on the GPU. We decided that this was the core metric that we needed because we expected majority of the latency to come from running the LLM. Also, we have a warmup sequence, so kernel is already launched and our batch and sequences are not large anough to stress the CPU to GPU bandwidth. Other then timings we also wanted to look at the GPU utilization and how the jobs were being allocated resources. For this we decided to usse Nvidia Nsight, which allows us to collect data on which kernel is running. Nsight slows down the GPU a lot because it constantly prods the GPU for information, we decided to first test for latency and then GPU utilization. 

#Test Cases
We needed a variety of test cases to gather enough data to understand how the GPU reacts and performs under different constraints. We developed our test cases as follows. We first need to establish a baseline performance for latency, so we ran each of the models individually. Then we run each of the models as pairs to also check that the GPU resource sharing and scaling is as expected.

Then we needed to create test cases for our main question of whether the resource sharing is fair and efficient, and what the limitations were. To do this we came up with the following set of categories to test.

We first ran a baseline test of each model so that we have a relative metric to compare to for when we combine various models.

Then we created tests for each of the following subgroups of encoders only, decoders only, and a combination of both. By doing so we are able to compare how different architectures interact and whether or not there is an impact for performance. 

For the encoder and decoder only groups our goal was to see if there was any biasing of how resources were shared between processes that had the same resource limitations. We were interested in how the scheduler would allocate resources and the fairness along with efficieny limitations. Since the indpendent variable in this case was the model size, we tried different combinations of smaller and larger models to see how they interacted and the resulting performance impacts.

For the combination of encoder and decoder experiments our goal was to see how processes that had different resource bottlenecks would interact. Since encoders were generally limited by memory bandwidth and decoders were limited by compute resources, we were interested in meshing these models together and seeing if they would minimize performance hits. Another variable we were interested in was if how the number of processes along with the different architectures would improve or hurt performance. For example, we were curious if many encoders and a few decoders would have better results than only having decoders.

We also ran our models with FP16 accuracy so that all of the models would be able to fit on the GPU. We could've made some of the smaller models run with FP32, but we decided on FP16 for consistency. It should also have minimal impact on the majority of the analysis of the results. 

Based on the criteria and ideas listed above we tried to have a comprehensive coverage of tests to have.

We also needed to figure out how many iterations and the batch size for each of our experiments. We decided on a constant workload for simplicty and simpler comparisons. The workload was not a factor that we were interested in comparing, nor did we believe it to be a influential for our analsyis. Therefore, we decided a constant batch size of 8 and sequence of 128 tokens in length. We also ran it for 100 total iterations sequentially, so that we would have a large data sample for how the scheduler handles many requests. 

Before we collect any data, we ran 10 warm up iterations so that the cache and GPU frequency are warmed up, so that the GPU starts at a constant perforamnce level.

For our batch requests, we used a torch.synchronize call, so that each process only sends 1 request at a time to the GPU. This way we are replicating how multiple proceses would process one request at a time. This also simplifiess the timing of our program. It is possible that there is extra overhead when multiple jobs are queued, but our experiments with multiple models, should help account for these scenarios. 


---

## Results
We begin with analysis of the distil gpt2 models first. The solo baseline model had an average run time 


---

## Artifacts

