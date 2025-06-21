import hashlib
import struct
import sys

def shift_left(val, num):
    val &= 0xFFFF
    return ((val << num) | (val >> (16 - num))) & 0xFFFF

def algo1_A68(p1, p2, p3, p4):
    A, B, C, D = p1, p2, p3, p4

    A = (A + D) & 0xFFFF
    D = (D + C) & 0xFFFF
    C = (C + B) & 0xFFFF
    B = (B + A) & 0xFFFF

    A = shift_left(A, 2)
    B = shift_left(B, 9)
    C = shift_left(C, 1)
    D = shift_left(D, 4)

    A = (A + 6) & 0xFFFF
    B = (B + 7) & 0xFFFF

    A ^= B
    B ^= C
    C ^= D
    D ^= A

    return A, B, C, D

def algo2_A68(p1, p2, p3, p4):
    A, B, C, D = p1, p2, p3, p4

    A = (A + D) & 0xFFFF
    D = (D + C) & 0xFFFF
    C = (C + B) & 0xFFFF
    B = (B + A) & 0xFFFF

    A = shift_left(A, 6)
    B = shift_left(B, 0)
    C = shift_left(C, 8)
    D = shift_left(D, 3)

    A = (A + 3) & 0xFFFF
    B = (B + 9) & 0xFFFF
    C = (C + 2) & 0xFFFF
    D = (D + 3) & 0xFFFF

    A ^= B
    B ^= C
    C ^= D
    D ^= A

    return A, B, C, D

def main_algo(data):
    RecvData = bytearray(32)
    RecvData[:32] = data
    i = j = 0

    while i < 32:
        p1, = struct.unpack_from("<H", RecvData, i)
        i += 2
        p2, = struct.unpack_from("<H", RecvData, i)
        i += 2
        p3, = struct.unpack_from("<H", RecvData, i)
        i += 2
        p4, = struct.unpack_from("<H", RecvData, i)
        i += 2

        p1, p2, p3, p4 = algo1_A68(p1, p2, p3, p4)

        struct.pack_into("<H", RecvData, j, p4)
        j += 2
        struct.pack_into("<H", RecvData, j, p3)
        j += 2
        struct.pack_into("<H", RecvData, j, p2)
        j += 2
        struct.pack_into("<H", RecvData, j, p1)
        j += 2

        p1, = struct.unpack_from("<H", RecvData, i)
        i += 2
        p2, = struct.unpack_from("<H", RecvData, i)
        i += 2
        p3, = struct.unpack_from("<H", RecvData, i)
        i += 2
        p4, = struct.unpack_from("<H", RecvData, i)
        i += 2

        p1, p2, p3, p4 = algo2_A68(p1, p2, p3, p4)

        struct.pack_into("<H", RecvData, j, p4)
        j += 2
        struct.pack_into("<H", RecvData, j, p3)
        j += 2
        struct.pack_into("<H", RecvData, j, p2)
        j += 2
        struct.pack_into("<H", RecvData, j, p1)
        j += 2

    return ''.join([f"{byte:02x}" for byte in RecvData])

key = "12345678"

def main():
    rand_number = sys.argv[1]
    output_file = sys.argv[2]

    buf_rand_key = (rand_number + key).encode('ascii')
    md5sum = hashlib.md5(buf_rand_key).digest()
    output = bytearray(md5sum.hex(), 'ascii')

    result_hex = main_algo(output)
    print("Final hex:", result_hex)

    with open(output_file, 'w') as f:
        f.write(result_hex)

if __name__ == "__main__":
    main()
