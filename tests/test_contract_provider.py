import socket
import threading
import time
from pathlib import Path

import pytest
import uvicorn
from pact import Verifier

from server.main import app

PROJECT_ROOT = Path(__file__).resolve().parent.parent
# PACT_FILE = PROJECT_ROOT / "pacts" / "webfrontendclient-corebankingservice.json"
PACT_FILE = (
    PROJECT_ROOT / "pact" / "pacts" / "WebFrontendClient-CoreBankingService.json"
)


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def provider_url():
    """Run the FastAPI provider in a background thread and yield its base URL."""
    port = _free_port()
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    deadline = time.time() + 10
    while not server.started:
        if time.time() > deadline:
            raise RuntimeError("Provider server failed to start within 10s")
        time.sleep(0.05)

    yield f"http://127.0.0.1:{port}"

    server.should_exit = True
    thread.join(timeout=5)


def test_contract_against_provider(provider_url):
    assert PACT_FILE.exists(), f"Pact file not found: {PACT_FILE}"

    Verifier("CoreBankingService", host="127.0.0.1").add_transport(
        url=provider_url
    ).add_source(PACT_FILE).verify()
