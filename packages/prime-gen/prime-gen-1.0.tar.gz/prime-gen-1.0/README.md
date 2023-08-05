A package for generating and checking prime numbers.

# Installation
You can install `prime-gen` via the command line by using:

```
python -m pip install --user prime-gen
```

# Example Usage

```py
>>> import prime_gen
>>> prime_gen.p(100)
False
>>> prime_gen.p(97)
True
>>> prime_gen.p(93)
False
>>> prime_gen.p(5)
True
>>> prime_gen.p(13)
True
>>> prime_gen.g(100)
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
>>> prime_gen.g(20)
[2, 3, 5, 7, 11, 13, 17, 19]
```