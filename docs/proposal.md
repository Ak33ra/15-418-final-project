---
layout: default
title: "Project Proposal"
---

[Home](index.html) |
[Proposal](proposal.html) |
[Milestone](milestone.html) |
[Final](final.html)

# Project Proposal

## Title
**Authors:** Tianyou Zhang, Akira van de Groenendaal

**URL:** https://ak33ra.github.io/15-418-final-project/

## Summary

We are going to investigate the effects of multiple models inhabiting the same GPU. We will look at how performance metrics such as throughput, latency, slowdown, and load change as a function of number and size (batches, parameter count, etc) of models. We will explore how different resource intensive kernels perform on a shared GPU. Specifically we will investigate the interactions and potential conflicts between compute intensive and memory intensive programs. Another question to think about is which models benefit or suffer more from this setup?

## Background
Currently there are resources offered such as CUDA streams and NVIDIA's Multi-Process Service, which allows for concurrency on a single GPU, but do not offer any tools for the programmer for performance optimization. Multi tennacy on GPU's is a relevant issue with the age of AI and cloud compute, where a GPU is used for multiple kernel's out of necessity. There are a few papers that explore schedulers to optimiize performance, but they are a bit outdated.

##The Challenge
There is no correct solution for how to efficiently parallelize resources. It is difficult to predict how the hardware will scheudle the different kernels and specific limitations of the hardware, so ordering of kernels is challenging

## Goals and Deliverables
Plan to Achieve: Create a full benchmark for how different types of kernels interact and affect different performance metrics. 
Hope to Achieve: Create a scheduler to help efficiently queue kerenels and optimize hardware utilization.

## Platform
CUDA, C++, NVIDIA GeForce RTX 2080, add the psc machine 
Both are commonly used languages for writing parallel code. NVIDIA is a very widly used hardware.

## Schedule
