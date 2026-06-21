# UTF-8 Truncate

Goal: cleanly truncate a byte-limited string, without leaving partial characters behind.

## Oz's instructions

- The "cases" file has one case per line. The first byte is an unsigned integer indicating the number of bytes to which to truncate; the remained is a utf-8 encoded string to truncate.
- The "expected" file has one expected result per line.
- Your program should read "cases", parse it, and write one correctly truncated string per line. This output can then be `diff`ed against "expected".
- Do not truncate the string in the middle of a single unicode codepoint! This is the purpose of the exercise.
- None of the cases cover grapheme clusters like 👨‍👩‍👧‍👦 (family of 4) ... this is a challenging stretch goal; see https://unicode.org/reports/tr29/

## How UTF-8 encoding works

The first thing necessary to understand is how UTF-8 encodes Unicode characters.

In Unicode, every distinct character is expressed in a codepoint: e.g., U+2764 corresponds to a red heart emoji. The codepoeint is a prefix `U+` plus a hexademical number.

There have been various attempts to encode these values into legible bytes, but UTF-8 has won the day. UTF-8 has the advantage of being backwards compatible with ASCII (another encoding that could only handle unaccented Latin characters), easily extensible to a large extent, and variable width so we don't use more memory than strictly necessary to encode a character.

The scheme is:

* For characters at codepoints <128 (7 bits), which includes all of ASCII, we prefix with a single `0`. Capital A (U+0041) is `0b01000001` (65).
* If a character needs more than one byte, it required a _leading byte_ that encodes how many bytes will be needed and _continuation bytes_.
  * The _leading byte_ is prefixed with the number of bytes needed **in unary**, then a `0` divider, then the payload. 
  * Each _continuation byte_ is prefixed with `10`, then the payload.
* For example, a sandwich emoji (`U+1F96A`) requires four bytes.
  * The first byte starts with `11110`; the next three start with `10`.
  * The payload then reads in big-endian order, right-aligned, in the remaining payload bits: `11110000 10011111 10100101 10101010`.
* The result is a scheme that allows 2^21 (~2mil) characters to be encoded. The current version has 2^18 (~300k) assigned codepoints.

## The algorithm

I hit on the core algorithm fairly quickly:

* Parse into lines, separating the truncate length from the message
* Look from the end to see if any partial characters have been left behind
* If so, delete them
* Return truncated strings

But my initial attempt got overly complex because I looked at the wrong side of the cut. I first truncated at `n` bytes, then looked to see whether what was left included the expected number of continuation bytes. That meant _counting_ the continuation bytes and then comparing against the leading byte. Correct, but cumbersome.

Oz's solution was far simpler: _look at the byte we're throwing away_. If it's a continuation byte, all preceding bytes and the leading byte need to be thrown away. So all we need is:

```python
while msg[:n] >> 6 == 0b10:
  n -= 1
return msg[:n]
```

