import os
from time import localtime, strftime, time

import click

from notexport import fetch_notes
from notexport.common import CONST_COMM


def generate_file_path(ctx, param, value):
    if str(value).endswith(".csv"):
        return value

    folder = CONST_COMM.DATA_FOLDER
    if value:
        folder = value if os.path.isdir(value) else os.path.dirname(value)
    try:
        date = strftime(CONST_COMM.TIME_FORMAT, localtime(time()))
        return os.path.join(folder, f"{ctx.params['title']}_{date}.csv")
    except ValueError:
        raise click.BadParameter(f"Parameter {param} is not legal")


@click.command()
@click.option("--title", required=True, help="Keywords in book title")
@click.option(
    "--output",
    type=click.UNPROCESSED,
    callback=generate_file_path,
    default=None,
    help="Target path for result, <data/title_timestamp.csv> as default",
)
@click.option(
    "--after", default=None, help="[FILTER] timestamp after which should be kept"
)
@click.option(
    "--before", default=None, help="[FILTER] timestamp before which should be kept"
)
def _main(title, output, after, before):
    result = fetch_notes(kw_title=title)
    result.to_csv(output)


if __name__ == "__main__":
    _main()
