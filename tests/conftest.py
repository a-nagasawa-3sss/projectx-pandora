import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import app  # noqa: E402
from data import seed  # noqa: E402

# テスト実行前にDBを既知の状態へ初期化するためのフィクスチャ
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """テスト実行前にDBを既知の状態へ初期化する。"""
    seed.main()

# テストクライアントのフィクスチャ
@pytest.fixture()
def client():
    return TestClient(app)
