"""
Utility for writing common json events.
"""

import json
import time
from dataclasses import asdict
from data.single_model_config import SingleModelConfig
from data.single_model_result import SingleModelResult

def write_json_event(jsonl_file, event: dict):
    """
    Write the json object specified by event to jsonl_file.
    """
    if jsonl_file is None:
        return
    json.dump(event, jsonl_file)
    jsonl_file.write("\n")
    jsonl_file.flush()

def write_run_start(jsonl_file, config: SingleModelConfig):
    """
    Helper function to write a standard run start json object to jsonl_file.
    Requires jsonl_file to be None or a valid jsonl file.
    """
    write_json_event(jsonl_file,
        {
            "type": "run_start",
            "timestamp": time.time(),
            "model_name": config.model_name,
            "tag": config.tag,
            "device": config.device,
            "batch_size": config.batch_size,
            "seq_len": config.seq_len,
            "num_iters": config.num_iters,
            "num_warmup": config.num_warmup,
            "config": asdict(config),
        })

def write_run_end(jsonl_file, config: SingleModelConfig, result: SingleModelResult):
    """
    Helper function to write a standard run end json object to jsonl_file.
    Requires jsonl_file to be None or a valid jsonl file.
    """
    write_json_event(jsonl_file,
        {
            "type": "run_end",
            "timestamp": time.time(),
            "avg_ms": result.avg_ms,
            "p50_ms": result.p50_ms,
            "p90_ms": result.p90_ms,
            "p95_ms": result.p95_ms,
            "p99_ms": result.p99_ms,
            "throughput_tokens_per_s": result.throughput_tokens_per_s,
            "tokens_processed": config.batch_size * config.seq_len * config.num_iters,
            "num_iters": config.num_iters,
        })
