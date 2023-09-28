import os
import sqlite3

import click

from notexport.common import load_query
from notexport.ext.mdxanalysis.readmdict import MDX


class MDictConverter:
    def __init__(self, mdict_path: str) -> None:
        self._mdx_path = mdict_path
        self._mdx: MDX = MDX(mdict_path)

    def dump_to_sqlite(self, db_file_path=None, override=True):
        if not db_file_path:
            mdx_base_name = os.path.splitext(os.path.basename(self._mdx_path))[0]
            db_file_path = os.path.join(
                os.path.dirname(self._mdx_path), f"{mdx_base_name}.sqlite.db"
            )
        if override:
            if os.path.exists(db_file_path):
                os.remove(db_file_path)

        with sqlite3.connect(db_file_path) as conn:
            cursor = conn.cursor()

            # Create new TABLE
            cursor.execute(load_query("sql/mdx_create_db.sql"))

            # Load data into TABLE
            contents = [(k.decode(), v.decode()) for k, v in self._mdx.items()]
            cursor.executemany("INSERT INTO MDX_DICT VALUES (?,?)", contents)

            # Create INDEX
            cursor.execute(load_query("sql/mdx_create_index.sql"))

            conn.commit()

        print(
            f"Generated new sqlite database file to {db_file_path}, override [{override}]"
        )


@click.command()
@click.option("--mdx_path", help="Absolute path for mdx dict file.")
@click.option("--sqlite_db_path", default=None, help="Absolute path for sqlite db")
@click.option("--override", default=False)
def _mdx_to_sqlite(mdx_path, sqlite_db_path, override):
    converter = MDictConverter(mdx_path)
    converter.dump_to_sqlite(db_file_path=sqlite_db_path, override=override)


if __name__ == "__main__":
    _mdx_to_sqlite()
