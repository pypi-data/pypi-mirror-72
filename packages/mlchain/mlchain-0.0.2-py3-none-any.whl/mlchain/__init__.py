# Parameters of MLchain
__version__ = "0.0.2"
host = "https://www.api.mlchain.ml"
web_host = host
api_address = host
model_id = None
from os import environ

environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'
from mlchain.base.log import logger
from .config import mlconfig
try:
    import torch
    torch.set_num_thread(1)
except Exception as e:
    pass
