from fastapi import FastAPI 
from pydantic import BaseModel
from typing import List

from fastembed.embedding import FlagEmbedding as Embedding

app = FastAPI()

class EmbedRequest(BaseModel):
    inputs: List[str]


@app.post("/embed")
def embed(request: EmbedRequest):
    print(request.inputs)
    embeddings = app.model.passage_embed(request.inputs)
    return [arr.tolist() for arr in embeddings]

app.model = Embedding(model_name="BAAI/bge-base-en-v1.5")