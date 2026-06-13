import os
from unittest.mock import MagicMock

import numpy as np
import pytest
import yaml

from .skill import NoveltyExtractor


def _mock_embed_vectors(texts):
    """Deterministic keyword vectors — no HuggingFace download in CI."""
    vectors = []
    for text in texts:
        t = text.lower()
        if "bitcoin" in t:
            vectors.append(np.array([1.0, 0.0, 0.0], dtype=float))
        elif "sky" in t or "blue" in t:
            vectors.append(np.array([0.0, 1.0, 0.0], dtype=float))
        elif "python" in t:
            vectors.append(np.array([0.0, 0.0, 1.0], dtype=float))
        else:
            vectors.append(np.array([0.1, 0.1, 0.1], dtype=float))
    return vectors


@pytest.fixture(autouse=True)
def mock_embedding_model(monkeypatch):
    """Bundle tests must stay offline; mock fastembed to avoid HF rate limits in CI."""
    NoveltyExtractor._model = None
    mock_model = MagicMock()
    mock_model.embed.side_effect = _mock_embed_vectors

    @classmethod
    def _fake_get_model(cls):
        if cls._model is None:
            cls._model = mock_model
        return cls._model

    monkeypatch.setattr(NoveltyExtractor, "_get_model", _fake_get_model)
    yield
    NoveltyExtractor._model = None


@pytest.fixture
def skill():
    return NoveltyExtractor()


@pytest.fixture
def manifest():
    manifest_path = os.path.join(os.path.dirname(__file__), "manifest.yaml")
    with open(manifest_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_skill_manifest_consistency(skill, manifest):
    skill_manifest = skill.manifest
    assert skill_manifest["name"] == manifest["name"]
    assert skill_manifest["version"] == manifest["version"]


def test_skill_returns_dict(skill):
    result = skill.execute(
        {
            "dataset_chunk": "Bitcoin is going to rise.\n\nThe sky is blue.",
            "novelty_threshold": 0.85,
        }
    )
    assert isinstance(result, dict)


def test_skill_output_keys(skill):
    result = skill.execute(
        {
            "dataset_chunk": "Bitcoin is going to rise.\n\nThe sky is blue.",
            "novelty_threshold": 0.85,
        }
    )
    assert "distilled_content" in result
    assert "compression_ratio" in result
    assert "redundant_chunks_dropped" in result


def test_skill_filters_redundant_chunks(skill):
    result = skill.execute(
        {
            "dataset_chunk": (
                "Bitcoin is going to rise.\n\n"
                "Bitcoin will increase in value.\n\n"
                "The sky is blue."
            ),
            "novelty_threshold": 0.85,
        }
    )
    assert result["redundant_chunks_dropped"] >= 1
    assert "Bitcoin is going to rise." in result["distilled_content"]
    assert "The sky is blue." in result["distilled_content"]


def test_skill_empty_input(skill):
    result = skill.execute(
        {
            "dataset_chunk": "",
            "novelty_threshold": 0.85,
        }
    )
    assert result["distilled_content"] == ""
    assert result["redundant_chunks_dropped"] == 0


def test_skill_baseline_filters_seen_content(skill):
    baseline = "Bitcoin is going to rise.\n\nThe sky is blue."
    result = skill.execute(
        {
            "dataset_chunk": "Bitcoin is going to rise.\n\nPython is a programming language.",
            "novelty_threshold": 0.85,
            "baseline_chunks": baseline,
        }
    )
    assert "Python is a programming language." in result["distilled_content"]
    assert result["redundant_chunks_dropped"] >= 1


def test_skill_sentence_strategy(skill):
    result = skill.execute(
        {
            "dataset_chunk": "Bitcoin is going to rise. The sky is blue. Python is great.",
            "novelty_threshold": 0.85,
            "chunk_strategy": "sentence",
        }
    )
    assert isinstance(result, dict)
    assert "distilled_content" in result
