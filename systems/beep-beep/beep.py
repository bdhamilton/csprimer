import sys
from time import sleep
import tty
import termios


old_settings = termios.tcgetattr(0)
tty.setcbreak(0)

def beep():
    while True:
        character = sys.stdin.read(1)
        if character == 'q':
            exit(0)

        try:
            number = int(character)
            for _ in range(number):
                sys.stdout.buffer.write(b'\x07')
                sys.stdout.flush()
                sleep(0.2)
        except:
            pass

try:
    beep()
finally:
    termios.tcsetattr(0, termios.TCSADRAIN, old_settings)
