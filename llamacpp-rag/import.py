import uuid

import jsonlines
import time
import llama_cpp

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from itertools import islice
from langchain_core.documents import Document
from dataclasses import dataclass
from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils import chunk

file = "data/936d21b9.mp3-openai.json"


with jsonlines.open(file) as reader:
    documents = [row['text'] for row in reader]

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
    length_function=len,
    is_separator_regex=False,
)

documents = text_splitter.create_documents(documents)
print(len(documents))   

llm = llama_cpp.Llama(
  model_path="./models/mxbai-embed-large-v1-f16.gguf", 
  embedding=True, 
  verbose=False
)

batch_size = 100
documents_embeddings = []
batches = list(chunk(documents, batch_size))
start = time.time()
for batch in batches:
  embeddings = llm.create_embedding([item.page_content for item in batch])
  documents_embeddings.extend(
    [ 
      (document, embeddings['embedding'])  
      for document, embeddings in zip(batch, embeddings['data'])
    ]
  )
end = time.time()
char_per_second = len(''.join([item.page_content for item in documents])) / (end-start)
print(f"Time taken: {end-start:.2f} seconds / {char_per_second:,.2f} characters per second")

# Init client and create collection

client = QdrantClient(path="embeddings")

client.create_collection(
    collection_name="podcast",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
)

# Store documemts

points = [
  PointStruct(
    id = str(uuid.uuid4()),
    vector = embeddings,
    payload = {
      "text": doc.page_content
    }
  )
  for doc, embeddings in documents_embeddings
]

operation_info = client.upsert(
    collection_name="podcast",
    wait=True,
    points=points
)
