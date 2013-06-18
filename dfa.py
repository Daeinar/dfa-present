#!/usr/bin/env python
from present import Present
import random

#
# Simulates fault injection on the PRESENT key schedule.
#

def sample(keysize=80,r=30,l=None,N=100):
    present = Present(ks=keysize)

    infile  = open( 'input.txt', 'w')
    outfile = open('output.txt', 'w')

    for i in xrange(N):
        m = random.randint(0, (1 << 64) - 1)
        k = random.randint(0, (1 << keysize ) - 1)
        if l == None:
            s = random.randint(0,keysize/4 - 1)
        else:
            s = l
        v = random.randint(1,15)
        f = (r,v << s*4)
        c = present(m,k)
        cf = present(m,k,f)

        if keysize == 80:
            infile.write("{:064b} {:080b} {:04b} {:02d} {:032b}\n".format(m,k,0,s,1 << r))
            infile.write("{:064b} {:080b} {:04b} {:02d} {:032b}\n".format(m,k,v,s,1 << r))
        else:
            infile.write("{:064b} {:0128b} {:04b} {:02d} {:032b}\n".format(m,k,0,s,1 << r))
            infile.write("{:064b} {:0128b} {:04b} {:02d} {:032b}\n".format(m,k,v,s,1 << r))

        outfile.write("{:064b}\n".format(c))
        outfile.write("{:064b}\n".format(cf))


if __name__ == '__main__':

    # sample 100 random correct and faulty PRESENT-80 encryptions with random (nibble) fault values.
    # default fault config: round = 30, fault location (nibble based) = random
    sample()

    # sample 1000 random correct and faulty PRESENT-128 encryptions with random (nibble) fault values.
    # fault config: round = 30, fault location (nibble based) = random
    #sample(keysize=128,r=30,l=15,N=1000)


    # 80-bit fault injection
    """
    p80 = Present(ks=80)
    m = 0x0000000000000000
    k = 0x00000000000000000000
    f = (30,0x00000000009000000000) # (fault round, 80-bit fault value)
    c  = p80(m,k)
    cf = p80(m,k,f)
    print "c      = {:016x}".format(c)
    print "c'     = {:016x}".format(cf)
    print "c ^ c' = {:016x}".format(c ^ cf)
    """
