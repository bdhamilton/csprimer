# [Protobuf varint](https://csprimer.com/watch/varint/)

Goal: implement the [Base 128 Varint](https://protobuf.dev/programming-guides/encoding/#varints) encoding used in Protocol Buffers.

## Notes

### Background

This is my first time learning about binary. Binary notation is a way of writing numbers, analogous to the decimal notation we're used to. In decimal, each digit can be one of ten possible values (0-9) and each position represents a power of ten (ones, tens, hundreds, etc.). In binary notation, each digit can be one of two possible values (0-1) and each position represents a power of two (ones, twos, fours, eights, etc.). So for example:

* 1 = 1
* 4 = 100
* 5 = 101
* 10 = 1010

This is also my first time learning about bits and bytes. A "bit" is simply a "binary digit": a 0 or a 1. A "byte" is a slice of memory with a specific address in the computer. In theory a byte could be any of various sizes, but for historical reasons a byte on a modern computer is 8 bits. That means that the biggest number that can be represented in a single byte is 11111111, or in decimal, 255. 

Obviously we often need to send higher numbers than that over the wire, which means we'll need to use multiple bytes (multiple memory addresses) to represent a single number. This raises another question about _byte order_. When we send a multi-byte number over the wire, should we send the smaller or larger digits first? It turns out that different computer systems make different decisions about this, so we sometimes need to handle both.

The order that's most intuitive to me is called "big endian" order. Big endian order leads with the bigger digits, such that `00000001 000000010` = 258. But some systems use "little endian" order, leading with the least significant byte. In that case, `00000001 00000010` = 513.

In principle you can represent numbers in any number of different notations, not just binary or decimal. One other notation in wide use is _hexadecimal_, where each digit represents values from 0–15 and each position represents a power of sixteen. Since we only have numeric symbols for the values 0-9, we borrow from the alphabet for the remaining values: A-F represeent 10–15. Hexadecimal notation is a convenient representation of bytes because it can represent the full range of possible values (0-255) in just two digits. Thus `ff` = `11111111` = `255`.

### The problem

Since we know we'll sometimes need to send numbers greater than 255 over the wire, we have two choices. We _could_ reserve a set amount of memory for every number, say 8 bytes (64 bits), that was big enough to handle the biggest number we'd ever care about. Then the message receiver would know that they'd need to examine 8 bytes of data to interpret any given number. But since most of the numbers we'll send would be much smaller, we'd end up wasting a lot of memory that way. 

We could also find a way of communicating where a number _ends_, so we never used more than the necessary amount of memory to store a number. This is the "varint" or "variable-width inteeger," which we're going to be implementing here. Varints are way of using the _fewest necessary bytes_ to encode a number.

The strategy used by Protocol Buffers is to reserve the first bit in every byte for use as a _continuation_ bit: a message about whether this byte marks the end of the current number (in which case the bit is 0) or the number continues to the next (in which case the bit is 1). 

The tradeoff is that by reserving the first bit for a continuation marker, each byte can store only 7 digits of the number itself---128 possible values. (Thus a "base 128 varint.") But that allowance makes it possible to use much less space overall.

For reasons I don't know, protobuf sends multi-byte integers in little endian order. 

The challenge here is how to write a function that converts a number in decimal to a base 128 varint in bytes, and another function that decodes it back.

### The implementation background

There