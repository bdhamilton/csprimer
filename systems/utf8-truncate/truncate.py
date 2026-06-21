import sys

def truncate(string, n): 
    if len(string) <= n:
        return string
    while string[n] >> 6 == 0b10:
        n -= 1
    return string[:n]

with open("cases", "rb") as f:
    lines = f.read().split(b'\n')

truncated_lines = [truncate(line[1:], line[0]) for line in lines if line]

for line in truncated_lines:
    sys.stdout.buffer.write(line + b'\n')
