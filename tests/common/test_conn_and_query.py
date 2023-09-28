import os
import unittest
from glob import glob
from string import Template

import pandas as pd

from notexport.common import CONST_IBOOK, SQLiteAdapter


class TestConnection(unittest.TestCase):
    def test_query(self):
        db_kw = os.path.join(
            CONST_IBOOK.DEFAULT_ROOT, CONST_IBOOK.DEFAULT_BKLIBRARY, "*.sqlite"
        )
        endpoint = glob(db_kw)[-1]
        sql_path = "sql/ibook_query_book_by_name.sql"
        with SQLiteAdapter(endpoint=endpoint) as conn, open(sql_path, "r") as fp:
            sql = fp.read()
            query = Template(sql).substitute(kw_title="Mindset")
            tb: pd.DataFrame = conn.query(query)
            self.assertGreater(tb.shape[0], 0)


if __name__ == "__main__":
    unittest.main()
