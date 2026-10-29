import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class EmbeddingEngine:
    def __init__(self):
        # Load the pretrained model once, not for every chunk.
        self.model = SentenceTransformer(MODEL_NAME)

    def encode(self, texts: list[str]) -> np.ndarray:
        """Convert text passages into normalized embedding vectors."""
        if not texts:
            return np.empty((0, 384), dtype=np.float32)

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return embeddings

    @staticmethod
    def similarity_matrix(embeddings: np.ndarray) -> np.ndarray:
        """Calculate cosine similarity for every pair of embeddings."""
        if embeddings.size == 0:
            return np.empty((0, 0), dtype=np.float32)

        # Because vectors are normalized, dot product equals cosine similarity.
        return embeddings @ embeddings.T
