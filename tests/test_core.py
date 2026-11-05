import unittest
from tinysearch import SearchIndex, tokenize

class SearchTests(unittest.TestCase):
    def test_rank_and_update(self):
        index = SearchIndex()
        index.add("a", "python python search")
        index.add("b", "search")
        self.assertEqual(index.search("python")[0]["id"], "a")
        index.add("a", "new")
        self.assertEqual(index.search("python"), [])
        self.assertTrue(index.remove("a"))
        self.assertFalse(index.remove("a"))

    def test_and_or(self):
        index = SearchIndex()
        index.add("1", "red blue")
        index.add("2", "red")
        self.assertEqual([x["id"] for x in index.search("red blue", operator="and")], ["1"])
        self.assertEqual(len(index.search("red blue")), 2)

    def test_validation(self):
        index = SearchIndex()
        with self.assertRaises(ValueError):
            index.add("", "text")
        with self.assertRaises(ValueError):
            index.search("x", limit=0)
        with self.assertRaises(ValueError):
            index.search("x", operator="xor")
        self.assertEqual(tokenize("Hello, WORLD!"), ["hello", "world"])


    def test_unicode_and_stable_order(self):
        index = SearchIndex()
        index.add("z", "CAFÉ 東京")
        index.add("a", "café 東京")
        self.assertEqual([r["id"] for r in index.search("CAFÉ")], ["a", "z"])
        self.assertEqual(len(index.search("東京", operator="and")), 2)

    def test_empty_document_and_query(self):
        index = SearchIndex()
        index.add("empty", "")
        self.assertEqual(index.search(""), [])
        self.assertEqual(index.search("missing"), [])
        with self.assertRaises(TypeError):
            index.add("bad", None)
        with self.assertRaises(ValueError):
            index.search("x", limit=True)

if __name__ == "__main__":
    unittest.main()
