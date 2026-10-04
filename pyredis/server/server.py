import socket,threading
from pyredis.config import Config
from pyredis.storage.store import Store,WrongType
from pyredis.protocol.resp import parse,encode,error,RESPError
from pyredis.persistence.aof import AOF
from pyredis.persistence.snapshot import Snapshot
from pyredis.monitoring.metrics import Metrics
from pyredis.replication.replica import ReplicationManager
class RedisServer:
 def __init__(self,config=None):
  self.config=config or Config(); d=self.config.data_dir; self.store=Store(self.config.max_memory,self.config.maxmemory_policy); self.aof=AOF(d+"/appendonly.aof");self.snapshot=Snapshot(d+"/dump.rdb");self.metrics=Metrics();self.repl=ReplicationManager();self.running=False;self.sock=None;self.clients=set();self.lock=threading.Lock()
  self._recover()
 def _recover(self):
  self.snapshot.load(self.store)
  for args in self.aof.records():
   try:self.execute(args,persist=False)
   except Exception:pass
 def execute(self,parts,persist=True):
  a=[x.decode() if isinstance(x,bytes) else str(x) for x in parts];cmd=a[0].upper();self.metrics.command()
  r=None
  if cmd=="PING":r="PONG"
  elif cmd=="GET":r=self.store.get(a[1])
  elif cmd=="SET":
   ttl=None
   if len(a)==5 and a[3].upper()=="EX":ttl=int(a[4])
   self.store.set(a[1],a[2].encode(),ttl);r="OK"
  elif cmd=="DEL":r=self.store.delete(*a[1:])
  elif cmd=="EXISTS":r=self.store.exists(a[1])
  elif cmd=="EXPIRE":r=self.store.expire(a[1],int(a[2]))
  elif cmd=="TTL":r=self.store.ttl(a[1])
  elif cmd=="INCR":r=self.store.incrby(a[1],1)
  elif cmd=="DECR":r=self.store.incrby(a[1],-1)
  elif cmd=="DBSIZE":r=self.store.dbsize()
  elif cmd=="HSET":r=self.store.hset(a[1],a[2],a[3])
  elif cmd=="HGET":r=self.store.hget(a[1],a[2])
  elif cmd=="HGETALL":r=self.store.hgetall(a[1])
  elif cmd=="LPUSH":r=self.store.lpush(a[1],*[x.encode() for x in a[2:]])
  elif cmd=="RPUSH":r=self.store.rpush(a[1],*[x.encode() for x in a[2:]])
  elif cmd=="LRANGE":r=self.store.lrange(a[1],int(a[2]),int(a[3]))
  elif cmd=="SADD":r=self.store.sadd(a[1],*[x.encode() for x in a[2:]])
  elif cmd=="SMEMBERS":r=self.store.smembers(a[1])
  elif cmd=="ZADD":r=self.store.zadd(a[1],[(a[i],a[i+1]) for i in range(2,len(a),2)])
  elif cmd=="ZRANGE":r=self.store.zrange(a[1],int(a[2]),int(a[3]),len(a)>4 and a[4].upper()=="WITHSCORES")
  elif cmd=="INFO":r="\r\n".join(f"{k}:{v}" for k,v in self.metrics.info(self.store).items())
  elif cmd=="SAVE":self.snapshot.save(self.store);r="OK"
  elif cmd=="BGREWRITEAOF":self.aof.rewrite(self._aof_state());r="OK"
  else:raise ValueError(f"unknown command {cmd}")
  if persist and cmd in {"SET","DEL","EXPIRE","INCR","DECR","HSET","LPUSH","RPUSH","SADD","ZADD"} and self.config.aof:
   self.aof.append(a);self.repl.propagate(a)
  return r
 def _aof_state(self):return []
 def client(self,conn):
  buf=b""
  with conn:
   while self.running:
    chunk=conn.recv(65536)
    if not chunk:break
    buf+=chunk
    while buf:
     try:req,pos=parse(buf)
     except RESPError:break
     buf=buf[pos:]
     try:out=encode(self.execute(req))
     except Exception as e:self.metrics.error();out=error(str(e))
     conn.sendall(out)
 def run(self):
  self.running=True
  with socket.socket() as s:
   self.sock=s;s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);s.bind((self.config.host,self.config.port));s.listen(256);print(f"PyRedis {self.config.node_id} listening on {self.config.host}:{self.config.port}")
   try:
    while self.running:
     c,a=s.accept();threading.Thread(target=self.client,args=(c,),daemon=True).start()
   except KeyboardInterrupt:pass
