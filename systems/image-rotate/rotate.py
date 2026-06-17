"""
Plan:

* [x] Figure out how to read the bitmap as bytes
* [x] Extract relevant bytes from header
"""
import sys
import math
  

def little_endian(bytes: bytes) -> int:
    n = 0
    for i, byte in enumerate(bytes):
        n += (byte << (i * 8))
    return n

if __name__ == "__main__":
    filepath = str(sys.argv[1])
    data = open(filepath, "rb").read()
    print(type(data))

    assert data[0:2] == b'BM'

    offset = little_endian(data[10:14])
    width, height = little_endian(data[18:22]), little_endian(data[22:26])
    bits_per_pixel = little_endian(data[28:30])
    bytes_per_pixel = int(bits_per_pixel / 8)
    width_in_bytes = width * bytes_per_pixel
    # row_length_in_bits = math.ceil((bits_per_pixel * width) / 32) * 4
    # row_length_in_bytes = int(row_length_in_bits / 8)

    # copy the header exactly
    rotated = bytearray(data[:offset])

    # build a new row, column by column from right to left
    for row in range(1, width + 1):
        for col in range(1, height + 1):
            start = offset + (col * width_in_bytes - row * bytes_per_pixel)
            rotated += data[start:start + bytes_per_pixel]

    with open('out.bmp', 'wb') as f:
        f.write(rotated) 