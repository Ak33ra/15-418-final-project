#!/usr/bin/env python

"""
Driver script to run multitenant experiments.

Uses multiprocess to spawn a child script for each tenant and coordinate them,
ensuring timed events are coordinated.

TODO: implement this whole file
- document desired multitenant yaml config format
- parse multitenant config file
- for each tenant, spawn a child process and use script that runs a single model
- implement barrier in single model script
- sync all children at the timed inference portion
- report metrics
- cleanup child processes
"""

import subprocess
import multiprocessing as mp
from dataclasses import dataclass
from pathlib import Path
import argparse
import os
import signal
import time
import yaml

from multitenant.single_model_runner import SingleModelConfig, run_single_model

def start_mps():
    """
    Starts MPS daemon.
    """
    print("[driver] Starting MPS.")

def stop_mps():
    """
    Stops MPS daemon.
    """
    print("[driver] Stopping MPS.")

def parse_args():
    """
    Create commandline argument parser and return parsed arguments.
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=str, required=True)
    ap.add_argument("--no-save", type=bool, default=False)
    ap.add_argument("--verbose", type=bool, default=False)
    return ap.parse_args()

def tenant_entry(cfg, no_save, barrier, verbose):
    """
    Wrapper to act as entry point for child processes into the single model runner.
    """
    run_single_model(cfg, no_save, barrier, verbose)

def main():
    """
    Benchmarks performance of models under multitenancy.

    Arguments:
        - Path to YAML experiment config file
        - (Optional) Boolean that specifies whether or not to write experiment results

    Prints performance summary for each model.

    By default, writes performance data to the out directory specified in the config file.
    """
    args = parse_args()
    with open(args.config, mode="r", encoding="utf-8") as f:
        experiment = yaml.safe_load(f)
    print("[driver] Opened config file.")

    # Parse config file
    experiment_name = experiment["experiment_name"]
    tenants = experiment["tenants"]
    mps_on = experiment.get("mps", False)
    #sleep_duration = int(experiment.get("duration", 120))

    # Make experiment directory
    data_dir = Path("data") / experiment_name
    data_dir.mkdir(parents = True, exist_ok = True)

    if mps_on:
        start_mps()

    barrier = mp.Barrier(len(tenants) + 1)

    processes = []
    try:
        for t in tenants:
            cfg = SingleModelConfig(
                model_name = t["model_name"],
                batch_size = t["batch_size"],
                seq_len = t["seq_len"],
                num_warmup=t.get("num_warmup", 10),
                num_iters = t.get("num_iters", 200),
                device = experiment.get("device", "cuda"),
                out_dir = str(data_dir / t["name"]),
                tag = t["name"]
            )
            p = mp.Process(target = tenant_entry, args=(cfg, args.no_save, barrier, args.verbose))
            p.start()
            processes.append(p)
        print("[driver] Waiting for warmups to finish...")
        barrier.wait() # Start barrier
        print("[driver] Models executing timed run.")
        barrier.wait() # End barrier
        print("[driver] Models compiling metrics.")
        barrier.wait()

    finally:
        print("[driver] Cleaning up and terminating child processes.")
        #for p in processes:
        #    if p.is_alive():
        #        p.terminate()
        for p in processes:
            p.join(timeout=5)
        if mps_on:
            stop_mps()
        print("[driver] Cleanup done.")

if __name__ == "__main__":
    mp.set_start_method("spawn", force = True)
    main()
