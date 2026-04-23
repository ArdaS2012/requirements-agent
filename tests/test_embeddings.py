import pytest
from unittest.mock import MagicMock, patch
import numpy as np


# We patch the embedding model at the config level before the module is imported
@pytest.fixture(autouse=True)
def mock_embedding_model():
    """Replace the sentence-transformer model with a lightweight mock."""
    with patch("src.embeddings.embedding_model") as mock_model:
        # encode() returns a numpy-like array whose .tolist() gives a fixed vector
        mock_model.encode.side_effect = lambda text: np.array([0.1, 0.2, 0.3])
        yield mock_model


from src.embeddings import create_embedding, fake_embedding


class TestFakeEmbedding:
    """fake_embedding is a standalone utility – no mocking needed."""

    def test_returns_correct_dimension(self):
        vec = fake_embedding("hello", dim=1536)
        assert len(vec) == 1536

    def test_custom_dimension(self):
        vec = fake_embedding("hello", dim=64)
        assert len(vec) == 64

    def test_first_element_based_on_length(self):
        text = "a" * 500
        vec = fake_embedding(text)
        assert vec[0] == pytest.approx(0.5)

    def test_first_element_capped_at_one(self):
        text = "a" * 2000
        vec = fake_embedding(text)
        assert vec[0] == pytest.approx(1.0)

    def test_rag_count_in_second_element(self):
        vec = fake_embedding("rag rag rag")
        assert vec[1] == 3

    def test_postgres_count_in_third_element(self):
        vec = fake_embedding("postgres and postgres")
        assert vec[2] == 2

    def test_deterministic(self):
        assert fake_embedding("same text") == fake_embedding("same text")


class TestCreateEmbedding:

    def test_returns_list_of_embeddings(self):
        result = create_embedding(["hello", "world"])
        assert isinstance(result, list)
        assert len(result) == 2

    def test_each_embedding_is_a_list(self):
        result = create_embedding(["hello"])
        assert isinstance(result[0], list)

    def test_empty_input_returns_empty_list(self):
        result = create_embedding([])
        assert result == []

    def test_model_encode_called_per_text(self, mock_embedding_model):
        create_embedding(["a", "b", "c"])
        assert mock_embedding_model.encode.call_count == 3

    def test_single_text_embedding_shape(self):
        result = create_embedding(["test sentence"])
        assert len(result) == 1
        assert isinstance(result[0], list)
