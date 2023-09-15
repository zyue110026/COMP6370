#!/usr/bin/python3
import hashlib
import sys

EMAIL = 'yzz0229@auburn.edu%d'
TARGET_PREFIX = EMAIL[:3].encode() + b'\x00'


def find_collision():
    seen_hashes = {}
    n = 0
    while True:
        h = hashlib.sha256((EMAIL % n).encode()).digest()[:4]

        # Check if the first four bytes match the target prefix
        if h == TARGET_PREFIX:
            if h in seen_hashes:
                sys.stdout.write(f"{EMAIL % seen_hashes[h]}\n")
                sys.stdout.write(f"{EMAIL % n}\n")
                sys.exit(0)

            else:
                seen_hashes[h] = n
        n += 1

def main():
    find_collision()

    #input 1: yzz0229@auburn.edu4832951051
    #input 2: yzz0229@auburn.edu5660354521
    # print(hashlib.sha256('yzz0229@auburn.edu4832951051'.encode()).digest().hex())
    # print(hashlib.sha256('yzz0229@auburn.edu5660354521'.encode()).digest().hex())
    # print(EMAIL[:3].encode().hex())
if __name__ == "__main__":
    main()
