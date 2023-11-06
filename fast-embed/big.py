import jsonlines
with jsonlines.open("data/documents.json") as documents_file:
    documents = [row for row in documents_file]

from fastembed.embedding import FlagEmbedding as Embedding
model = Embedding(model_name="BAAI/bge-base-en-v1.5")

sentences = [s for doc in documents for s in doc['body']]

import time



start = time.time()
print(len(list(model.passage_embed(sentences))))
end = time.time()
print(f"{end - start} seconds")

start = time.time()
print(f"{'Documents embedded:':<20} {len(list(model.passage_embed(sentences[:10], batch_size=100)))}")
end = time.time()
print(f"{'Time taken:':<20} {end - start:.2f} seconds")



len()