from pyredis.protocol.resp import encode,parse
def test_resp():
 x=encode([b"GET",b"x"]);assert parse(x)[0]==[b"GET",b"x"]
