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

from mps_multitenant.runners.single_model_runner import SingleModelConfig, run_single_model

def start_mps():
    pass

def stop_mps():
    pass

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=str, required=True)
    ap.add_argument("--no-save", type=bool, default=False)
    return ap.parse_args()

def tenant_entry(cfg, no_save, barrier):
    """
    Wrapper to act as entry point for child processes into the single model runner.
    """
    run_single_model(cfg, no_save, barrier)

def main():
    args = parse_args()

    tenants = []
    processes = []

    barrier = mp.Barrier(len(tenants) + 1)

    try:
        for t in tenants:
            cfg = SingleModelConfig(
                model_name = t["model"],
                batch_size = t["batch_size"],
                seq_len = t["seq_len"],
                num_warmup=t.get("num_warmup", 10),
                num_iters = t.get("num_iters", 200),
                device = t.get("device", "cuda"),
                out_dir = str(exp_dir / t["name"]),
                tag = t["name"]
            )
            p = mp.Process(target = tenant_entry, args=(cfg, False, barrier))
            p.start()
            processes.append(p)
    finally:
        # Cleanup
        print("[driver] terminating tenants")
        for p in processes:
            if p.is_alive():
                p.terminate()
        for p in processes:
            p.join(timeout=5)
        # also stop mps
        print("[driver] cleanup done")

if __name__ == "__main__":
    mp.set_start_method("spawn", force = True)
    main()
