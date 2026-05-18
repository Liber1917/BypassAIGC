"""
Integration tests requiring real API credentials.

Usage:
    BYPASS_AIGC_API_KEY=sk-xxx BYPASS_AIGC_BASE_URL=https://your-proxy/v1 \
    python -m pytest tests/test_integration.py -v -s

These tests verify the full optimization pipeline with real API calls.
Skip them in CI with: -k "not integration" or --ignore=tests/test_integration.py
"""
import os
import pytest
import time
from fastapi.testclient import TestClient

pytestmark = pytest.mark.integration

API_KEY = os.environ.get("BYPASS_AIGC_API_KEY")
BASE_URL = os.environ.get("BYPASS_AIGC_BASE_URL", "https://api.openai.com/v1")
MODEL = os.environ.get("BYPASS_AIGC_MODEL", "gpt-4o-mini")

requires_api = pytest.mark.skipif(
    not API_KEY,
    reason="Set BYPASS_AIGC_API_KEY to run integration tests",
)


@requires_api
class TestPolishWithRealAPI:
    @pytest.fixture(autouse=True)
    def setup_api_config(self, client, admin_token):
        client.post(
            "/api/admin/config",
            json={
                "POLISH_API_KEY": API_KEY,
                "POLISH_BASE_URL": BASE_URL,
                "POLISH_MODEL": MODEL,
                "ENHANCE_API_KEY": API_KEY,
                "ENHANCE_BASE_URL": BASE_URL,
                "ENHANCE_MODEL": MODEL,
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )

    def test_polish_simple_text(self, client, user_token):
        text = "人工智能技术正在快速发展。"
        resp = client.post(
            "/api/optimization/start",
            json={
                "original_text": text,
                "processing_mode": "paper_polish",
            },
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert resp.status_code == 200
        session_id = resp.json()["session_id"]

        for _ in range(60):
            time.sleep(2)
            prog = client.get(
                f"/api/optimization/sessions/{session_id}/progress",
                headers={"Authorization": f"Bearer {user_token}"},
            )
            status = prog.json()["status"]
            if status == "completed":
                break
            if status == "failed":
                pytest.fail(f"Task failed: {prog.json().get('error_message')}")

        detail = client.get(
            f"/api/optimization/sessions/{session_id}",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert detail.status_code == 200
        data = detail.json()
        assert data["status"] == "completed"
        assert len(data["segments"]) > 0
        for seg in data["segments"]:
            assert seg["polished_text"] is not None
            assert len(seg["polished_text"]) > 0

    def test_polish_and_enhance(self, client, user_token):
        text = "深度学习在自然语言处理领域取得了显著的进展。"
        resp = client.post(
            "/api/optimization/start",
            json={
                "original_text": text,
                "processing_mode": "paper_polish_enhance",
            },
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert resp.status_code == 200
        session_id = resp.json()["session_id"]

        for _ in range(120):
            time.sleep(2)
            prog = client.get(
                f"/api/optimization/sessions/{session_id}/progress",
                headers={"Authorization": f"Bearer {user_token}"},
            )
            status = prog.json()["status"]
            if status == "completed":
                break
            if status == "failed":
                pytest.fail(f"Task failed: {prog.json().get('error_message')}")

        detail = client.get(
            f"/api/optimization/sessions/{session_id}",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert detail.status_code == 200
        data = detail.json()
        assert data["status"] == "completed"
        for seg in data["segments"]:
            assert seg["polished_text"] is not None
            assert seg["enhanced_text"] is not None


@requires_api
class TestConcurrencyWithRealAPI:
    @pytest.fixture(autouse=True)
    def setup_api_config(self, client, admin_token):
        client.post(
            "/api/admin/config",
            json={
                "POLISH_API_KEY": API_KEY,
                "POLISH_BASE_URL": BASE_URL,
                "POLISH_MODEL": MODEL,
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )

    def test_parallel_tasks_same_user(self, client, user_token):
        texts = [
            "第一段测试文本。",
            "第二段测试文本。",
        ]
        sessions = []
        for text in texts:
            resp = client.post(
                "/api/optimization/start",
                json={"original_text": text, "processing_mode": "paper_polish"},
                headers={"Authorization": f"Bearer {user_token}"},
            )
            assert resp.status_code == 200
            sessions.append(resp.json()["session_id"])

        for sid in sessions:
            for _ in range(60):
                time.sleep(2)
                prog = client.get(
                    f"/api/optimization/sessions/{sid}/progress",
                    headers={"Authorization": f"Bearer {user_token}"},
                )
                status = prog.json()["status"]
                if status in ("completed", "failed"):
                    break
            assert status == "completed", f"Session {sid} failed"

        my_sessions = client.get(
            "/api/optimization/sessions",
            headers={"Authorization": f"Bearer {user_token}"},
        ).json()
        assert len(my_sessions) == 2
