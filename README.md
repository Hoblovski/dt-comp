# Random C Program Generator
Randomly generate a C function. Tailered for minidecaf.

# Usage
```bash
$ ./cgen
$ ./cgenf

$ ./cgen -s 10007 # specify seed
```

Generation legality test: `while ./cgen > t.c && gcc t.c; do done`

# Tweaks
`./cgen -h` and check `config.py`.

# Problems
* `-Woverflow` and `-Wdiv-by-zero`
* Python is too slow, switch to Rust.

# Methodology
My approach is ad hoc.
There can be some more principled approach like grammar guided generation but I doubt their practicality.

The apprach is basically grammar driven DFS; the DFS functions are Stmt/Expr constructors.
DFS search state (declared variables etc) is stored in `GeneratorState` i.e. gs.
Constraints are scattered in ctors, gs, and `randexpr/randstmt`.

# Reference
* [csmith](github.com/csmith-project/csmith)

