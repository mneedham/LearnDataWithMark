import llama_cpp
from qdrant_client import QdrantClient
from rich.console import Console

c = Console()

embedding_llm = llama_cpp.Llama(
  model_path="./models/mxbai-embed-large-v1-f16.gguf",
  embedding=True,
  verbose=False
)

client = QdrantClient(path="embeddings")


# Search

search_query = "What did they say about Claude?"
query_vector = embedding_llm.create_embedding(search_query)['data'][0]['embedding']
search_result = client.search(
  collection_name="podcast",
  query_vector=query_vector,
  limit=5
)

c.print(search_result)

template = """You are a helpful assistant who answers questions using only the provided context.
If you don't know the answer, simply state that you don't know.

{context}

Question: {question}"""

llm = llama_cpp.Llama(
  model_path="./models/Llama-3-Instruct-8B-SPPO-Iter3-Q4_K_M.gguf",
  verbose=False
)

stream = llm.create_chat_completion(
    messages = [
      {"role": "user", "content": template.format(
        context = "\n\n".join([row.payload['text'] for row in search_result]),
        question = search_query      
      )}
    ],
    stream=True
)

for chunk in stream:
  c.print(chunk['choices'][0]['delta'].get('content', ''), end='')