# PyRedis — Production-Oriented Redis-Compatible Data Store

PyRedis is a systems-engineering project written in Python. It implements a Redis-inspired in-memory data store and explores the architecture behind production caching infrastructure.

## Implemented
- TCP server with concurrent clients
- RESP-style protocol
- Strings, hashes, lists, sets, sorted sets
- TTL and lazy expiration
- Configurable memory limit and LRU-style eviction
- AOF command persistence
- Atomic snapshot/recovery foundation
- Primary-to-replica propagation foundation
- 16,384-slot consistent key routing foundation
- Metrics and INFO command
- Unit tests, benchmarks, Docker and architecture/failure docs

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
PYTHONPATH=. python -m pyredis
```

In another shell:
```bash
PYTHONPATH=. python -m pyredis.cli
```

Docker:
```bash
docker compose up --build
```

## Benchmark
```bash
PYTHONPATH=. python benchmarks/benchmark_store.py
```

## Roadmap / hardening
Authentication/TLS, RESP3 completeness, production fsync policy, replication handshake/partial resync, real cluster membership/failover, ACLs, load tests, fuzzing, crash injection, and benchmark comparison against Redis.

