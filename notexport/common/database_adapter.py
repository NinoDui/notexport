import sqlite3

import pandas as pd


class SQLiteAdapter:
    def __init__(self, endpoint, timeout=120):
        self._endpoint = endpoint
        self._timeout = timeout
        self._conn = None

    def __enter__(self):
        self._conn = sqlite3.connect(self._endpoint, timeout=self._timeout)
        self._conn.text_factory = lambda x: str(x, "utf8")
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self._conn:
            self._conn.close()
            if exc_type or exc_value or exc_tb:
                print(exc_type, exc_value, exc_tb, sep="\n")
        else:
            print(f"No connection established with {self._endpoint}")

    def query(self, sql) -> pd.DataFrame:
        return pd.read_sql_query(sql, self._conn)
