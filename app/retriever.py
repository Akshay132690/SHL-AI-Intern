import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

model = None
index = None
assessments = None


def load_resources():
    global model, index, assessments

    if model is None:
        print("Loading embedding model...")
        model = SentenceTransformer("all-MiniLM-L6-v2")

    if index is None:
        print("Loading FAISS index...")
        index = faiss.read_index("vector_db/shl.index")

    if assessments is None:
        print("Loading assessment database...")
        with open("vector_db/documents.pkl", "rb") as f:
            assessments = pickle.load(f)


def search(query, k=5):
    load_resources()

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    ).astype(np.float32)

    distances, indices = index.search(query_embedding, k)

    results = []

    for score, idx in zip(distances[0], indices[0]):

        if idx == -1:
            continue

        item = assessments[idx].copy()
        item["score"] = float(score)

        results.append(item)

    return results


if __name__ == "__main__":

    while True:

        query = input("Query: ")

        if query.lower() == "exit":
            break

        results = search(query)

        for r in results:
            print(r["name"])