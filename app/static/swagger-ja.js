// Swagger UI の主要なボタン・ラベルを日本語に置き換える簡易スクリプト。
// Swagger UI自体には文言の多言語対応機能が無いため、
// 描画されたDOMのテキストを辞書で置換することで日本語化する。
(function () {
  const dict = {
    "Try it out": "実行してみる",
    "Cancel": "キャンセル",
    "Execute": "実行",
    "Clear": "クリア",
    "Reset": "リセット",
    "Responses": "レスポンス",
    "Response body": "レスポンスボディ",
    "Response headers": "レスポンスヘッダー",
    "Curl": "cURL",
    "Request URL": "リクエストURL",
    "Server response": "サーバーレスポンス",
    "Code": "コード",
    "Details": "詳細",
    "Parameters": "パラメータ",
    "Name": "名前",
    "Description": "説明",
    "Example Value": "サンプル値",
    "Schema": "スキーマ",
    "Schemas": "スキーマ",
    "No parameters": "パラメータはありません",
    "Send empty value": "空の値を送信する",
    "Download": "ダウンロード",
    "Servers": "サーバー",
    "Authorize": "認証",
    "Authorized": "認証済み",
    "Close": "閉じる",
    "Logout": "ログアウト",
    "Request body": "リクエストボディ",
    "required": "必須",
    "Available authorizations": "利用可能な認証",
    "Loading...": "読み込み中...",
    "Hide": "閉じる",
    "Show": "表示",
    "Models": "モデル",
    "No links": "リンクなし",
    "Links": "リンク",
    "Deep link to this operation": "この操作へのリンク",
    "Edit Value": "値を編集",
    "Copy": "コピー",
  };

  function translateText(text) {
    const trimmed = text.trim();
    if (Object.prototype.hasOwnProperty.call(dict, trimmed)) {
      return text.replace(trimmed, dict[trimmed]);
    }
    return null;
  }

  function walk(node) {
    if (node.nodeType === Node.TEXT_NODE) {
      const translated = translateText(node.nodeValue);
      if (translated !== null) {
        node.nodeValue = translated;
      }
      return;
    }
    if (node.nodeType !== Node.ELEMENT_NODE) {
      return;
    }
    if (node.tagName === "SCRIPT" || node.tagName === "STYLE") {
      return;
    }
    for (const child of Array.from(node.childNodes)) {
      walk(child);
    }
  }

  function start() {
    const root = document.getElementById("swagger-ui");
    if (!root) {
      setTimeout(start, 200);
      return;
    }

    walk(root);

    const observer = new MutationObserver((mutations) => {
      for (const mutation of mutations) {
        if (mutation.type === "childList") {
          mutation.addedNodes.forEach((node) => walk(node));
        } else if (mutation.type === "characterData") {
          walk(mutation.target);
        }
      }
    });

    observer.observe(root, {
      childList: true,
      subtree: true,
      characterData: true,
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
