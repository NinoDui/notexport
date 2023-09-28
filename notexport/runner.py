import os
from glob import glob
from string import Template

import pandas as pd

from .common import CONST_IBOOK, SQLiteAdapter, load_query


def find_abs_db_path(folder) -> str:
    elems = glob(os.path.join(folder, "*.sqlite"))
    if not elems or len(elems) < 1:
        raise ValueError(f"Failed to find any sqlite file under {folder}")
    return sorted(elems)[-1]


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
