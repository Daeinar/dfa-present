#!/usr/bin/env python
from present import Present

def test_present():

  p80 = Present(ks=80)

  # 80-bit test vectors
  v80 = [
     (0x0000000000000000,0x00000000000000000000,0x5579c1387b228445),
     (0x0000000000000000,0xffffffffffffffffffff,0xe72c46c0f5945049),
     (0xffffffffffffffff,0x00000000000000000000,0xa112ffc72f68417b),
     (0xffffffffffffffff,0xffffffffffffffffffff,0x3333dcd3213210d2),
     (0x0123456789abcdef,0x0123456789abcdef0123,0xf8dd50531d973bde)
  ]

  for i in xrange(len(v80)):
    v = v80[i]
    assert p80(v[0],v[1]) == v[2]
    #print "{:016x}".format(p80(v[0],v[1])) 

  print "All  80-bit tests passed."


  p128 = Present(ks=128)

  # 128-bit test vectors
  v128 = [
     (0x0000000000000000,0x00000000000000000000000000000000,0x96db702a2e6900af),
     (0x0000000000000000,0xffffffffffffffffffffffffffffffff,0x13238c710272a5d8),
     (0xffffffffffffffff,0x00000000000000000000000000000000,0x3c6019e5e5edd563),
     (0xffffffffffffffff,0xffffffffffffffffffffffffffffffff,0x628d9fbd4218e5b4),
     (0x0123456789abcdef,0x0123456789abcdef0123456789abcdef,0x0e9d28685e671dd6)
  ]

  for i in xrange(len(v128)):
    v = v128[i]
    assert p128(v[0],v[1]) == v[2]
    #print "{:016x}".format(p128(v[0],v[1])) 

  print "All 128-bit tests passed."

if __name__ == '__main__':
  test_present()

