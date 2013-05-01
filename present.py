class Present:
  def __init__(self,ks=80):
    assert ks in [80,128]
    self._ks = ks

    if self._ks == 80:
      self._mask = 0xffffffffffffffffffff
    else:
      self._mask = 0xffffffffffffffffffffffffffffffff

    self._sbox = [0xc,0x5,0x6,0xb,0x9,0x0,0xa,0xd,0x3,0xe,0xf,0x8,0x4,0x7,0x1,0x2]

    self._p = [
       0, 16, 32, 48,  1, 17, 33, 49,  2, 18, 34, 50,  3, 19, 35, 51,
       4, 20, 36, 52,  5, 21, 37, 53,  6, 22, 38, 54,  7, 23, 39, 55,
       8, 24, 40, 56,  9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59,
      12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63
    ]

  def __call__(self,m,k,f=None):

    if f == None:
      f = (0,0)

    # the cipher state
    self._s = m

    # the 80-/128-bit key register
    self._key_reg = k 

    for r in xrange(1,32):
      self._add_round_key()

      # fault injection
      if f[0] == r:
        self._key_reg ^= f[1]

      self._update_key(r)
      self._sbox_layer()
      self._p_layer()
    self._add_round_key()

    return self._s


  def _add_round_key(self):
    self._s ^= self._extract_key()

  def _sbox_layer(self):
    for i in xrange(16):
      s = ( self._s >> ( 60 - 4*i ) ) & 0xf # extract 4-bits from the state
      self._s ^= ( ( self._sbox[s] ^ s ) << ( 60 - 4*i ) )


  def _p_layer(self):
    s = 0
    for i in xrange(64):
      s ^= ( (self._s >> i ) & 0x1 ) << self._p[i]
    self._s = s


  def _extract_key(self):
    # extracts a 64-bit round key from the key register
    return self._key_reg >> self._ks - 64



  # 0xffffffff 32-bit
  # 0xffffffffffffffff 64-bit
  # 0xffffffffffffffffffff 80-bit
  # 0xffffffffffffffffffffffffffffffff 128-bit
  def _update_key(self,r):

    # shift key register cyclically 61 positions to the left
    self._key_reg = ( ( self._key_reg << 61 ) & self._mask | ( self._key_reg >> self._ks - 61 ) )

    if self._ks == 80:
      k = self._key_reg >> 76
      self._key_reg ^= (self._sbox[k] ^ k) << 76
      self._key_reg ^= r << 15
    else:
      k0 = (self._key_reg >> 124) & 0xf
      k1 = (self._key_reg >> 120) & 0xf
      self._key_reg ^= ( ( ( ( self._sbox[k0] ^ k0 ) << 124 ) ^ ( self._sbox[k1] ^ k1 ) << 120 ) ) 
      self._key_reg ^= r << 62


