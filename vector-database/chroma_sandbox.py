import chromadb
import pprint
import uuid
import chromadb.utils.embedding_functions as ef

client = chromadb.PersistentClient(path="vector.db")

collection = client.create_collection(name="bitsOfText")


documents = [
    "Cristiano Ronaldo plays for Portugal"
]

for document in documents:
    collection.add(
        documents=[document],
        metadatas=[{"source": "MarksBrain"}],
        ids=[f"id-{uuid.uuid4()}"]
    )

results = collection.query(
    query_texts=["Clothing"],
    n_results=3
)
pprint.pprint(results)
