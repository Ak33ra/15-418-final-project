"""
Holds timing results for a single model.
"""

from dataclasses import dataclass
from typing import List
from data.single_model_config import SingleModelConfig


@dataclass
class SingleModelResult:
    avg_ms: float
    p50_ms: float
    p90_ms: float
    p95_ms: float
    p99_ms: float
    throughput_tokens_per_s: float
    latencies_ms: List[float]
    config: SingleModelConfig
