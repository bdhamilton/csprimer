import struct

def encode(x: int) -> bytes:
    remaining = x
    result = []

    # Handle 0 separately
    if x == 0:
        return [0b00000000]

    # While there are digits left, peel off the last seven
    # digits and add them as a new byte to the result.
    while remaining > 0:
        lowest_seven_digits = remaining & 0b01111111
        remaining >>= 7
        result.append(lowest_seven_digits | 0b10000000)

    # Switch off the continuation bit of the last byte
    result[-1] &= 0b01111111

    return bytes(result)

def decode(bytes: bytes) -> int:
    result = 0

    # For each byte, peel off the payload, shift to the appropriate
    # position, and add to the result.
    i = 0
    for byte in bytes:
        payload = byte & 0b01111111
        payload <<= 7 * i
        result |= payload
        i += 1

    return result

def read_as_int(filepath) -> bytes:
    with open(filepath, "rb") as f:
        return f.read()
    
raw_binary = read_as_int("maxint.uint64")
initial_int = struct.unpack('>Q', raw_binary)[0]
encoded = encode(initial_int)
decoded = decode(encoded)

print(f"""
Raw binary: {raw_binary} (type {type(raw_binary)})
Converted to integer: {initial_int} (type {type(initial_int)})
Encoded integer: {encoded} (type {type(encoded)})
Decoded inter: {decoded} (type {type(decoded)})
Matching? {decoded == initial_int}
""")
