from pyredis.storage.store import Store
def test_strings():
 s=Store();s.set("x",b"1");assert s.get("x")==b"1";assert s.incrby("x",2)==3
def test_hash_list_set_sorted():
 s=Store();assert s.hset("h","a",b"1")==1;assert s.hget("h","a")==b"1";assert s.lpush("l",b"a",b"b")==2;assert s.sadd("s",b"x")==1;assert s.zadd("z",[(2,"a"),(1,"b")])==2
def test_ttl():
 s=Store();s.set("x",b"1",.01);import time;time.sleep(.02);assert s.get("x") is None
