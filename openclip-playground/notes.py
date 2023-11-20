#poetry add llm
#poetry run llm install llm-clip
#poetry run llm embed-multi photos --files images/ '*.png' --binary -m clip
#poetry run llm similar photos -c 'parrot'

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