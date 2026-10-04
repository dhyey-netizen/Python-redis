import threading,time
from collections import OrderedDict
class WrongType(Exception):pass
class Store:
 def __init__(self,max_memory=0,policy="allkeys-lru"):
  self.data={}; self.expiry={}; self.lru=OrderedDict(); self.lock=threading.RLock(); self.max_memory=max_memory; self.policy=policy; self.hits=0; self.misses=0; self.evictions=0
 def _expired(self,k):
  d=self.expiry.get(k)
  if d is not None and d<=time.time(): self._delete(k); return True
  return False
 def _delete(self,k): self.data.pop(k,None); self.expiry.pop(k,None); self.lru.pop(k,None)
 def _touch(self,k): self.lru.pop(k,None); self.lru[k]=time.monotonic()
 def get(self,k):
  with self.lock:
   if k not in self.data or self._expired(k): self.misses+=1; return None
   self.hits+=1; self._touch(k); return self.data[k]
 def exists(self,k): return int(self.get(k) is not None)
 def set(self,k,v,ttl=None):
  with self.lock:
   self.data[k]=v; self._touch(k); self.expiry.pop(k,None)
   if ttl is not None:self.expiry[k]=time.time()+ttl
   self._evict()
 def delete(self,*keys):
  with self.lock:
   n=0
   for k in keys:
    if k in self.data and not self._expired(k): n+=1; self._delete(k)
   return n
 def expire(self,k,seconds):
  with self.lock:
   if k not in self.data or self._expired(k):return 0
   self.expiry[k]=time.time()+seconds; return 1
 def ttl(self,k):
  with self.lock:
   if k not in self.data or self._expired(k):return -2
   if k not in self.expiry:return -1
   return max(0,int(self.expiry[k]-time.time()))
 def _typed(self,k,t,default):
  v=self.get(k)
  if v is None:
   v=default; self.data[k]=v; self._touch(k)
  if not isinstance(v,t):raise WrongType("WRONGTYPE operation against a key holding the wrong kind of value")
  return v
 def hset(self,k,field,value):
  with self.lock:
   h=self._typed(k,dict,{ }); created=int(field not in h); h[field]=value; self._touch(k); self._evict(); return created
 def hget(self,k,field):
  h=self.get(k); return None if h is None else h.get(field) if isinstance(h,dict) else (_ for _ in ()).throw(WrongType("WRONGTYPE"))
 def hgetall(self,k):
  h=self.get(k); return [] if h is None else [x for kv in h.items() for x in kv]
 def lpush(self,k,*vals):
  with self.lock:
   a=self._typed(k,list,[]); [a.insert(0,v) for v in vals]; self._touch(k); return len(a)
 def rpush(self,k,*vals):
  with self.lock:
   a=self._typed(k,list,[]); a.extend(vals); self._touch(k); return len(a)
 def lrange(self,k,start,end):
  a=self.get(k) or []; end=None if end==-1 else end+1; return a[start:end]
 def sadd(self,k,*vals):
  with self.lock:
   s=self._typed(k,set,set()); before=len(s); s.update(vals); self._touch(k); return len(s)-before
 def smembers(self,k):
  s=self.get(k) or set(); return list(s)
 def zadd(self,k,items):
  with self.lock:
   z=self._typed(k,dict,{}); added=0
   for score,member in items:
    if member not in z:added+=1
    z[member]=float(score)
   self._touch(k); return added
 def zrange(self,k,start,end,withscores=False):
  z=self.get(k) or {}; arr=sorted(z.items(),key=lambda x:(x[1],x[0])); end=None if end==-1 else end+1; arr=arr[start:end]; return [x for p in arr for x in (p if withscores else (p[0],))]
 def incrby(self,k,n):
  with self.lock:
   v=self.get(k); cur=0 if v is None else int(v); cur+=n; self.data[k]=str(cur).encode(); self._touch(k); self._evict(); return cur
 def dbsize(self):
  with self.lock:
   for k in list(self.data):self._expired(k)
   return len(self.data)
 def _evict(self):
  if not self.max_memory:return
  while self.memory_usage()>self.max_memory and self.data:
   k=next(iter(self.lru)) if "lru" in self.policy else next(iter(self.data)); self._delete(k); self.evictions+=1
 def memory_usage(self):
  import sys
  return sum(sys.getsizeof(k)+sys.getsizeof(v) for k,v in self.data.items())
