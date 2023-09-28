import unittest

from notexport import fetch_notes
from notexport.common import load_query


class RunnerTest(unittest.TestCase):
    def test_load_query(self):
        query_path = "sql/ibook_query_book_by_name.sql"
        query = load_query(query_path, kw_title="Tomorrow is another day")
        self.assertIn("Tomorrow is", query)

    def test_query_notes(self):
        kwargs = {"kw_title": "Growth Mindset"}
        result = fetch_notes(**kwargs)
        self.assertGreater(result.shape[0], 1)


if __name__ == "__main__":
    unittest.main()
