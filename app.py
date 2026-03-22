import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- ページ設定 ---
st.set_page_config(page_title="Tech0 Search v0.2", layout="wide")

# --- 状態管理（セッション）の初期化 ---
if "pages" not in st.session_state:
    st.session_state.pages = []  # クロール済みデータを格納

# --- ロジック部分（ご提示のコードを統合） ---

def fetch_page(url: str) -> str:
    """HTMLを取得するヘルパー関数"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception:
        return ""

def parse_html(html: str, url: str) -> dict:
    """HTMLを解析して情報を抽出する"""
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string if soup.title else url
    description = ""
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc:
        description = meta_desc.get("content", "")
    
    # 本文（scriptやstyleを除去）
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()
    full_text = soup.get_text(separator=" ", strip=True)

    return {
        "url": url,
        "title": title,
        "description": description,
        "full_text": full_text,
        "keywords": [],
        "crawl_status": "success",
        "crawled_at": datetime.now().isoformat(),
    }

def crawl_url(url: str) -> dict:
    """URLをクロールして情報を返す"""
    html = fetch_page(url)
    if not html:
        return {
            "url": url,
            "crawl_status": "failed",
            "crawled_at": datetime.now().isoformat(),
            "error": "Failed to fetch page",
        }
    try:
        return parse_html(html, url)
    except Exception as e:
        return {
            "url": url,
            "crawl_status": "error",
            "crawled_at": datetime.now().isoformat(),
            "error": str(e),
        }

def _make_preview(text: str, query: str, ctx: int = 80) -> str:
    if not text or not query: return ""
    pos = text.lower().find(query.lower())
    if pos == -1:
        return (text[:200] + "...") if len(text) > 200 else text
    start = max(0, pos - ctx)
    end = min(len(text), pos + len(query) + ctx)
    preview = "..." if start > 0 else ""
    preview += text[start:end]
    preview += "..." if end < len(text) else ""
    return preview

def search_fulltext(query: str, pages: list) -> list:
    """
    全文検索（本文含む）を実行し、マッチ数でスコアリングする。
    """
    if not query.strip():
        return []

    results = []
    q = query.lower()

    for page in pages:
        # --- ここを修正 ---
        # 各項目を取得する際、None の場合は空文字 "" を使うように dict.get(key, default) を徹底
        # または or "" を使って確実に文字列にします
        text = " ".join([
            str(page.get("title") or ""),
            str(page.get("description") or ""),
            str(page.get("full_text") or ""),
            " ".join([str(k) for k in page.get("keywords", []) if k is not None]),
        ]).lower()
        # ------------------

        count = text.count(q)

        if count > 0:
            r = page.copy()
            r["match_count"] = count
            r["preview"] = _make_preview(
                page.get("full_text") or page.get("description") or "",
                query
            )
            results.append(r)

    results.sort(key=lambda x: x["match_count"], reverse=True)
    return results

# --- UI部分 ---

st.title("🔍 Tech0 Search v0.2")
st.caption("PROJECT ZERO — 社内ナレッジ検索エンジン 【全文検索対応】")

tabs = st.tabs(["🔍 検索", "🌐 クロール", "📝 手動登録", "📋 一覧"])

# 1. 検索タブ
with tabs[0]:
    query = st.text_input("検索キーワードを入力", placeholder="キーワードを入力してください...")
    if query:
        results = search_fulltext(query, st.session_state.pages)
        st.write(f"**{len(results)}** 件ヒットしました")
        for res in results:
            with st.container():
                st.markdown(f"### [{res['title']}]({res['url']})")
                st.caption(f"URL: {res['url']} | スコア: {res['match_count']}")
                st.write(res['preview'])
                st.divider()

# 2. クロールタブ（画像で指定されたUI）
with tabs[1]:
    st.subheader("🌀 単体クロール")
    st.info("URLを入力すると、自動でページ情報を取得します")
    
    url_input = st.text_input("クロール対象URL", placeholder="https://example.com")
    if st.button("🌀 クロール実行"):
        if url_input:
            with st.spinner("クロール中..."):
                res = crawl_url(url_input)
                if res["crawl_status"] == "success":
                    st.session_state.pages.append(res)
                    st.success(f"成功: {res['title']}")
                else:
                    st.error(f"失敗: {res.get('error')}")
        else:
            st.warning("URLを入力してください。")

    st.divider()

    st.subheader("📋 一括クロール")
    url_list_input = st.text_area("URLリスト (1行に1URL)", placeholder="https://example1.com\nhttps://example2.com")
    if st.button("🚀 一括クロール実行"):
        if url_list_input:
            urls = [u.strip() for u in url_list_input.strip().split('\n') if u.strip()]
            progress_bar = st.progress(0)
            for i, url in enumerate(urls):
                res = crawl_url(url)
                if res["crawl_status"] == "success":
                    st.session_state.pages.append(res)
                progress_bar.progress((i + 1) / len(urls))
            st.success(f"{len(urls)}件の処理が完了しました。")

# 4. 一覧タブ
with tabs[3]:
    st.subheader("保存済みページ一覧")
    if st.session_state.pages:
        st.table([{"タイトル": p["title"], "URL": p["url"], "取得日時": p["crawled_at"]} for p in st.session_state.pages])
    else:
        st.write("データがありません。")