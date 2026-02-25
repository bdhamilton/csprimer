"""

1. Write a program that beeps a hard-coded number of times
2. Write a program that accepts a numeric argument and beeps that many times
3. Write a program that listens for input and accepts that as an argument.

"""

import sys
from time import sleep

def beep(n = 1):
  for _ in range(n):
    sys.stdout.buffer.write(b'\x07')
    sys.stdout.flush()
    sleep(0.3)

try:
  n = int(sys.stdin.read())
  beep(n)
except:
  pass