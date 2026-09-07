import numpy as np
from sentence_transformers import SentenceTransformer
from app.utils.config import SIMILARITY_THRESHOLD, EMBEDDING_MODEL_NAME


class SemanticGuard:

    def __init__(self, model_name: str = EMBEDDING_MODEL_NAME, threshold: float = SIMILARITY_THRESHOLD):
        self.threshold = threshold
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def compute_similarity(self, original_text: str, compressed_text: str) -> float:
        if not original_text.strip() or not compressed_text.strip():
            return 1.0 if not original_text.strip() and not compressed_text.strip() else 0.0

        embeddings = self.model.encode([original_text, compressed_text], convert_to_numpy=True)
        vec1, vec2 = embeddings[0], embeddings[1]

        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        similarity = np.dot(vec1, vec2) / (norm1 * norm2)
        return float(similarity)

    def verify(self, original_text: str, compressed_text: str, threshold: float = None) -> dict:
        target_threshold = threshold if threshold is not None else self.threshold
        similarity = self.compute_similarity(original_text, compressed_text)
        passed = similarity >= target_threshold

        return {
            "passed": passed,
            "similarity": round(similarity, 4),
            "threshold": target_threshold
        }
