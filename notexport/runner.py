import os
from datetime import datetime
from glob import glob
from typing import List, Tuple, Union

import pandas as pd

from .common import CONST_COMM, CONST_IBOOK, CONST_VACABULARY, SQLiteAdapter, load_query
from .ibook import IBookNoteProcessor


def find_abs_db_path(folder) -> str:
    elems = glob(os.path.join(folder, "*.sqlite"))
    if not elems or len(elems) < 1:
        raise ValueError(f"Failed to find any sqlite file under {folder}")
    return sorted(elems)[-1]


def calculate_time_range_epoch(start_time, end_time) -> Tuple:
    # TODO: Fix timezone
    if not start_time:
        start_time = CONST_COMM.DEFAULT_START_TIME
    start_time = datetime.strptime(start_time, CONST_COMM.TIME_FORMAT).replace(
        tzinfo=CONST_COMM.DEFAULT_TIME_ZONE
    )

    if not end_time:
        end_time = datetime.now()
    if isinstance(end_time, str):
        end_time = datetime.strptime(end_time, CONST_COMM.TIME_FORMAT)
    end_time = end_time.replace(tzinfo=CONST_COMM.DEFAULT_TIME_ZONE)

    return (
        start_time.timestamp() - CONST_COMM.COCOA_UNIX_DELTA_SEC,
        end_time.timestamp() - CONST_COMM.COCOA_UNIX_DELTA_SEC,
    )


def fetch_notes(**kwargs) -> pd.DataFrame:
    book_db_path = find_abs_db_path(
        os.path.join(CONST_IBOOK.DEFAULT_ROOT, CONST_IBOOK.DEFAULT_BKLIBRARY)
    )
    annotation_db_path = find_abs_db_path(
        os.path.join(CONST_IBOOK.DEFAULT_ROOT, CONST_IBOOK.DEFAULT_ANNOTATION)
    )
    book_sql_path = "sql/ibook_query_book_by_name.sql"
    annotation_sql_path = "sql/ibook_query_annotation_by_id.sql"

    with SQLiteAdapter(book_db_path) as book_db, SQLiteAdapter(
        annotation_db_path
    ) as anno_db:
        tb_books: pd.DataFrame = book_db.query(load_query(book_sql_path, **kwargs))

        book_ids = tb_books[CONST_IBOOK.BOOK_ID_COL_IN_BKLIBRARY].to_list()
        print(
            f"Fetched {len(book_ids)} books from {book_db_path} under condition {kwargs}"
        )

        kwargs["asset_ids"] = ",".join(book_ids)
        kwargs["start_time"], kwargs["end_time"] = calculate_time_range_epoch(
            kwargs.get("after", None), kwargs.get("before", None)
        )
        tb_annotation: pd.DataFrame = anno_db.query(
            load_query(annotation_sql_path, **kwargs)
        )
        print(
            f"Fetched {len(tb_annotation)} annotations from {annotation_db_path} under condition {kwargs}"
        )

        all_notes = pd.merge(
            left=tb_books,
            right=tb_annotation,
            left_on=CONST_IBOOK.BOOK_ID_COL_IN_BKLIBRARY,
            right_on=CONST_IBOOK.BOOK_ID_COL_IN_ANNOTATION,
            how="inner",
            right_index=False,
        )
        return all_notes


def fetch_vocabulary(keys: List, vocabulary_name: str) -> pd.DataFrame:
    vocabulary_db_path = None
    if vocabulary_name.upper() == CONST_VACABULARY.COLLINS.name:
        vocabulary_db_path = CONST_VACABULARY.COLLINS
    elif vocabulary_name.upper() == CONST_VACABULARY.MERRIAM_WEBSTER.name:
        vocabulary_db_path = CONST_VACABULARY.MERRIAM_WEBSTER
    else:
        raise NotImplementedError(
            f"Vocabulary {vocabulary_name} is not supported, select from ['collins', 'merriam_webster]"
        )

    with SQLiteAdapter(vocabulary_db_path) as voc_conn:
        sql = load_query("sql/mdx_query_by_key.sql", target_words="','".join(keys))
        return voc_conn.query(sql)


def attach_word_explaination(src: Union[str, pd.DataFrame], voc_name):
    """
    Merge the vocabulary explanitions for highlighted notes

    Args:
        src (str, pd.DataFrame): notes dumped from ibook
        voc_name (str): vocabulary file name
        target_folder: saving path
    """
    ibook_processor = IBookNoteProcessor(data=src)

    words = ibook_processor.lemmatize().normalize().get_words(cleaned=True)
    vocabulary = fetch_vocabulary(words, voc_name)
    ibook_processor.merge_explanation_from_vocabulary(vocabulary)

    return ibook_processor.get_data()
