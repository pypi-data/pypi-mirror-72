from penchmark._defs import ByDataReport, Callee, InData, Report, ReportItem, Summary, SummaryItem
from penchmark._report import report_as_md_table
from penchmark._core import benchmark, NameGenerator


def benchmark_and_print(*args, floatfmt=None, markdown=True, **kwargs):
    print(report_as_md_table(*benchmark(*args, **kwargs), floatfmt=floatfmt, markdown=markdown))
