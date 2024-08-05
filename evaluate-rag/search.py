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

  def fts(self, query, limit=3):
    return self.con.sql("""
      SELECT text, index, fts_main_olympics.match_bm25(
              index,
              $searchTerm
          ) AS score
      FROM olympics
      WHERE score IS NOT NULL
      ORDER BY score DESC
      LIMIT $limit
      """, params={"searchTerm": query, "limit": limit})


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


  def hybrid(self, query, limit=3, base_limit=20):
    fts_result = (self.fts(query, limit=base_limit)
      .select("*, rank() OVER (ORDER BY score DESC) AS rank")
    )
    vec_result = (self.vector_search(query, limit=base_limit)
      .select("*, rank() OVER (ORDER BY score DESC) AS rank")
    )

    return self.con.sql("""
    FROM fts_result
    FULL OUTER JOIN vec_result ON fts_result.text = vec_result.text

    SELECT coalesce(fts_result.text, vec_result.text) AS text, 
          coalesce(fts_result.index, vec_result.index) AS index, 
          rrf(vec_result.rank) + rrf(fts_result.rank) AS score,
          fts_result.rank as ftsRank, vec_result.rank AS vecRank

    ORDER BY score DESC
    LIMIT $limit
    """, params={"limit": limit})


