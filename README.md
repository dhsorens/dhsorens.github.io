# Website (Forester)

This site is built with [forester](https://sr.ht/~jonsterling/forester/) **5.0**. To install it (requires OCaml ≥ 5.3.0 and opam):

```bash
    opam install forester.5.0
```

To compile and view (locally)

```bash
    ./view.sh
```

To make a new note:
```bash
    ./new.sh
```
this will automatically generate a new tree (?) and index it properly; you can transclude trees into each other from there.

To commit a change, run:
```bash
    ./commit.sh "my message here"
```
This is here because forester outputs things into an `output/` directory, but we want to serve it from the `docs/` directory (bc github). The build itself lives in `./build.sh`, which also:
- copies `assets/` into the output under their original paths (forester 5.0 only emits content-addressed copies), so link assets with absolute paths like `/docs/paper.pdf`;
- copies the root `CNAME` into the output;
- writes a redirect at each old `/<addr>.xml` URL, since forester 5.0 moved each tree to `/<addr>/`.

Some commands [are here](cmds.md).

Also the [forester documentation](https://www.forester-notes.org/index/).
