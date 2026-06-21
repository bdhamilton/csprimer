# Hello, C!

Goal: write, compile, and execute a simple "Hello, world!" program in C.

## Notes

* Both `gcc --version`, `cc --version`, and `clang --version` work out of the box on my Mac, and seem to point to the same compiler.
* Found the syntax at [Hyperpolyglot](https://hyperpolyglot.org/c#grammar-invocation)
  * Some of the boilerplate is unintelligible to me now: why `main` is called an `int` (because it _returns_ an int, an exit code? apparently implicit?), what `argc` and `argv` are (unused here), what `**` means (something about these mysterious pointers?), what `.h` means?
  * `.h` apparently means that this is a _header_ file, though I'm not sure what that is.
* `clang --help` prints a huge number of options that are mostly unintelligible to me.
* It outputs an `a.out` file, nonsense when read with `cat`, but the code is visible in a `hexdump`.

After watching the rest of the video, a few initial clarifications and answers:

* Confirmed that `main` (which is required in any C program) must return an `int`, either 0 for success or non-zero for failure, and that 0 is implicitly returned by default if nothing else is provided. This is part of its coupling with Unix, which expects this behavior.
* `main` provides two arguments: `argc` which is a count of arguments, and `argv` which is an array of argument values. In this case they could be omitted because neither is used.