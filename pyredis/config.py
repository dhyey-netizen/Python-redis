from dataclasses import dataclass
import os
@dataclass(frozen=True)
class Config:
    host:str=os.getenv("PYREDIS_HOST","0.0.0.0")
    port:int=int(os.getenv("PYREDIS_PORT","6379"))
    data_dir:str=os.getenv("PYREDIS_DATA_DIR","./data")
    max_memory:int=int(os.getenv("PYREDIS_MAX_MEMORY","0"))
    maxmemory_policy:str=os.getenv("PYREDIS_MAXMEMORY_POLICY","allkeys-lru")
    aof:bool=os.getenv("PYREDIS_AOF","yes").lower() in ("1","yes","true")
    snapshot_interval:int=int(os.getenv("PYREDIS_SNAPSHOT_INTERVAL","60"))
    node_id:str=os.getenv("PYREDIS_NODE_ID","node-1")
