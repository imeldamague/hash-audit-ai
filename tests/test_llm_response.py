import pytest

from hash_audit.llm import extract_final_response


def test_normal_response():
    assert extract_final_response(
        "MD5 est trop rapide."
    ) == "MD5 est trop rapide."


def test_qwen_final_response():
    assert extract_final_response(
        "Analyse interne</think>Argon2id est recommandé."
    ) == "Argon2id est recommandé."


def test_empty_final_response():
    assert extract_final_response(
        "Analyse interne</think>   "
    ) == ""
