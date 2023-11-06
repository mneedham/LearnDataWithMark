from fastembed.embedding import FlagEmbedding as Embedding
import numpy as np
from typing import List

documents: List[str] = [
    "passage: Hello, World!",
    "passage: This is an example passage.",
]
embedding_model = Embedding(model_name="BAAI/bge-base-en-v1.5", max_length=512) 
# embedding_model = Embedding(model_name="BAAI/bge-base-en-v1.5", max_length=512) 
embeddings: List[np.ndarray] = list(embedding_model.embed(documents)) # Note the list() call - this is a generator 