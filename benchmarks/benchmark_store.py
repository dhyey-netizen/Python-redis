import time
from pyredis.storage.store import Store
s=Store();n=200000;t=time.perf_counter()
for i in range(n):s.set(str(i),b"value")
print("SET ops/sec",round(n/(time.perf_counter()-t)))
t=time.perf_counter()
for i in range(n):s.get(str(i))
print("GET ops/sec",round(n/(time.perf_counter()-t)))
