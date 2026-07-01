import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading FAISS index...")
index = faiss.read_index("vector_db/shl.index")

with open("vector_db/documents.pkl", "rb") as f:
    assessments = pickle.load(f)


def search(query, k=5):
    """
    Search the FAISS index and return the top-k matching assessments.
    """

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


# -------------------------------------------------------
# Run this block ONLY when retriever.py is executed directly
# -------------------------------------------------------

if __name__ == "__main__":

    while True:

        query = input("\nEnter hiring requirement (or 'exit'): ")

        if query.lower() == "exit":
            break

        results = search(query)

        print("\nTop Recommendations\n")

        for i, item in enumerate(results, start=1):

            print("=" * 60)
            print(f"{i}. {item['name']}")
            print(f"Score      : {item['score']:.4f}")
            print(f"Duration   : {item.get('duration', '-')}")
            print(f"Remote     : {item.get('remote', '-')}")
            print(f"Adaptive   : {item.get('adaptive', '-')}")
            print(item.get("description", ""))
            print(item["link"])