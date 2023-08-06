# Python benchmark library
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python package](https://github.com/Ruzzz/penchmark/workflows/Python%20package/badge.svg?branch=master)
[![codecov](https://codecov.io/gh/Ruzzz/penchmark/branch/master/graph/badge.svg)](https://codecov.io/gh/Ruzzz/penchmark)

## Installation

```bash
pip install penchmark
pip install penchmark[charts]
```

## Example

```python
from penchmark import benchmark_and_print, Callee, InData

callees = (
    Callee(callee_name='mul', callee=lambda x: x[0] * x[1]),
    Callee(callee_name='nop', callee=lambda x: x)
)
dataset = (
    InData(name='small-data', data=(2, 1), count_of_call=100000),
    InData(name='big-data', data=(200, 10), count_of_call=1000),
    InData(name='skipped-data', data=(1, 1), count_of_call=0)
)
benchmark_and_print(callees, dataset)
```

or

```python
from penchmark import benchmark_and_print

callees = (
    ('mul', lambda x: x[0] * x[1]),
    ('nop', lambda x: x)
)
dataset = (
    ('small-data', (2, 1), 100000),
    ('big-data', (200, 10), 1000),
    ('skipped-data', (1, 1), 0)
)
benchmark_and_print(callees, dataset)
```

or

```python
from penchmark import benchmark_and_print

def mul(x): return x[0] * x[1]
def nop(x): return x

dataset = (
    ('small-data', (2, 1), 100000),
    ('big-data', (200, 10), 1000),
    ('skipped-data', (1, 1), 0)
)
benchmark_and_print((mul, nop), dataset)
```

### Markdown result

#### small-data

| callee_name   |   elapsed |   ratio |
|:--------------|----------:|--------:|
| nop           |    0.0050 |  1.0000 |
| mul           |    0.0080 |  1.5842 |

#### big-data

| callee_name   |   elapsed |   ratio |
|:--------------|----------:|--------:|
| nop           |    0.0000 |  1.0000 |
| mul           |    0.0001 |  1.7201 |

#### Summary

| callee_name   |   mean |   median |
|:--------------|-------:|---------:|
| nop           | 1.0000 |   1.0000 |
| mul           | 1.6521 |   1.6521 |

or

```python
...
benchmark_and_print((mul, nop), dataset, markdown=False)
```

### Result

```
SMALL-DATA

callee_name      elapsed    ratio
-------------  ---------  -------
nop               0.0050   1.0000
mul               0.0079   1.5944

BIG-DATA

callee_name      elapsed    ratio
-------------  ---------  -------
nop               0.0001   1.0000
mul               0.0001   1.7565

SUMMARY

callee_name      mean    median
-------------  ------  --------
nop            1.0000    1.0000
mul            1.6754    1.6754
```
