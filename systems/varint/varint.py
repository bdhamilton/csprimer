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

assert decode(b'\x96\x01') == 150
print("test")