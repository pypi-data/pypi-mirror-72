from typing import Any

from tabulate import tabulate

from penchmark._defs import Report


def report_as_md_table(report: Report,
                       summary: Any = None,
                       floatfmt=None,
                       markdown=True,
                       **kwargs):
    if not floatfmt:
        floatfmt = '.5f'
    tablefmt = 'pipe' if markdown else 'simple'
    content = ''

    for data_name, group in report.items():
        if markdown:
            content += f'#### {data_name}\n\n'
        else:
            content += f'{data_name.upper()}\n\n'
        content += tabulate(
            group,
            headers='keys',
            tablefmt=tablefmt,
            floatfmt=('g', floatfmt, 'g'),
            missingval=('', 'ERROR', ''),
            colalign=('left', 'right', 'right'),
            **kwargs
        )
        content += '\n\n'

    if summary:
        if markdown:
            content += '#### Summary\n\n'
        else:
            content += 'SUMMARY\n\n'
        content += tabulate(summary, headers='keys', tablefmt=tablefmt, **kwargs)
        content += '\n\n'

    return content
