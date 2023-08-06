import re
import statistics
import sys
from collections import defaultdict
from sys import getsizeof
from timeit import default_timer
from types import BuiltinFunctionType, FunctionType, MethodType
from typing import Any, Dict, Iterable, Optional, Tuple, Union

from penchmark._defs import (
    AnyCallee,
    AnyInData,
    ByDataReport,
    CallableAny,
    Report,
    ReportItem,
    Summary,
    SummaryItem,
)


class Estimator:

    def __call__(self,
                 callee: CallableAny,
                 data: Any,
                 count_of_call: int,
                 expected: Any = None) -> float:
        with Estimator.Elapsed() as elapsed:
            for _ in range(count_of_call):
                ret = callee(data)
                if expected is not None:
                    assert ret == expected
        return elapsed()

    class Elapsed:
        __slots__ = '_start', 'dx'

        FLOAT_FMT = '.3f'

        def __init__(self):
            self._start = 0
            self.dx = 0

        def __enter__(self):
            self._start = default_timer()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.dx = default_timer() - self._start

        def __call__(self, fmt=None) -> Union[float, str]:
            return self.dx if fmt is None else format(self.dx, fmt)


class ByDataSummary:

    def __init__(self):
        self.by_data_ratios = defaultdict(list)
        self._with_errors = set()

    def __call__(self, by_data_report: ByDataReport):
        for x in by_data_report:
            if x.callee_name not in self._with_errors:
                if x.valid:
                    self.by_data_ratios[x.callee_name].append(x.ratio)
                else:
                    self._with_errors.add(x.callee_name)
                    if x.callee_name in self.by_data_ratios:
                        del self.by_data_ratios[x.callee_name]

    def calc_summary(self) -> Summary:
        ret = []
        for callee_name, ratios in self.by_data_ratios.items():
            ret.append(SummaryItem(
                callee_name=callee_name,
                mean=statistics.mean(ratios),
                median=statistics.median(ratios)
            ))
        ret.sort(key=lambda x: x.median)
        return ret


class NameGenerator:

    def __init__(self, module_as_prefix=True):
        self.module_as_prefix = module_as_prefix
        self._name_counters = defaultdict(int)
        self._cache = {}  # type: Dict[object, str]

    def __call__(self, obj: CallableAny):
        ret = self._cache.get(obj, None)
        if ret is not None:
            return ret

        ret = self.scan_name(obj)
        if not ret:
            ret = 'callable'

        if ret in self._name_counters:
            count = self._name_counters[ret] + 1
            ret = ret + '-' + str(count)
            self._name_counters[ret] = count
        else:
            self._name_counters[ret] = 1

        self._cache[obj] = ret
        return ret

    _REGEXS = [
        re.compile('<bound method (.+) of <.*>>'),
        re.compile('<function (.+) at .*'),
        re.compile('<built-in function (.+)>'),
    ]

    @classmethod
    def scan_name(cls, x: object):
        ret = None
        if isinstance(x, (BuiltinFunctionType, FunctionType, MethodType)):
            ret = str(x)
            for regex in cls._REGEXS:
                m = regex.match(ret)
                if m:
                    ret = m[1]
                    break
            if '<lambda>' in ret:
                ret = 'lambda'
            if '<locals>.' in ret:
                ret = ret[ret.find('<locals>.') + 9:]

        elif hasattr(x, '__name__'):
            ret = x.__name__  # type: ignore

        if not ret:
            # special cases
            # - functools.partial
            s = repr(x)
            if s.startswith('functools'):
                ret = s[:s.find('(')]

        if not ret and hasattr(x, '__class__'):
            ret = x.__class__.__name__  # type: ignore

        if ret and hasattr(x, '__module__') and x.__module__ and x.__module__ != '__main__':
            ret = x.__module__ + '.' + ret

        return ret


def benchmark(callees: Iterable[AnyCallee],
              dataset: Iterable[AnyInData],
              *,
              count_factor=1.0,
              estimator=None,
              summary=None,
              name_generator=None,
              verbose=True) -> Tuple[Report, Optional[Union[Summary, Any]]]:
    """
    :param callees:
    :param dataset:
    :param count_factor:
    :param estimator: Default is Estimator()
    :param summary: None, False or summary object, default is ByDataSummary()
    :param name_generator:
    :param verbose:
    :return:
    """

    # pylint: disable=too-many-branches, too-many-arguments, too-many-locals
    if not estimator:
        estimator = Estimator()
    if summary is None:
        summary = ByDataSummary()
    if not name_generator:
        name_generator = NameGenerator()
    ret = {}

    for data_name, data, count_of_call, *data_expected in dataset:
        expected = data_expected[0] if data_expected else None
        count_of_call = round(count_of_call * count_factor)
        if count_of_call <= 0:
            continue
        if verbose:
            print(data_name, 'count of call:', count_of_call, 'size of data:', getsizeof(data))

        group = []
        for callee_data in callees:
            if not callable(callee_data):
                callee_name, callee = callee_data
            else:
                callee_name, callee = name_generator(callee_data), callee_data

            if verbose:
                print(' -', callee_name)

            try:
                elapsed = estimator(callee, data, count_of_call, expected)
                ri = ReportItem(callee_name=callee_name, elapsed=elapsed)
            except Exception:  # pylint: disable=broad-except
                ri = ReportItem(callee_name=callee_name)
            group.append(ri)

        group.sort(key=lambda x: x.elapsed if x.valid else sys.maxsize)
        first = group[0]
        if first.valid:
            for item in group:
                if item == first:
                    item.ratio = 1.0
                elif item.valid:
                    item.ratio = item.elapsed / first.elapsed

        if summary:
            summary(group)
        ret[data_name] = group

    if verbose:
        print()

    return ret, summary.calc_summary() if summary else None
