import socket,threading
from pyredis.protocol.resp import encode,parse,RESPError
class ReplicationManager:
 def __init__(self):self.replicas=set();self.lock=threading.Lock();self.offset=0
 def register(self,conn):
  with self.lock:self.replicas.add(conn)
 def unregister(self,conn):
  with self.lock:self.replicas.discard(conn)
 def propagate(self,args):
  payload=encode([x.encode() if isinstance(x,str) else x for x in args]);self.offset+=len(payload)
  dead=[]
  with self.lock: peers=list(self.replicas)
  for c in peers:
   try:c.sendall(payload)
   except OSError:dead.append(c)
  for c in dead:self.unregister(c)
