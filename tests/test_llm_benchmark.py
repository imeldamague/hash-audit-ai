from unittest.mock import patch, MagicMock
import json

from hash_audit.llm import ask_ollama_detailed


def mock_ollama_response(data):
    response = MagicMock()
    response.__enter__.return_value = response
    response.__exit__.return_value = False
    response.read.return_value = json.dumps(data).encode("utf-8")
    return response


@patch("hash_audit.llm.urllib.request.urlopen")
def test_benchmark_success(mock_urlopen):
    mock_urlopen.return_value = mock_ollama_response({
        "response": "MD5 est trop rapide.",
        "done_reason": "stop",
        "eval_count": 50,
        "total_duration": 1000000000,
    })

    result = ask_ollama_detailed("Test", model="llama3.2:3b")

    assert result["status"] == "success"
    assert result["eval_count"] == 50


@patch("hash_audit.llm.urllib.request.urlopen")
def test_benchmark_truncated(mock_urlopen):
    mock_urlopen.return_value = mock_ollama_response({
        "response": "Analyse inachevee",
        "done_reason": "length",
        "eval_count": 1024,
    })

    result = ask_ollama_detailed("Test", model="qwen3:4b")

    assert result["status"] == "truncated"
    assert result["final_response"] == ""


@patch("hash_audit.llm.urllib.request.urlopen")
def test_benchmark_qwen_final(mock_urlopen):
    mock_urlopen.return_value = mock_ollama_response({
        "response": "Analyse</think>Argon2id est recommande.",
        "done_reason": "stop",
        "eval_count": 859,
    })

    result = ask_ollama_detailed("Test", model="qwen3:4b")

    assert result["status"] == "success"
    assert result["final_response"] == "Argon2id est recommande."
