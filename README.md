# Website (Forester)

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
This is here because forester outputs things into an `output/` directory, but we want to run it from the `docs/` directory (bc github).

Some commands [are here](cmds.md). 

Also the [10 min introduction on forester](https://www.forester-notes.org/0052/index.xml) and [some 2023 release notes](https://www.forester-notes.org/005P/index.xml).