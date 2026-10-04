from pathlib import Path
import json,threading
class AOF:
 def __init__(self,path):self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True);self.lock=threading.Lock()
 def append(self,args):
  with self.lock,self.path.open("a",encoding="utf8") as f:f.write(json.dumps(args,separators=(",",":"))+"\n");f.flush()
 def records(self):
  if not self.path.exists():return []
  return [json.loads(x) for x in self.path.read_text().splitlines() if x]
 def rewrite(self,records):
  tmp=self.path.with_suffix(".tmp"); tmp.write_text("".join(json.dumps(x,separators=(",",":"))+"\n" for x in records)); tmp.replace(self.path)
