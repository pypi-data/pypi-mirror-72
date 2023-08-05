# MatchPattern

An integrated glob and regex pattern matcher, with file and folder scan capabilities.

# TL;DR

```python
from match_pattern import Pattern

# with glob
assert Pattern("*ab").test("this is a long text that ends with ab") is True

# with regex
assert Pattern("re::^.*ab$").test("this is a long text that ends with ab") is True

# multiple glob (or)
assert Pattern("*ab|*kd").test("this is a long text that ends with kd") is True

# multiple types (or)
assert Pattern(["*ab", "*cd", "re::^.*ef$", Pattern("*gh")]).test("this is a long text that ends with gh") is True


# replace
assert Pattern("ab", is_full_match=False).replace("cd", "abcd") == "cdcd"

# format
assert Pattern.format("""{[msg]}""", custom_start_pattern="{[", custom_end_pattern="]}", msg="ok") == "ok"
```

# Symbols

### Globs
1. `|` - Sperate glob patterns
1. `*` - Match multiple chars (any)
1. `?` - Match single char (any)

### Regex
A regex pattern must start with `re::`, anything after that will not be modified, i.e.
```python
"re::^.my[:].*$" -> r"^.my[:].*$"
```

# Scan Path

Allows for scanning folders and files to match a pattern. Will always do a recursive scan. Example:

```python
import os
from match_pattern import Pattern

# Find all test files in the current folder and subfolders.
pattern = Pattern("*_test.py")
src_path = os.path.abspath(os.path.dirname(__file__))

test_files = pattern.scan_path(src_path)
```

# Available methods

1. [match] - Return the matched pattern results.
1. [test] - Boolean, test if the pattern exists.
1. [replace] - Replace a matched pattern, if its a partial match please notice `is_full_match=False`
1. [find_all] - Returns all the matched results in an array.
1. [format] - Format with custom start and end patterns (can be regex)
1. [scan_path] - See below.

# Install

```shell
pip install match_pattern
```

## From the git repo directly

To install from master branch,

```shell
pip install git+https://github.com/LamaAni/MatchPattern.git@master
```

To install from a release (tag)

```shell
pip install git+https://github.com/LamaAni/MatchPattern.git@[tag]
```

# Contribution

Feel free to ping me in issues or directly on LinkedIn to contribute.

# Licence

Copyright ©
`Zav Shotan` and other [contributors](https://github.com/LamaAni/postgres-xl-helm/graphs/contributors).
It is free software, released under the MIT licence, and may be redistributed under the terms specified in `LICENSE`.
