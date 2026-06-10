from pathlib import Path

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse

from .routers import campaigns, delivery, invoices, masters
# FastAPIのインスタンスを作成（Swagger UIは日本語化のため独自エンドポイントで提供する）
app = FastAPI(
    title="Pandora Ad Platform API",
    description="広告配信プラットフォーム API（研修用）",
    version="1.0.0",
    docs_url=None,
)

# 日本語化スクリプトなどの静的ファイルを配信
app.mount("/static", StaticFiles(directory=Path(__file__).resolve().parent / "static"), name="static")

# ルーターをアプリに登録
app.include_router(masters.router)
app.include_router(campaigns.router)
app.include_router(delivery.router)
app.include_router(invoices.router)

# ルートエンドポイント
@app.get("/")
def root():
    return {"message": "Pandora Ad Platform API"}


# Swagger UI（日本語化スクリプトを読み込む）
@app.get("/docs", include_in_schema=False)
def custom_swagger_ui_html():
    response = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
    )
    html = response.body.decode("utf-8")
    html = html.replace("</body>", '<script src="/static/swagger-ja.js"></script></body>')
    return HTMLResponse(html)
