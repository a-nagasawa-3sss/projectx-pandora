from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# データベースのURLを定義
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
# SQLiteのファイルはdataディレクトリのpandora.db
DATABASE_URL = f"sqlite:///{DATA_DIR / 'pandora.db'}"

# SQLAlchemyのエンジンとセッションを設定
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# セッションローカルクラスとベースクラスを定義
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# モデルのベースクラス
Base = declarative_base()

# データベースセッションを取得するための依存関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
