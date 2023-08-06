from pathlib import Path

# pylint: disable=import-error
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from penchmark._defs import ByDataReport, Report


def save_chart(data_report: ByDataReport, title: str, fname):
    plt.rcParams.update({'font.size': 8})
    plt.figure(figsize=(5, 3))

    df = pd.DataFrame(sorted(data_report, key=lambda x: x['callee_name']))
    ax = sns.barplot(x='callee_name', y='elapsed', palette='pastel', data=df)
    ax.set_title(title)
    ax.set_xlabel('')
    ax.set_ylabel('')
    Path(fname).parent.mkdir(parents=True, exist_ok=True)
    ax.figure.savefig(fname, dpi=100)
    plt.close(ax.figure)


def save_charts_and_get_markdown(report: Report, *,
                                 title_template: str = None,
                                 fname_template: str = None,
                                 link_template: str = None):
    if not title_template:
        title_template = '{data_name}'
    if not fname_template:
        fname_template = 'reports/charts/{data_name}.png'
    if not link_template:
        link_template = fname_template

    markdown = ''
    for data_name, data_report in report.items():
        title = title_template.format(data_name=data_name)
        fname = fname_template.format(data_name=data_name)
        save_chart(data_report, title, fname)

        link = link_template.format(data_name=data_name)
        markdown += f'![{title}]({link})\n'
    return markdown
