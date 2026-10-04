from pyredis.cluster.hashslots import slot,Ring
def test_slot():assert 0<=slot("user:1")<16384
def test_ring():assert Ring(["a","b"]).owner(0) in ("a","b")
