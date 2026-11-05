# TinySearch Engine

An in-memory inverted index with BM25-style ranking, document replacement/deletion and AND/OR queries. Python 3.10+; standard library only.

```bash
python -m unittest discover -s tests -v
```

```python
from tinysearch import SearchIndex
index = SearchIndex()
index.add("doc-1", "Python search search")
index.add("doc-2", "Python graphs")
print(index.search("search"))
print(index.search("python search", operator="and"))
```

IDs must be nonempty strings. Query terms are case-folded Unicode word tokens; punctuation is ignored. Results are ranked by a BM25-style score and tie-broken by ID. Empty queries return no results. No persistence, phrase matching, stemming, access controls or distributed indexing. This is an educational in-memory engine, not a production search service.

## Quality checks
GitHub Actions runs unit tests on Python 3.10, 3.12 and 3.13. CI results must be checked before declaring this repository verified.

MIT license; see LICENSE.
