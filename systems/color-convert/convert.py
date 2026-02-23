import sys
from pathlib import Path
import re

HEX_REGEX = '#([0-9a-fA-F]+)'
HEX_MAP = dict(zip('0123456789abcdef', range(16)))

def to_decimal(xx):
    return HEX_MAP[xx[0]] * 16 + HEX_MAP[xx[1]]

def hex_to_rgb(hex_string: re.Match) -> str:
    # Grab and normalize the hex color code.
    code = hex_string.group(1).lower()
    if len(code) <= 4:
        code = "".join((x + x for x in code))

    # Get decimal versions of rgb values.
    values = [
        to_decimal(code[0:2]), # red 
        to_decimal(code[2:4]), # green
        to_decimal(code[4:6])  # blue
    ]

    label = "rgb"

    # Maybe add alpha value.
    if len(code) == 8:
        label = "rgba"
        values.append(to_decimal(code[6:8]) / 255)

    return f"{label}({" ".join(str(d) for d in values)})"

if __name__ == "__main__":
    file = Path(sys.argv[1])

    if not file or not file.exists or file.suffix != ".css":
        print("Please include a valid CSS file to convert.")
        exit(1)

    result = re.subn(
        pattern=HEX_REGEX,
        repl=hex_to_rgb,
        string=file.read_text(),
    )

    print(f"Replaced {result[1]} hex codes with RGB values.")

    output_file = Path("output.css")
    output_file.write_text(result[0])

    exit(0)