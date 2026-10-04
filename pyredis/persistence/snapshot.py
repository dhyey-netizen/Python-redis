from pathlib import Path
import pickle,tempfile,os
class Snapshot:
 def __init__(self,path):self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True)
 def save(self,store):
  fd,tmp=tempfile.mkstemp(dir=self.path.parent); os.close(fd)
  with open(tmp,"wb") as f:pickle.dump((store.data,store.expiry),f,pickle.HIGHEST_PROTOCOL)
  os.replace(tmp,self.path)
 def load(self,store):
  if not self.path.exists():return False
  with self.path.open("rb") as f:data,expiry=pickle.load(f)
  with store.lock:store.data=data;store.expiry=expiry;store.lru.clear();[store._touch(k) for k in data]
  return True
