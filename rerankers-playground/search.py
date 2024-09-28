import duckdb
import llama_cpp

class Search:
  def __init__(self, con):
    self.con = con
    self.llm = llama_cpp.Llama(
      model_path="./models/mxbai-embed-large-v1-f16.gguf", 
      embedding=True, 
      verbose=False
    )


  def vector_search(self, query, limit=3):
    search_vector = self.llm.create_embedding([query])['data'][0]['embedding']
    return self.con.sql("""
      SELECT text, index, 
              array_cosine_similarity(
                embeddings, $searchVector::FLOAT[1024]
              ) AS score
      FROM olympics
      ORDER BY score DESC
      LIMIT $limit
      """, params={"searchVector": search_vector, "limit": limit})


