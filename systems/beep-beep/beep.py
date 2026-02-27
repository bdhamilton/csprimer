"""

1. Write a program that beeps a hard-coded number of times
2. Write a program that accepts a numeric argument and beeps that many times
3. Write a program that listens for input and accepts that as an argument.

"""

import sys
from time import sleep
import tty
import termios

def beep(n = 1):
  for _ in range(n):
    # We need to write straight to the buffer to keep Python from trying
    # to encode our byte value. b'\x07' is the ASCII code for BEL.
    sys.stdout.buffer.write(b'\x07')

    # Flush so the terminal receives BEL immediately, then pause between bells.
    sys.stdout.flush()
    sleep(0.2)

def read_char():
    # Get stdin's file descriptor and save its current settings.
    current_stdin = sys.stdin.fileno()
    old_settings = termios.tcgetattr(current_stdin)

    try:
        # Raw mode disables line-buffered input, so read(1) returns after
        # a single keypress instead of waiting for Enter.
        tty.setraw(current_stdin)
        ch = sys.stdin.read(1)
    finally:
        # Reset old settings after input has cleared to get out of raw mode.
        termios.tcsetattr(current_stdin, termios.TCSADRAIN, old_settings)
    return ch

while True:
    try:
        n = read_char() 

        if n == 'q':
            break

        beep(int(n))
    except:
        pass