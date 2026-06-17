# Image rotate

Goal: rotate a bitmap image by 90 degrees. 

## Walkthrough

The first step was to read the [Wikipedia entry for bitmap images](https://en.wikipedia.org/wiki/BMP_file_format#DIBs_in_memory), which describes the shape of the header. The header encodes a lot of the information we need (width, height, bits per pixel, offset of the image data, etc.) at fixed byte locations.

Then I had to remember how to read, work with, and write binary data in bash and Python.

```bash
hexdump -C teapot.bmp
```

```python
with open(filepath, "rb") as f: # `b` means `read as bytes`
  data = f.read() # reads the file into memory as a `bytes` object

with open(filepath, "wb") as f: # `b` means `write as bytes`
  f.write(data_to_write)
```

I learned that a `bytes` object is accessible at a specific index, and when accessed appears _as an integer_. **There is no single-byte scalar in Python; it's just an integer underwritten by a binary encoding.** 

I initially used a built-in method to convert from a little-endian multibyte number to an `int`: `int.from_bytes(bytes, "little")`. But we can do also do it manually in a fairly straightforward way using bitwise operators:

```python
def little_endian(bytes: bytes) -> int:
    n = 0
    for i, byte in enumerate(bytes):
        n += (byte << (i * 8))
    return n
```

This works because we leave the leftmost byte in place (`byte << 0`) and move each subsequent byte one byte further to the left.

I really got tangled on the actual rotation logic---which pixel needs to go where, how to correct for the offset, how to account for the number of bytes per pixel. But it turned out to be fairly simple, in the end. My mental model was that each _column_ in the original image, moving from bottom to top and right to left, becomes a _row_ in the new image, moving from bottom to top and left to right. I.e.,

```
7 8 9       1 4 7
4 5 6  -->  2 5 8
1 2 3       3 6 9
```

Two big things my implementation scoped out, and I'm not following up on now:

* This works only because it's a square. I have no confidence it works on rectangles.
* BMP files pad rows to a multiple of four bytes. I started working on that, but didn't finish it, and my implementation is probably wrong. It didn't matter in my case, because the supplied image needed no padding.


## Scratch


* `hexdump -C teapot.bmp | head -10` shows that the two bitmaps carry the same first 6 binary lines, which must be some kind of BMP header, followed by an asterix in place of the 7th line---not sure what that means. Actually the 8th line is also the same. Divergence begins on the 9th line.
* `diff teapot.bmp rotated.bmp` shows `Binary files teapot.bmp and rotated.bmp differ`. Can use that to compare.
* I've already forgotten how to really interpret this hexdump output. It's outputting hex, obviously, and I remember that two hexadecimal digits can express the same range of values as eight binary digits (0-255), i.e.,  one byte. So each line is showing me 16 bytes. I think I remember that the end of the line is showing me an ASCII representation of those bytes.
* Right now I'd have absolutely no idea how to rotate this. It makes sense to me that we'd just be trying to swap bytes in a consistent way, but I'm not sure which bytes correspond to what.

The [Wikipedia entry for bitmap images](https://en.wikipedia.org/wiki/BMP_file_format#DIBs_in_memory) describes the shape of the header:

* 0-1: a header field, in this case `BM`, that identifies the file.
* 2–5: the size of the file in bytes, in this case `ba 13 08 00`. 
* 6-9: reserved for the application, in this case all `00`.
* 10–13: the address where the actual image starts, which tells us the size of the header, in this case `8a 00 00 00` = `138`. That correspends to the `BITMAPV5HEADER`, which takes 124 bytes plus the 14 already used. **The bitmap actually starts halfway across line `80`.**
* 14–17: the size of the header , in this case `7c 00 00 00` = `124`, as we just inferred.
* 18–21: the image width, here `a4 01 00 00` = `429`
* 22–25: the image height, here `a4 01 00 00` = `429`
* 26–27: number of color panes, `01 00`
* 28–29: number of bits per pixel, `18 00` (`24` = 3 bytes---I guess that means there's no alpha channel?)
* 30–33: compression method, `00 00 00 00`
* 34–37: size of the raw bitmap data, `30 13 08 00`
* 38–41: horizontal resolution, `12 0b 00 00`
* 42–45: vertical resolution, `12 0b 00 00`
* 46–49: number of colors in the palette, `00 00 00 00` (defaults to 2^n)
* 50–53: number of important colors (usually ignored), `00 00 00 00`
* 54–55: specifies the _units_ for horizontal and vertical resolution, `00 ff`
* 56–57: padding, `00 00`
* 58–59: **the direction in which the bits fill the bitmap**, only defined value is 0, both use `ff 00`

Pixels fill from the bottom left corner, left to right, then bottom to top. 

The algorithm is basically: rebuild each row, left to right, from each column, bottom to top, starting from the right.

Each row is stored together, rounded up to a multiple of 32 bits / 4 bytes. The end is padded with zeros. 

This gives us most of what I should need:

* Get width, height, starting point
* Calculate length of row

Since we're starting with a square, let's just solve for a square.

If I could access each byte as a list:

```
def int_from_bytes(bytes):
  pass

width = int_from_bytes(bytes[18:22])
height = int_from_bytes(bytes[22:26])
bits_per_pixel = int_from_bytes(bytes[28:30])
starting_index = int_from_bytes(bytes[10:14])

row_length_in_bits = ceil((bits_per_pixel * width) / 32) * 4
```