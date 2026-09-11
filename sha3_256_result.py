import struct
import hashlib

ROTATION = [
    [0, 36, 3, 41, 18],
    [1, 44, 10, 45, 2],
    [62, 6, 43, 15, 61],
    [28, 55, 25, 21, 56],
    [27, 20, 39, 8, 14]
]

RC = [
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
    0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
    0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
    0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
    0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008
]

MASK64 = 0xFFFFFFFFFFFFFFFF

def rotl64(x, n):
    return ((x << n) | (x >> (64 - n))) & MASK64

def sha3_verify(msg_bytes):
    rate = 136
    pad_len = (134 - (len(msg_bytes) % rate)) % rate
    padded = msg_bytes + b'\x06' + b'\x00' * pad_len + b'\x80'

    state = [0] * 25
    block = padded[:rate]
    for j in range(len(block) // 8):
        word = int.from_bytes(block[j*8:(j+1)*8], 'little')
        state[j] ^= word

    print("=" * 60)
    print("INITIAL STATE (after absorption)")
    print("=" * 60)
    for y in range(5):
        print(" ".join(f"{state[x+5*y]:016x}" for x in range(5)))

    for rnd in range(24):
        C = [state[x] ^ state[x+5] ^ state[x+10] ^ state[x+15] ^ state[x+20] for x in range(5)]
        D = [(C[(x+4)%5] ^ rotl64(C[(x+1)%5], 1)) for x in range(5)]
        for i in range(5):
            state[i]    ^= D[i]
            state[i+5]  ^= D[i]
            state[i+10] ^= D[i]
            state[i+15] ^= D[i]
            state[i+20] ^= D[i]

        # Rho+Pi
        B = [0]*25
        for y in range(5):
            for x in range(5):
                idx = 5*y + x
                rot = ROTATION[x][y]
                val = state[idx]
                if rot:
                    val = rotl64(val, rot)
                new_idx = 5*((2*x + 3*y) % 5) + y
                B[new_idx] = val
        state = B

        # Chi
        for y in range(5):
            t = [state[5*y + x] for x in range(5)]
            for x in range(5):
                state[5*y + x] = t[x] ^ ((~t[(x+1)%5]) & t[(x+2)%5])

        # Iota
        state[0] ^= RC[rnd]

        print(f"\nCYCLE {rnd}")
        print("  C   :", " ".join(f"{v:016x}" for v in C))
        print("  D   :", " ".join(f"{v:016x}" for v in D))
        print("  State after cycle:")
        for y in range(5):
            print("    " + " ".join(f"{state[x+5*y]:016x}" for x in range(5)))

    digest = state[0].to_bytes(8,'little') + state[1].to_bytes(8,'little') + \
             state[2].to_bytes(8,'little') + state[3].to_bytes(8,'little')
    print("\nFINAL DIGEST:", digest.hex())
    print("hashlib:      ", hashlib.sha3_256(msg_bytes).hexdigest())
    print("MATCH:        ", digest.hex() == hashlib.sha3_256(msg_bytes).hexdigest())

if __name__ == '__main__':
    sha3_verify(b'AbdulmajeedMeshalTariq')