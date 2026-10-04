import socket,sys
from pyredis.protocol.resp import encode,parse
def main():
 host=sys.argv[1] if len(sys.argv)>1 else "127.0.0.1";port=int(sys.argv[2]) if len(sys.argv)>2 else 6379
 s=socket.create_connection((host,port));print("pyredis-cli connected; Ctrl-D to exit")
 while True:
  try:line=input("> ")
  except EOFError:break
  args=line.split();s.sendall(encode(args));data=s.recv(65536)
  try:r,_=parse(data);print(r)
  except Exception:print(data)
if __name__=="__main__":main()
