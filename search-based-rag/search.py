from openai import OpenAI
from rich.console import Console

import duckdb
import time
import json
from gliner import GLiNER

c = Console()

con = duckdb.connect("podcasts.duckdb")

model = GLiNER.from_pretrained("knowledgator/gliner-multitask-large-v0.5")
def extract_search_terms(question):
  prompt = """Find keywords or entities in this text:\n"""
  input_ = prompt+question
  labels = ["match", "entity"]
  return [entry['text'] for entry in model.predict_entities(input_, labels)]


def query_store(search_query, limit=3):
  return con.sql("""
  SELECT *, fts_main_podcast_transcript.match_bm25(
          id,
          $searchTerm
      ) AS score
  FROM podcast_transcript
  WHERE score IS NOT NULL
  ORDER BY score DESC
  LIMIT $limit
  """, params={"searchTerm": search_query, "limit": limit})


def generate_answer(search_query, search_result):
  template = """You are a helpful assistant who answers questions 
  using only the provided subset of a podcast transcript.
  If you don't know the answer, simply state that you don't know.
  {context}
  Question: {question}"""

  stream = llm.chat.completions.create(
    model = "llama3",
    messages = [
      {"role": "user", "content": template.format(
        context = "\n\n".join([row[0] for row in search_result.fetchall()]),
        question = search_query      
      )}
    ],
    stream=True
  )
  for chunk in stream:
    content = chunk.choices[0].delta.content
    yield content if content else ""

llm = OpenAI(
  base_url="http://localhost:8080/v1",
  api_key="llama-cpp"
)

search_query = "What did they say about Claude Sonnet"
search_result = query_store(search_query)

start = time.time()
stream = generate_answer(search_query, search_result)
for index, chunk in enumerate(stream):
  if index == 0:
    first_token = time.time()
  c.print(chunk, end='')
end = time.time()
c.print(f"\nTime to first token: {first_token-start:.2f} seconds", style="yellow")
c.print(f"Total Time: {end-start:.2f} seconds", style="yellow")


question = "What did they say about Claude Sonnet"
search_query = " OR ".join(extract_search_terms(question))
search_result = query_store(search_query)
stream = generate_answer(question, search_result)
for index, chunk in enumerate(stream):
  c.print(chunk, end='')