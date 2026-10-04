# Failure and Recovery

- Client disconnect: worker exits without affecting other clients.
- Malformed RESP: request is rejected; connection remains isolated.
- AOF restart: records are replayed after snapshot recovery.
- Snapshot write: temporary file + atomic rename prevents partial target files.
- Replica disconnect: replication manager removes failed sockets.
- Memory pressure: configured eviction policy removes LRU keys.

Known hardening work: fsync policies, checksums, replication handshake, partial resync, cluster membership, authentication/TLS, ACLs, and crash-injection testing.
