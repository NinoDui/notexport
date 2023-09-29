import os
import random
from datetime import datetime
from typing import Union

import click
import pandas as pd
from genanki import Deck, Model, Note, Package

from notexport.common import CONST_COMM


def new_id():
    return random.randrange(1 << 30, 1 << 31)


word_model = Model(
    model_id=new_id(),
    name="Word Learning",
    fields=[
        {"name": "word"},
        {"name": "meaning"},
        {"name": "sentence"},
    ],
    templates=[
        {
            "name": "Word Card",
            "qfmt": '{{word}}<hr id="example">{{sentence}}',
            "afmt": '{{FrontSide}}<hr id="answer">{{meaning}}',
        },
    ],
)


def pack(data: Union[str, pd.DataFrame], output_folder=None):
    if not output_folder:
        output_folder = (
            os.path.dirname(data) if isinstance(data, str) else CONST_COMM.DATA_FOLDER
        )

    if isinstance(data, str):
        data = pd.read_csv(data)
    # Cover case that word is not matched in vocabulary, such that the meaning is NaN
    data.fillna(value={"meaning": ""}, inplace=True)

    timestamp = datetime.strftime(datetime.now(), CONST_COMM.TIME_FORMAT)
    for title, book_notes in data.groupby("Title"):
        deck_name = f"Reading::{title}::{timestamp}"
        deck = Deck(deck_id=new_id(), name=deck_name)

        for idx, row in book_notes.iterrows():
            deck.add_note(
                Note(
                    model=word_model,
                    fields=[row["CleanedWord"], row["meaning"], row["BroaderText"]],
                )
            )

        deck_path = os.path.join(output_folder, f"{title}-{timestamp}.apkg")
        Package(deck).write_to_file(deck_path)
        print(f"Transmited {book_notes.shape[0]} words to {deck_path}")


@click.command()
@click.option("--data_path", help="Data Path (.csv)")
@click.option("--output_folder", help="Output Folder")
def _main(data_path, output_folder):
    pack(data_path, output_folder)


if __name__ == "__main__":
    _main()
