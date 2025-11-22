"""
Data class to pass around model configurations
"""

from dataclasses import dataclass, asdict

@dataclass
class SingleModelConfig: # W: Missing class docstring
    model_name: str
    batch_size: int
    seq_len: int
    num_warmup: int
    num_iters: int
    device: str
    out_dir: str
    tag: str
