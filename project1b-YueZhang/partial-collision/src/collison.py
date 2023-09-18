#!/usr/bin/python3
import hashlib
import sys
import random
import time

EMAIL = 'yzz0229@auburn.edu%d'
TARGET_PREFIX = EMAIL[:3].encode() + b'\x00'
INPUTS = []


def find_collision(start, end):
    # print("start collision")

    for n in range(start, end):
        h = hashlib.sha256((EMAIL % n).encode()).digest()[:4]
        if len(INPUTS) < 2:
            # Check if the first four bytes match the target prefix
            if h == TARGET_PREFIX:
                if len(INPUTS) == 0:
                    INPUTS.append(EMAIL % n)
                    sys.stdout.write(f"{EMAIL % n}\n")
                elif len(INPUTS) == 1:
                    if (EMAIL % n) != INPUTS[0]:
                        INPUTS.append(EMAIL % n)
                        sys.stdout.write(f"{EMAIL % n}\n")
        else:
            return 0

def main():
    # print(len(INPUTS))
    random.seed(time.time())
    start = random.randint(0, 1000000000000)
    end = 1000000000000

    while len(INPUTS) != 2:
        # sys.stdout.write(f"start: {start} end: {end} INPUTS: {len(INPUTS)}")
        find_collision(start, end)
        if start <= end:
            end = start
            if end > 3:
                start = random.randint(0, end)
            else:
                sys.stderr.write("Can not find valid inputs")
                sys.exit(0)

if __name__ == "__main__":
    main()
