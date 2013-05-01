#!/usr/bin/env python
from present import Present

if __name__ == '__main__':
  # 80-bit fault injection
  p80 = Present(ks=80)
  m = 0x0000000000000000
  k = 0x00000000000000000000
  f = (31,0x00000000000000000000) # (fault round, fault value)
  c  = p80(m,k)
  cf = p80(m,k,f)
  print "c      = {:016x}".format(c)
  print "c'     = {:016x}".format(cf)
  print "c ^ c' = {:016x}".format(c ^ cf)
