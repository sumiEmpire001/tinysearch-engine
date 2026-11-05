import math
import re
from collections import Counter, defaultdict

def tokenize(text):
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return re.findall(r"[^\W_]+", text.casefold())

class SearchIndex:
    def __init__(self):
        self.docs = {}
        self.postings = defaultdict(dict)

    def add(self, key, text):
        if not isinstance(key, str) or not key:
            raise ValueError("nonempty string ID required")
        terms = Counter(tokenize(text))
        self.remove(key)
        self.docs[key] = (text, terms)
        for term, count in terms.items():
            self.postings[term][key] = count

    def remove(self, key):
        old = self.docs.pop(key, None)
        if old is None:
            return False
        for term in old[1]:
            del self.postings[term][key]
            if not self.postings[term]:
                del self.postings[term]
        return True

    def search(self, query, limit=10, operator="or"):
        if type(limit) is not int or limit < 1:
            raise ValueError("limit must be positive integer")
        if operator not in ("and", "or"):
            raise ValueError("operator must be and/or")
        terms = set(tokenize(query))
        if not terms or not self.docs:
            return []
        sets = [set(self.postings.get(term, {})) for term in terms]
        ids = set.intersection(*sets) if operator == "and" else set.union(*sets)
        n = len(self.docs)
        avg = sum(sum(counts.values()) for _, counts in self.docs.values()) / n or 1
        results = []
        for key in ids:
            text, counts = self.docs[key]
            length = sum(counts.values())
            score = 0.0
            for term in terms:
                tf = counts.get(term, 0)
                if tf:
                    df = len(self.postings[term])
                    idf = math.log(1 + (n - df + 0.5) / (df + 0.5))
                    score += idf * tf * 2.2 / (tf + 1.2 * (0.25 + 0.75 * length / avg))
            results.append({"id": key, "text": text, "score": round(score, 8)})
        return sorted(results, key=lambda item: (-item["score"], item["id"]))[:limit]
