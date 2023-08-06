# Python benchmark library
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/penchmark.svg)](https://pypi.org/project/penchmark/)
![Python package](https://github.com/Ruzzz/penchmark/workflows/Python%20package/badge.svg?branch=master)
[![codecov](https://codecov.io/gh/Ruzzz/penchmark/branch/master/graph/badge.svg)](https://codecov.io/gh/Ruzzz/penchmark)

## Installation

```bash
pip install penchmark
pip install penchmark[charts]
```

## Example

#### Classes `Callee`, `InData`

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

#### Tuples

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

#### Auto generate names of callees

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

#### Markdown result

##### small-data

| callee_name   |   elapsed |   ratio |
|:--------------|----------:|--------:|
| nop           |    0.0050 |  1.0000 |
| mul           |    0.0080 |  1.5842 |

##### big-data

| callee_name   |   elapsed |   ratio |
|:--------------|----------:|--------:|
| nop           |    0.0000 |  1.0000 |
| mul           |    0.0001 |  1.7201 |

##### Summary

| callee_name   |   mean |   median |
|:--------------|-------:|---------:|
| nop           | 1.0000 |   1.0000 |
| mul           | 1.6521 |   1.6521 |

#### Console mode result

```python
...
benchmark_and_print((mul, nop), dataset, markdown=False)
```

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

#### Callee with exceptions

```python
from penchmark import benchmark_and_print

def callee_with_exceptions(x):
    if not x:
        raise Exception()

callees = (
    ('callee-with-exceptions', callee_with_exceptions),
    ('callee-without-exceptions', lambda x: None)
)
dataset = (
    ('valid-data', True, 10),
    ('invalid-data', False, 10),
)
benchmark_and_print(callees, dataset)
```

##### valid-data

| callee_name               |   elapsed |   ratio |
|:--------------------------|----------:|--------:|
| callee-without-exceptions |   0.00000 |       1 |
| callee-with-exceptions    |   0.00000 | 2.36735 |

##### invalid-data

| callee_name               |   elapsed |   ratio |
|:--------------------------|----------:|--------:|
| callee-without-exceptions |   0.00000 |       1 |
| callee-with-exceptions    |     ERROR |         |

##### Summary

| callee_name               |   mean |   median |
|:--------------------------|-------:|---------:|
| callee-without-exceptions |      1 |        1 |

#### Expected using InData

```python
from penchmark import benchmark_and_print, InData

def mul2_1(sequ): return [x * 2 for x in sequ]
def mul2_2(sequ): return [x + x for x in sequ]

dataset = (
    InData(name='small-data', data=(2, 1), count_of_call=100000, expected=[4, 2]),
    InData(name='big-data', data=(200, 10), count_of_call=1000, expected=[400, 20]),
    InData(name='skipped-data', data=(1, 1), count_of_call=0, expected=[2, 2])
)
benchmark_and_print((mul2_1, mul2_2), dataset)
```

#### Expected using tuples

```python
from penchmark import benchmark_and_print

def mul2_1(sequ): return [x * 2 for x in sequ]
def mul2_2(sequ): return [x + x for x in sequ]

dataset = (
    ('small-data', (2, 1), 100000, [4, 2]),
    ('big-data', (200, 10), 1000, [400, 20]),
    ('skipped-data', (1, 1), 0, [2, 2])
)
benchmark_and_print((mul2_1, mul2_2), dataset)
```

#### small-data

| callee_name   |   elapsed |   ratio |
|:--------------|----------:|--------:|
| mul2_2        |   0.02114 |       1 |
| mul2_1        |   0.02317 | 1.09603 |

#### big-data

| callee_name   |   elapsed |   ratio |
|:--------------|----------:|--------:|
| mul2_2        |   0.00021 |       1 |
| mul2_1        |   0.00022 | 1.01147 |

#### Summary

| callee_name   |    mean |   median |
|:--------------|--------:|---------:|
| mul2_2        | 1       |  1       |
| mul2_1        | 1.05375 |  1.05375 |
