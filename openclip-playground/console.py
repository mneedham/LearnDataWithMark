import llm
import glob
import base64
import hashlib
import chromadb
from rich import console
from iterm_utils import display_image

model = llm.get_embedding_model("clip")
c = console.Console()

with c.pager():
    c.out(model.embed("cute dog"))

image = 'images/DALL·E 2023-11-21 06.18.24 - a cartoon-style i.png'
display_image(image)

with c.pager(), open(image, 'rb') as image_file:
    c.out(model.embed(image_file.read()))

images = glob.glob("images/*.png")

embeddings = []
for image in images:
  with open(image, "rb") as image_file:
    embedding = model.embed(image_file.read())
    embeddings.append({
      "embedding": embedding,
      "filePath": image,
      "id": base64.b64encode(hashlib.sha256(image.encode()).digest()).decode()
    })


chroma_client = chromadb.PersistentClient(path="images.chromadb")
collection = chroma_client.create_collection(name="images")
collection.add(
    embeddings=[e["embedding"] for e in embeddings],
    metadatas=[{k: e[k] for k in ["filePath"]} for e in embeddings],
    ids=[e["id"] for e in embeddings],
)

query_embeddings = model.embed("cute dog")
collection.query(
    query_embeddings=[query_embeddings],
    n_results=3
)