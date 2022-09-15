# Random C Program Generator
Randomly generate a C function. Tailered for minidecaf.

# Usage
```bash
$ ./cgen
$ ./cgenf # Same as cgen, but format the output C file

$ ./cgen -s 10007 # specify seed
```

You can conduct mass-scale duipai (differential testing) with `./mdtest`

# Tweaks
`./cgen -h` and check `config.py`.

# TODO
* Python is too slow, switch to Rust.
* Multi-threading for mass-scale duipai
* Add feature switch so user can choose which features of C to incorporate
* Get rid of undefined behaviour e.g. `(a=5) + (a=6) - a`
  - Already `-Werror=overflow` etc but that is not enough

# Methodology
My approach is ad hoc, same as that of CSmith.
There can be some more principled approaches like grammar guided generation but I doubt their practicality.

The apprach is basically grammar driven DFS; the DFS functions are Stmt/Expr constructors.
DFS search state (declared variables etc) is stored in `GeneratorState` i.e. gs.
Constraints are scattered in ctors, gs, and `randexpr/randstmt`.

# Reference
* [csmith](github.com/csmith-project/csmith)

