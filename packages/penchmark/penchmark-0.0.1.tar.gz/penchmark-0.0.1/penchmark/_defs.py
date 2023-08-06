from typing import Any, Callable, Dict, List, NamedTuple, Union, Tuple

from penchmark._helpers import AutoPropertiesDict


CallableAny = Callable[[Any], Any]


class Callee(NamedTuple):
    callee_name: str
    callee: CallableAny


class InData(NamedTuple):
    name: str  # name of data ('data grouped' benchmark name)
    data: Any
    count_of_call: int


AnyCallee = Union[CallableAny, Callee, Tuple[str, CallableAny]]
AnyInData = Union[InData, Tuple[str, Any, int]]


class ReportItem(AutoPropertiesDict):
    callee_name: str
    elapsed: float
    ratio: float


class SummaryItem(AutoPropertiesDict):
    callee_name: str
    mean: float
    median: float


ByDataReport = List[ReportItem]
Report = Dict[str, ByDataReport]  # [name of data] = ByDataReport
Summary = List[SummaryItem]
