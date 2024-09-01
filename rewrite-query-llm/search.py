import duckdb
from openai import OpenAI

class Search:
  def __init__(self, con):
    self.con = con
    self.local_llm = OpenAI(base_url="http://localhost:8000/v1")


  def vector_search(self, query, limit=3):
    search_vector = self.local_llm.embeddings.create(
      input = query, model="NA"
    ).data[0].embedding
    return self.con.sql("""
      SELECT text, index, 
             array_cosine_similarity(embeddings, $search::FLOAT[1024]) AS score
      FROM olympics
      ORDER BY score DESC
      LIMIT $limit
      """, params={"search": search_vector, "limit": limit})
