"""HTTP model adapters. Request metadata excludes authentication headers."""
import json
import os
import urllib.error
import urllib.request

from design import INSTRUCTION


class RejectRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}), RejectRedirect())
LOCAL = "http://127.0.0.1:11434"
CLAUDE = "https://api.anthropic.com/v1/messages"
CLAUDE_VERSION = "2023-06-01"


def request(url, payload=None, headers=None):
    body = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "application/json", **(headers or {}),
    })
    with OPENER.open(req, timeout=90) as response:
        return {
            "http_status": response.status,
            "request_id": response.headers.get("request-id"),
            "body": response.read().decode("utf-8", errors="replace"),
        }


def local_metadata(model):
    def get(path, payload=None):
        return json.loads(request(LOCAL + path, payload)["body"])

    tag = next((entry for entry in get("/api/tags")["models"] if entry["name"] == model), None)
    if tag is None:
        raise ValueError(f"Install exact Ollama tag first: {model}")
    details = get("/api/show", {"model": model})
    return {
        "tag": tag, "version": get("/api/version")["version"],
        "model_info": details.get("model_info"), "capabilities": details.get("capabilities"),
        "template": details.get("template"), "parameters": details.get("parameters"),
        "license": details.get("license"),
    }


def build_request(provider, model, prompt, seed):
    stem, instruction = prompt.rsplit("\n", 1)
    if instruction != INSTRUCTION:
        raise ValueError("Unexpected answer instruction")
    prompt = stem + '\nReturn a JSON object with one key "answer" and one option letter (A, B, C, or D) as its value.'
    messages = [{"role": "user", "content": prompt}]
    if provider == "ollama":
        payload = {
            "model": model, "messages": messages, "stream": False, "keep_alive": "10m",
            "format": {"type": "object", "properties": {"answer": {
                "type": "string", "enum": list("ABCD"),
            }}, "required": ["answer"], "additionalProperties": False},
            "options": {"temperature": 0.2, "top_p": 1, "top_k": 0, "seed": seed,
                        "num_predict": 96, "num_ctx": 2048},
        }
        if model.startswith("qwen3:"):
            payload["think"] = False
        return LOCAL + "/api/chat", payload
    return CLAUDE, {
        "model": model, "messages": messages, "temperature": 0.2, "max_tokens": 96,
    }


def response_text(provider, response):
    data = json.loads(response["body"])
    if provider == "ollama":
        if data.get("done") is not True or data.get("error"):
            raise ValueError("Incomplete Ollama response")
        return data["message"]["content"]
    if data.get("type") != "message" or data.get("role") != "assistant":
        raise ValueError("Invalid Messages API response")
    return "".join(part["text"] for part in data["content"] if part["type"] == "text")


def auth(provider):
    if provider == "ollama":
        return {}
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise SystemExit("Commercial cohort not run: ANTHROPIC_API_KEY is absent.")
    return {"x-api-key": key, "anthropic-version": CLAUDE_VERSION}
