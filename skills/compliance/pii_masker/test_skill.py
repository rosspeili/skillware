import os

import pytest
import yaml

from .skill import PIIMaskerSkill


@pytest.fixture
def skill():
    return PIIMaskerSkill()


@pytest.fixture
def manifest():
    manifest_path = os.path.join(os.path.dirname(__file__), "manifest.yaml")
    with open(manifest_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_skill_manifest_consistency(skill, manifest):
    skill_manifest = skill.manifest
    assert skill_manifest["name"] == manifest["name"]
    assert skill_manifest["version"] == manifest["version"]


def test_pii_masker_modes(mocker, skill):
    mock_response = (
        "Hello [PERSON_1], your wallet [CRYPTO_ADDRESS] and [EMAIL] have been verified."
    )
    mocker.patch.object(
        skill,
        "_call_ollama",
        return_value=(mock_response, ["PERSON_1", "CRYPTO_ADDRESS", "EMAIL"]),
    )

    sample_text = (
        "Hello John Doe, your wallet 0xabc and john@doe.com have been verified."
    )

    result_mask = skill.execute({"text": sample_text})
    assert (
        result_mask["sanitized_text"]
        == "Hello [PERSON_1], your wallet [CRYPTO_ADDRESS] and [EMAIL] have been verified."
    )
    assert "PERSON" in result_mask["metadata"]["detected_entities"]
    assert "CRYPTO_ADDRESS" in result_mask["metadata"]["detected_entities"]

    result_redact = skill.execute({"text": sample_text, "mode": "redact"})
    assert (
        result_redact["sanitized_text"]
        == "Hello XXXX, your wallet XXXX and XXXX have been verified."
    )

    result_remove = skill.execute({"text": sample_text, "mode": "remove"})
    assert (
        result_remove["sanitized_text"] == "Hello , your wallet and have been verified."
    )
