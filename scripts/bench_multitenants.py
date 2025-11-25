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
    ap.add_argument("--config", required = True)
    return ap.parse_args()

def main():
    args = parse_args()

if __name__ == "__main__":
    mp.set_start_method("spawn", force = True)
    main()
