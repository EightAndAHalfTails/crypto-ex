from pairs import pairs_k5_0b00_0606 as pairs1
from pairs import pairs_k5_000d_a0a0 as pairs2

#from pairs_null_key import pairs_k5_0b00_0606 as pairs1
#from pairs_null_key import pairs_k5_000d_a0a0 as pairs2

s_inv = [14, 3, 4, 8, 1, 12, 10, 15, 7, 13, 9, 6, 11, 2, 0, 5]

def differential(pairs, dout, mask):
    poss = {}
    for candidate in range(2**16):
        if candidate & ~mask != 0:
            continue
        for C, Cp in pairs:
            # invert the addition of the 5th sub-key
            T = C ^ candidate
            Tp = Cp ^ candidate
        
            # invert the 4th S-boxes
            U = 0
            Up = 0
            for i in range (0, 16, 4):
                U |= (s_inv[(T >> i) & 0xf] << i)
                Up |= (s_inv[(Tp >> i) & 0xf] << i)

            if (U ^ Up) & mask == dout:
                learned = candidate & mask
                if learned in poss:
                    poss[learned] += 1
                else:                    
                    poss[learned] = 1
    v=list(poss.values())
    k=list(poss.keys())
    return (k[v.index(max(v))], max(v))

key1, freq1 = differential(pairs1, 0x0606, 0x0f0f)
key2, freq2 = differential(pairs2, 0xa0a0, 0xf0f0)

print("Key 0x{0:0>4x} is most probable, occurring {1} times".format(key1, freq1))
print("Key 0x{0:0>4x} is most probable, occurring {1} times".format(key2, freq2))
print("So full key is likely 0x{0:0>4x}".format(key1 | key2))    
