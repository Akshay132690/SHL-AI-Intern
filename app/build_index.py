import json
import faiss
import pickle
import numpy as np

from sentence_transformers import SentenceTransformer

print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

with open("data/shl_product_catalog.json", "r", encoding="utf-8") as f:
    data = json.load(f)

documents = []

for item in data:

    doc = f"""
Assessment Name: {item.get("name","")}

Description:
{item.get("description","")}

Category:
{", ".join(item.get("keys",[]))}

Suitable For:
{", ".join(item.get("job_levels",[]))}

Languages:
{", ".join(item.get("languages",[]))}

Duration:
{item.get("duration","")}

Remote Testing:
{item.get("remote","")}

Adaptive:
{item.get("adaptive","")}
"""

    documents.append(doc.strip())

print("Generating embeddings...")

embeddings = model.encode(
    documents,
    convert_to_numpy=True,
    show_progress_bar=True
)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings))

faiss.write_index(index, "vector_db/shl.index")

with open("vector_db/documents.pkl", "wb") as f:
    pickle.dump(data, f)

print("\nDone!")
print("Vectors:", index.ntotal)