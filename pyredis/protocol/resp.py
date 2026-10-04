class RESPError(Exception): pass

def _line(buf,pos):
    e=buf.find(b"\r\n",pos)
    if e<0: raise RESPError("incomplete")
    return buf[pos:e],e+2

def parse(buf,pos=0):
    if pos>=len(buf): raise RESPError("incomplete")
    p=buf[pos:pos+1]; line,pos=_line(buf,pos+1)
    if p==b"*":
        n=int(line); out=[]
        for _ in range(n): v,pos=parse(buf,pos); out.append(v)
        return out,pos
    if p==b"$":
        n=int(line)
        if n<0:return None,pos
        if len(buf)<pos+n+2:raise RESPError("incomplete")
        if buf[pos+n:pos+n+2]!=b"\r\n":raise RESPError("bad bulk terminator")
        return buf[pos:pos+n],pos+n+2
    if p==b"+":return line.decode(),pos
    if p==b":":return int(line),pos
    if p==b"-":raise RESPError(line.decode(errors="replace"))
    raise RESPError("unknown RESP type")

def encode(v):
    if v is None:return b"$-1\r\n"
    if isinstance(v,bool):return b":"+str(int(v)).encode()+b"\r\n"
    if isinstance(v,int):return b":"+str(v).encode()+b"\r\n"
    if isinstance(v,bytes):return b"$"+str(len(v)).encode()+b"\r\n"+v+b"\r\n"
    if isinstance(v,str):return encode(v.encode())
    if isinstance(v,(list,tuple)):return b"*"+str(len(v)).encode()+b"\r\n"+b"".join(encode(x) for x in v)
    if isinstance(v,dict):return encode([x for kv in v.items() for x in kv])
    raise TypeError(type(v))

def error(msg):return b"-ERR "+str(msg).encode()+b"\r\n"
