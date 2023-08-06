# y2j
A command line tool for translating YAML streams to JSON.


## Installation

```
pip install y2j
```


## Usage
`y2j` accepts YAML data and writes the equivalent JSON to STDOUT. The YAML may be read from a named file, or from STDIN.

#### Options
* `-c`, `--compressed`: Print with no superfluous whitespace.
* `-p`, `--pretty`: Pretty-print the JSON output


The following examples are based on the contents of `example.yml`:

```
---
  y2j:
    - Is easy to use
    - Is neat

```

#### Reading from a file

```
$ y2j -p example.yml

{
  "y2j": [
    "Is easy to use",
    "Is neat"
  ]
}
```

#### Reading from STDIN

```
$ cat example.yml | y2j -p

{
  "y2j": [
    "Is easy to use",
    "Is neat"
  ]
}
```
