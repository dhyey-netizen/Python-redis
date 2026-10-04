# PyRedis Architecture

```
Clients -> TCP -> RESP -> Command Engine -> Thread-safe Store
                                  |             |
                                  |             +-- TTL / LRU / types
                                  +-- AOF -> recovery
                                  +-- replication stream

Snapshot -> atomic dump -> startup recovery
Cluster -> SHA1 hash slot (16384) -> node ownership
```

## Design goals
Correctness first, explicit failure modes, deterministic tests, measurable performance, and incremental distributed-system features.
