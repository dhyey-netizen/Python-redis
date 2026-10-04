# 30-minute interview walkthrough

1. Why build Redis? In-memory systems expose networking, protocols, concurrency, persistence and distributed systems in one project.
2. Request path: TCP -> RESP parser -> command dispatch -> store -> RESP response.
3. Concurrency: worker per client, shared store protected by RLock.
4. TTL: expiration timestamps checked lazily.
5. Eviction: LRU ordering with memory accounting.
6. Persistence: AOF command log plus atomic snapshots.
7. Transactions: roadmap for MULTI/EXEC/WATCH; atomic command execution is already lock-protected.
8. Replication: primary propagates mutation frames to registered replicas; production hardening requires handshake and offsets.
9. Sharding: 16384 logical slots allow deterministic ownership.
10. Observability: command/error counters, hits/misses, memory and evictions.
11. Tradeoffs: Python accelerates implementation but sacrifices raw throughput; correctness and architecture are the learning goals.
