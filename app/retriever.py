import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

_model = None
_index = None
_assessments = None


def _load():
    global _model, _index, _assessments

    if _model is None:
        print("Loading embedding model...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")

    if _index is None:
        print("Loading FAISS index...")
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        index_path = os.path.join(base, "vector_db", "shl.index")

        _index = faiss.read_index(index_path)

    if _assessments is None:
        print("Loading assessment database...")

        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        docs_path = os.path.join(base, "vector_db", "documents.pkl")

        with open(docs_path, "rb") as f:
            _assessments = pickle.load(f)


def search(query, k=5):

    _load()

    embedding = _model.encode(
        [query],
        convert_to_numpy=True
    ).astype(np.float32)

    distances, indices = _index.search(embedding, k)

    results = []

    for score, idx in zip(distances[0], indices[0]):

        if idx == -1:
            continue

        item = _assessments[idx].copy()

        item["score"] = float(score)

        results.append(item)

    return results


if __name__ == "__main__":

    while True:

        q = input("Query: ")

        if q.lower() == "exit":
            break

        res = search(q)

        for r in res:
            print(r["name"], r["score"])