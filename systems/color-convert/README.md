# [CSS color convert](https://csprimer.com/watch/color-convert/)

Goal: Write a script that converts the hex codes in a CSS file to equivalent `rgb(...)` descriptions for legibility.

This was much more straightforward than [implementing a varint](../varint/README.md). It exercised my new understanding of the hexadecimal number system, and gave me a little more practice with regular expressions. I didn't learn anything fundamental new, but I learned some new things about Python and reinforced some others.

* To do an in-stream regex replacement, use `re.sub(regex, replacement, string, flags)`. `replacement` can be a literal string or a callable. Just remember that what the callable receives is a `Match` object, not the resulting string. To get the resulting string, use `match.group(0)` (or whichever group you need).
* `dict(zip('0123456789abcdef', range(16)))` is a really easy, concise way to build a map. I had initially written this out manually, but this is way nicer.

The bigger things I learned, though, were about my own workflow.

* In his walkthrough, Oz took a few minutes at the beginning to spin up a basic feedback loop. This made it really trivial to see the output of his work and compare it against his expected output. I didn't do that, and as a result wasted time running and spot-checking output. 
* I always get hung up optimizing before I should. I spent a stupid amount of time hemming and hawing about the creation of a basic lookup map for hex values, because it seemed so painfully manual and I thought for sure there would just be a Python function for that. Maybe there still is, but it took all of 45s to write out the map. Why didn't I do it right away? Similarly, I got way ahead of myself trying to solve the "advanced" version before I'd solved the "simple" version. Optimizing too early is a big weakness

