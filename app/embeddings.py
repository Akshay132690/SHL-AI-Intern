import json

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

Catalog URL:
{item.get("link","")}
"""

    documents.append(doc.strip())

print("Documents created:", len(documents))

print("\n======================\n")

print(documents[0])