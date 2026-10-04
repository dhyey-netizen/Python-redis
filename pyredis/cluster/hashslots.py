import hashlib
SLOTS=16384
def slot(key):
 k=key.encode() if isinstance(key,str) else key
 a=k.find(b"{"); b=k.find(b"}",a+1) if a>=0 else -1
 if a>=0 and b>a+1:k=k[a+1:b]
 return int.from_bytes(hashlib.sha1(k).digest()[:4],"big")%SLOTS
class Ring:
 def __init__(self,nodes=None):self.nodes=list(nodes or [])
 def owner(self,s):
  if not self.nodes:return None
  return self.nodes[s%len(self.nodes)]
