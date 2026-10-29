
from src.matching.embedding_engine import EmbeddingEngine


def main():
    texts = [
        "Machine learning identifies patterns in data.",
        "ML discovers patterns within datasets.",
        "The weather is sunny today.",
    ]

    engine = EmbeddingEngine()

    embeddings = engine.encode(texts)
    similarities = engine.similarity_matrix(embeddings)

    print("Embedding shape:", embeddings.shape)
    print("\nSimilarity matrix:")

    for row in similarities:
        print([round(float(score), 3) for score in row])

    paraphrase_score = float(similarities[0, 1])
    unrelated_score = float(similarities[0, 2])

    print(f"\nParaphrase similarity: {paraphrase_score:.3f}")
    print(f"Unrelated similarity:  {unrelated_score:.3f}")

    assert embeddings.shape == (3, 384)
    assert similarities.shape == (3, 3)
    assert paraphrase_score > unrelated_score

    print("\nEmbedding tests passed!")


if __name__ == "__main__":
    main()
