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
    report, summary = benchmark(callees, dataset, summary=False, verbose=False)
    assert summary is None

    # main
    report, summary = benchmark(callees, dataset, verbose=False)

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
                assert isinstance(report[data_name][item_index][float_attr], (int, float))
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

    summary = deepcopy(summary)
    # clear attrs
    for summary_item in summary:
        summary_item['callee_name'] = 'op'
        summary_item['mean'] = 0
        summary_item['median'] = 0

    # compare structure
    assert summary == [
        {'callee_name': 'op', 'mean': 0, 'median': 0},
        {'callee_name': 'op', 'mean': 0, 'median': 0}
    ]


def test_benchmark_callee_exceptions_and_expected():

    def callee_with_exceptions(sequ):
        ret = []
        for x in sequ:
            if not x:
                raise Exception()
            ret.append(x + x)
        return ret

    callees = (
        ('callee-with-exceptions', callee_with_exceptions),
        ('callee-without-exceptions', lambda sequ: [x + x for x in sequ])
    )
    dataset = (
        InData(name='valid-data', data=(1, 2, 3), count_of_call=10, expected=[2, 4, 6]),
        InData(name='invalid-data', data=(1, 0, 3), count_of_call=10, expected=[2, 0, 6]),
    )
    report, summary = benchmark(callees, dataset, verbose=False)
    report = deepcopy(report)

    # clear attrs
    reset_attrs = [
        ('valid-data', 0),
        ('valid-data', 1),
        ('invalid-data', 0)
    ]
    for data_name, item_index in reset_attrs:
        report[data_name][item_index]['callee_name'] = 'op'
        for float_attr in ['elapsed', 'ratio']:
            report[data_name][item_index][float_attr] = 0

    # compare structure
    assert report == {
        'valid-data': [
            {'callee_name': 'op', 'elapsed': 0, 'ratio': 0},
            {'callee_name': 'op', 'elapsed': 0, 'ratio': 0}
        ],
        'invalid-data': [
            {'callee_name': 'op', 'elapsed': 0, 'ratio': 0},
            {'callee_name': 'callee-with-exceptions'}
        ]
    }

    # compare structure
    assert deepcopy(summary) == [
        {'callee_name': 'callee-without-exceptions', 'mean': 1, 'median': 1}
    ]
