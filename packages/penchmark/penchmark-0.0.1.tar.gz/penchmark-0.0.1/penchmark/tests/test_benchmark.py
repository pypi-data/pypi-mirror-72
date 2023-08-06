from io import StringIO
from contextlib import redirect_stdout
from copy import deepcopy

import pytest

from penchmark import benchmark, Callee, InData


@pytest.mark.parametrize(
    'callees, dataset',
    [
        (
            # callees
            (
                Callee('mul', lambda x: x[0] * x[1]),
                Callee('nop', lambda x: x)
            ),
            # dataset
            (
                InData('small-data', (2, 1), 100),
                InData('big-data', (200, 10), 10),
                InData('skipped-data', (1, 1), 0)
            )
        ),
        (
            # callees
            (
                ('mul', lambda x: x[0] * x[1]),
                ('nop', lambda x: x)
            ),
            # dataset
            (
                ('small-data', (2, 1), 1000),
                ('big-data', (200, 10), 10),
                ('skipped-data', (1, 1), 0)
            )
        )
    ]
)
def test_benchmark(callees, dataset):
    # verbose
    with StringIO() as f:
        with redirect_stdout(f):
            benchmark(callees, dataset, verbose=False)
            assert f.getvalue() == ''
            benchmark(callees, dataset, verbose=True)
            assert len(f.getvalue()) > 0

    # summary
    report, summary = benchmark(callees, dataset, summary=False)
    assert summary is None

    # main
    report, summary = benchmark(callees, dataset)
    assert summary is not None

    report = deepcopy(report)
    assert len(report['small-data']) == 2
    assert len(report['big-data']) == 2
    assert 'skipped-data' not in report

    # float attrs
    for data_name in ['small-data', 'big-data']:
        for item_index in [0, 1]:
            callee_name = report[data_name][item_index]['callee_name']
            assert callee_name in ('nop', 'mul')

            for float_attr in ['elapsed', 'ratio']:
                assert isinstance(report[data_name][item_index][float_attr], float)
                assert report[data_name][item_index][float_attr] > 0

        assert report[data_name][0]['ratio'] == 1  # first ratio == 1
        assert report[data_name][0]['elapsed'] < report[data_name][1]['elapsed']
        assert report[data_name][0]['ratio'] < report[data_name][1]['ratio']

    # clear attrs
    for data_name in ['small-data', 'big-data']:
        for item_index in [0, 1]:
            report[data_name][item_index]['callee_name'] = 'op'
            for float_attr in ['elapsed', 'ratio']:
                report[data_name][item_index][float_attr] = 0

    # compare structure
    assert report == {
        'small-data': [
            {'callee_name': 'op', 'elapsed': 0, 'ratio': 0},
            {'callee_name': 'op', 'elapsed': 0, 'ratio': 0}
        ],
        'big-data': [
            {'callee_name': 'op', 'elapsed': 0, 'ratio': 0},
            {'callee_name': 'op', 'elapsed': 0, 'ratio': 0}
        ]
    }
