import struct
def ROL(n, x):
    return ((x << n) & 0xffffffff) | (x >> (32 - n))
def ROL1(x, n):
    return ((x << n) & 0xffffffff) | (x >> (32 - n))

def F(j, x, y, z):
    if(0<=j<=15):
      return x ^ y ^ z
    if(16<=j<=31):
      return (x & y) | (((~x) % 0x100000000) & z)
    if(32<=j<=47):
      return (x | ((~y) % 0x100000000)) ^ z
    if(48<=j<=63):
      return (x & z) | (((~z) % 0x100000000) & y)
    if(64<=j<=79):
      return x ^ (y | ((~z) % 0x100000000))

def K1(j):
  if(0<=j<=15):
      return 0x00000000
  if(16<=j<=31):
      return 0x5A827999
  if(32<=j<=47):
      return 0x6ED9EBA1
  if(48<=j<=63):
      return 0x8F1BBCDC
  if(64<=j<=79):
      return 0xA953FD4E

def K2(j):
  if(0<=j<=15):
      return 0x50A28BE6
  if(16<=j<=31):
      return 0x5C4DD124
  if(32<=j<=47):
      return 0x6D703EF3
  if(48<=j<=63):
      return 0x7A6D76E9
  if(64<=j<=79):
      return 0x00000000

def R1(j, M):
   r1 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15, 7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8, 3, 10, 14, 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12, 1, 9, 11, 10, 0, 8, 12, 4, 13, 3, 7, 15, 14, 5, 6, 2, 4, 0, 5, 9, 7, 12, 2, 10, 14, 1, 3, 8, 11, 6, 15, 13]
   return M[r1[j]]

def R2(j, M):
    r2 = [5,  14,  7,  0,  9,  2,  11,  4,  13,  6,  15,  8,  1,  10,  3,  12,  6,  11,  3,  7,  0,  13,  5,  10,  14,  15,  8,  12,  4,  9,  1,  2,  15,  5,  1,  3,  7,  14,  6,  9,  11,  8,  12,  2,  10,  0,  4,  13,  8,  6,  4,  1,  3,  11,  15,  0,  5,  12,  2,  13,  9,  7,  10,  14,  12,  15,  10,  4,  1,  5,  8,  7,  6,  2,  13,  14,  0,  3,  9,  11]
    return M[r2[j]]
def S1(j):
    s1 = [11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8, 7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12, 11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5, 11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12, 9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 13, 14, 11, 8, 5, 6]
    return s1[j]
def S2(j):
    s2 = [8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6, 9, 13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11, 9, 7, 15, 11, 8, 6, 6, 14, 12, 13, 5, 14, 13, 13, 7, 5, 15, 5, 8, 11, 14, 14, 6, 14, 6, 9, 12, 9, 12, 5, 15, 8, 8, 5, 12, 9, 12, 5, 14, 6, 8, 13, 6, 5, 15, 13, 11, 11]
    return s2[j]

s = str(input())

bin_s = ''.join(format(x, '08b') for x in bytearray(s, 'utf-8'))
b = bin(len(bin_s))[2:].zfill(64)
M = []
s = []
bin_s = bin_s+'1'

while(len(bin_s)%512!=448):
  bin_s = bin_s+'0'

bin_s = bin_s + b[32:] + b[0:32]
t = []
M = []
m = ''
for j in range(0, len(bin_s)-64, 32):
    b_s = bin_s[j:j+32]
    m = ''
    s = []
    for k in range(0, 32, 8):
      s.append(b_s[k:k+8])
    m = m + "".join(s[::-1])
    M.append(m[0:32])
M.append(bin_s[len(bin_s)-64:len(bin_s)-32])
M.append(bin_s[len(bin_s)-32:len(bin_s)])
for i in range(0,len(bin_s), 512):
    t.append(bin_s[i:i+512])
H = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]
for i in range(0, len(t)):
  A1 = H[0]
  A2 = H[0]
  B1 = H[1]
  B2 = H[1]
  C1 = H[2]
  C2 = H[2]
  D1 = H[3]
  D2 = H[3]
  E1 = H[4]
  E2 = H[4]
  m = M[i*16:i*16+16]
  for j in  range(0, 80):
    T = (ROL1((A1 + F(j, B1, C1,D1) + int(R1(j, m),2) + K1(j))%0x100000000, S1(j)) + E1)%0x100000000
    A1=E1;
    E1 = D1;
    D1 = ROL1(C1, 10)
    C1 = B1
    B1 = T
    T = (ROL1((A2 + F(79-j, B2, C2,D2) + int(R2(j, m),2) + K2(j))%0x100000000, S2(j)) + E2)%0x100000000
    A2=E2;
    E2 = D2;
    D2 = ROL1(C2, 10)
    C2 = B2
    B2 = T
  T = (H[1]+C1+D2)%0x100000000
  H[1] = (H[2] + D1 + E2)% 0x100000000
  H[2] = (H[3] + E1 + A2)% 0x100000000
  H[3] = (H[4] + A1 + B2)% 0x100000000
  H[4] = (H[0] + B1 + C2)% 0x100000000
  H[0] = T%0x100000000
print(hex(int.from_bytes(struct.pack("<5L", *H), byteorder='big'))[2:])
output = hex(int.from_bytes(struct.pack("<1L", H[0]), byteorder='big'))[2:].zfill(8)
for i in range(1, 5):
  output = output + " " + hex(int.from_bytes(struct.pack("<1L", H[i]), byteorder='big'))[2:].zfill(8)
print(output)
