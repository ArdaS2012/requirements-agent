import pytest
from unittest.mock import MagicMock, patch, call
import numpy as np


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

FAKE_EMBEDDING = [0.1, 0.2, 0.3]
FAKE_ROWS = [
    ("Chunk content A", {"page_start": 0}, 0.12),
    ("Chunk content B", {"page_start": 1}, 0.35),
    ("Chunk content C", {"page_start": 2}, 0.67),
]


@pytest.fixture(autouse=True)
def mock_dependencies():
    """Patch DB connection, embedding model, and cross-encoder globally."""
    with (
        patch("src.embeddings.embedding_model") as mock_model,
        patch("src.retrieval.cross_encoder") as mock_cross,
        patch("src.retrieval.psycopg") as mock_psycopg,
        patch("src.retrieval.register_vector"),
    ):
        # Embedding model
        mock_model.encode.return_value = np.array(FAKE_EMBEDDING)

        # Cross-encoder: predict returns decreasing scores by default
        mock_cross.predict.return_value = np.array([0.9, 0.5, 0.1])

        # DB cursor that returns FAKE_ROWS
        mock_cursor = MagicMock()
        mock_cursor.__enter__ = lambda s: s
        mock_cursor.__exit__ = MagicMock(return_value=False)
        mock_cursor.fetchall.return_value = FAKE_ROWS

        mock_conn = MagicMock()
        mock_conn.__enter__ = lambda s: s
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.cursor.return_value = mock_cursor

        mock_psycopg.connect.return_value = mock_conn

        yield {
            "model": mock_model,
            "cross": mock_cross,
            "psycopg": mock_psycopg,
            "conn": mock_conn,
            "cursor": mock_cursor,
        }


from src.retrieval import process_query, rerank_query


# ---------------------------------------------------------------------------
# process_query
# ---------------------------------------------------------------------------

class TestProcessQuery:

    def test_returns_list(self):
        results = process_query("what are the auth requirements?")
        assert isinstance(results, list)

    def test_returns_same_rows_as_db(self):
        results = process_query("some query")
        assert results == FAKE_ROWS

    def test_embedding_called_once(self, mock_dependencies):
        process_query("my query")
        mock_dependencies["model"].encode.assert_called_once_with("my query")

    def test_db_queried_with_embedding(self, mock_dependencies):
        process_query("test query")
        cursor = mock_dependencies["cursor"]
        cursor.execute.assert_called_once()
        # The embedding vector must be passed as the first SQL param
        args = cursor.execute.call_args[0]
        assert FAKE_EMBEDDING == list(args[1][0])

    def test_empty_db_result_returns_empty_list(self, mock_dependencies):
        mock_dependencies["cursor"].fetchall.return_value = []
        results = process_query("anything")
        assert results == []


# ---------------------------------------------------------------------------
# rerank_query
# ---------------------------------------------------------------------------

class TestRerankQuery:

    def test_empty_results_returns_empty(self):
        assert rerank_query("q", []) == []

    def test_returns_same_number_of_rows(self):
        reranked = rerank_query("q", FAKE_ROWS)
        assert len(reranked) == len(FAKE_ROWS)

    def test_highest_score_is_first(self, mock_dependencies):
        # Scores: A=0.9, B=0.5, C=0.1 → A should be first
        reranked = rerank_query("q", FAKE_ROWS)
        assert reranked[0] == FAKE_ROWS[0]

    def test_cross_encoder_called_with_correct_pairs(self, mock_dependencies):
        rerank_query("my query", FAKE_ROWS)
        cross = mock_dependencies["cross"]
        cross.predict.assert_called_once()
        pairs = cross.predict.call_args[0][0]
        assert len(pairs) == len(FAKE_ROWS)
        assert all(p[0] == "my query" for p in pairs)

    def test_order_reversed_when_scores_inverted(self, mock_dependencies):
        # Make C score highest
        mock_dependencies["cross"].predict.return_value = np.array([0.1, 0.5, 0.9])
        reranked = rerank_query("q", FAKE_ROWS)
        assert reranked[0] == FAKE_ROWS[2]

    def test_single_result_returned_as_list(self):
        single = [FAKE_ROWS[0]]
        with patch("src.config.cross_encoder") as mock_cross:
            mock_cross.predict.return_value = np.array([1.0])
            # re-import to pick up patch — use the already-imported function
            from src.retrieval import rerank_query as rq
            result = rq("q", single)
        assert len(result) == 1
