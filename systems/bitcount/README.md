# Bitcount

Goal: write a C function that, given an integer, returns the number of bits that are on.

## Notes

`x &= (x-1)` deletes the rightmost 1-bit, I'm told. How?

```
x = 11
x = 11 & 10
x = 1011 & 1010
x = 1010

x = 10
x = 10 & 9
x = 1010 & 1001
x = 1000

x = 8
x = 8 & 7
x = 1000 & 111
x = 0
```

I can see it working here, but I'm not totally sure I understand the logic. If x is odd, the ones digit will be 1. Subtracting 1 will flip that bit off. If x is even, subtracting one will flip off some higher even digit and flip on the one. 

