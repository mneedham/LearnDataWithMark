```bash
poetry add llm
poetry run llm install llm-clip
poetry run llm embed-multi photos --files images/ '*.png' --binary -m clip
poetry run llm similar photos -c 'parrot'
```

How do you check that it actually embedded anything?

```python
import llm
from rich import console

c = console.Console()

model = llm.get_embedding_model("clip")

with c.pager():
    c.out(model.embed("bunny"))

model.supports_binary

import glob
import base64
import hashlib

embeddings = []
for image in glob.glob("images/*.png"):
    with open(image, "rb") as image_file:
        embedding = model.embed(image_file.read())
        embeddings.append({
            "embedding": embedding,
            "filePath": image,
            "id": base64.b64encode(hashlib.sha256(image.encode()).digest()).decode()
        })
```

```python
import chromadb
chroma_client = chromadb.PersistentClient(path="images.chromadb")

collection = chroma_client.create_collection(name="images")

collection.add(
    embeddings=[e["embedding"] for e in embeddings],
    metadatas=[{k: e[k] for k in ["filePath"]} for e in embeddings],
    ids=[e["id"] for e in embeddings],
)

query_embeddings = model.embed("bunny")
collection.query(
    query_embeddings=[query_embeddings],
    n_results=3
)
```

In this video, we'll learn how to build an image search engine with Streamlit and the CLIP embedding library, guided by insights from Simon Willison's blog. We demonstrate embedding text and images using CLIP, showing how to process and embed multiple images for a database. We then explore adding these images with metadata into ChromaDB and query the database with examples like a "cute dog" and a "green jumper".

We then build a UI using Streamlit app, with features for inputting search terms or uploading images, and displaying results. Practical tests show the effectiveness and limitations of the search engine, highlighting areas for potential improvement with future embedding algorithms.

#Streamlit #ImageSearch #MachineLearning #CLIP #Python #DataScience #AI

Code used on the terminal - https://github.com/mneedham/LearnDataWithMark/blob/main/openclip-playground/console.py
Streamlit app - https://github.com/mneedham/LearnDataWithMark/blob/main/openclip-playground/app.py
Simon Willison's blog - https://simonwillison.net/2023/Sep/12/llm-clip-and-chat/
