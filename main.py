import os
from time import localtime, strftime, time

import click
import pandas as pd

from notexport import attach_word_explaination, fetch_notes
from notexport.common import CONST_COMM


def generate_target_folder(ctx, param, value):
    folder = CONST_COMM.DATA_FOLDER
    if value:
        folder = value if os.path.isdir(value) else os.path.dirname(value)
    try:
        date = strftime(CONST_COMM.TIME_FORMAT, localtime(time()))
        folder = os.path.join(folder, f"{ctx.params['title']}_{date}")
        if not os.path.exists(folder):
            os.makedirs(folder)
        return folder
    except ValueError:
        raise click.BadParameter(f"Parameter {param} is not legal")


@click.command()
@click.option("--title", required=True, help="Keywords in book title")
@click.option(
    "--output",
    type=click.UNPROCESSED,
    callback=generate_target_folder,
    default=None,
    help="Target folder for results, <data/title_timestamp> as default",
)
@click.option(
    "--after", default=None, help="[FILTER] timestamp AFTER which should be kept"
)
@click.option(
    "--before", default=None, help="[FILTER] timestamp BEFORE which should be kept"
)
@click.option(
    "--join_vocabulary",
    default=False,
    help="[TASK] whether to join word explainations from vocabulary",
)
@click.option("--vocabulary", default="collins")
def _main(title, output, after, before, join_vocabulary, vocabulary):
    target_notes: pd.DataFrame = fetch_notes(kw_title=title, before=before, after=after)
    target_notes.to_csv(os.path.join(output, "notes.csv"))

    if join_vocabulary:
        df_w, df_s = attach_word_explaination(target_notes, vocabulary)
        df_w.to_csv(os.path.join(output, "words.csv"), index=False)
        df_s.to_csv(os.path.join(output, "sentences.csv"), index=False)

        print(
            f"Dumped {df_w.shape[0]} words and {df_s.shape[0]} sentences under folder {output}"
        )


if __name__ == "__main__":
    _main()
