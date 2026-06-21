
with open("cases", "rb") as f:
    lines = f.read().split(b'\n')

with open("expected", "r") as f:
    expected = f.read().split("\n")

def clean_trailing_bytes(bytes: bytes) -> bytes:
    if len(bytes) == 0:
        return bytes
    
    index = len(bytes) - 1
    print(f"Checking { format(bytes[index], '08b') }...")

    # 0xxxxxxx is a terminal byte.
    if bytes[index] >> 7 == 0:
        print(f"{ format(bytes[index], '08b')  } is a terminal byte.")
        return bytes
    
    # 10xxxxxx is a continuation byte.
    continuations = 0
    while bytes[index] >> 6 == 0b10:
        print(f"{ format(bytes[index], '08b')  } is a continuation byte...")
        continuations += 1
        index -= 1

    print(f"Expecting { continuations } continuation bytes.")

    # Compare expected to discovered continuations.
    print(f"Found start of character: { format(bytes[index], '08b')  }")
    first_four = bytes[index] >> 4
    print(f"Testing first four digits: { format(first_four, '04b')}")
    if first_four == 0b1111:
        print("Expecting 3 continuations.")
        if continuations != 3:
            return bytes[:index]
    elif first_four == 0b1110:
        print("Expecting 2 continuations.")
        if continuations != 2:
            return bytes[:index]
    elif first_four == 0b1100:
        print("Expecting 1 continuations.")
        if continuations != 1:
            return bytes[:index]

    return bytes

matches = 0
misses = 0
for i, msg in enumerate(lines):
    if not msg:
        break 
    
    truncate_length = msg[0]
    truncated_message = clean_trailing_bytes(msg[1:truncate_length + 1])
    decoded = truncated_message.decode()
    does_match = decoded == expected[i]
    if does_match:
        matches += 1
    else:
        misses += 1 
    print(f"\nOriginal: { str(msg[1:]) }")
    print(f"Truncated: { decoded }")
    print(f"Expected: { expected[i] }")

    print(f"Matches expected: { does_match }")

print(f"Matches: { matches }. Misses: { misses }.")

