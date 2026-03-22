# 🔐 PROJECT ZERO — WEEK 3

# Tech0 Search v0.2 — ノートブック README

---

## 📁 このフォルダに含まれるファイル

week3-notebook/
├── w3_tech0_search_v0.2.ipynb  #コード解説ノートブック（本体）
├── pages.json   #サンプルデータ（Week2の続き）
├── crawler.py  #Webクローラー
├── search_fulltext.py  #全文検索ロジック
└── README.md  #このファイル


⚠️ **重要**：`全てのファイルを **同じフォルダ** に置いてください。
別のフォルダに入れると `FileNotFoundError` が発生します。

---

# 🚀 セットアップ手順

## 1. 必要なもの

- Python 3.10 以上
- VS Code + Jupyter 拡張機能（または JupyterLab）

---

## 2. 必要ライブラリのインストール

インストールしていない場合は、ターミナルで以下を実行してください。

```bash
pip install requests beautifulsoup4 streamlit
```


## 3. ノートブックを開く

VS Code でこのフォルダを開き、
w3_tech0_search_v0.2.ipynb をダブルクリックしてください。

## 4. カーネルを選択する

ノートブック右上の 「カーネルを選択」 から
Python 環境を選択してください。


## 📖 ノートブックの構成と使い方
Step 0	UI設計	完成画面をイメージする
Step 1	検索エンジンの設計図	データの流れを理解
Step 2	pages.json の理解	検索インデックスの構造
Step 3	Webクローラー	URLから情報取得
Step 4	全文検索	本文も検索できるようにする
Step 5	Streamlit統合	app.pyを自分で作る
Step 6	アプリ起動 & CDOレビュー	検索エンジン完成


## Step について

ノートブックを開いたら、**すぐにコードを実行するのではなく**、まず Step 0 の指示に従って  
「自分が思う完成画面」を紙に手書きしてください。  
その後、ノートブックに埋め込まれた実際の画面イメージと比べることで理解が深まります。


## crawler.py / search_fulltext.py について

Week3では 検索エンジンのコア部分 を作ります。

URL
 ↓
crawler.py
（Webページ取得）
 ↓
pages.json
（検索インデックス）
 ↓
search_fulltext.py
（全文検索）
 ↓
app.py
（Streamlit UI）

この構造を理解することが今回の目的です。


## app.py について

`app.py` の完成コードはあえて配布していません。  
Stepで学んだパーツを組み合わせて、自分で作ってみてください。  

**自分の手で動かした瞬間が一番理解が深まります。**


## ⚠️ よくあるエラーと対処法

### FileNotFoundError: pages.json
原因
pages.json がノートブックと同じフォルダにない

対処
week3-notebook/
├── w3_tech0_search_v0.2.ipynb
└── pages.json   ← ここに置く


 ## ModuleNotFoundError: requests
原因
requests がインストールされていない

対処
pip install requests


## ModuleNotFoundError: bs4
原因
BeautifulSoup がインストールされていない

対処
pip install beautifulsoup4


## ModuleNotFoundError: crawler
原因
crawler.py が同じフォルダにない

対処
week3-notebook/
├── crawler.py
├── search_fulltext.py
└── w3_tech0_search_v0.2.ipynb

同じフォルダに配置してください。


## 🏗️ Streamlit アプリ用フォルダ構成

ノートブックとは 別フォルダ に検索アプリを作ります。  
ノートブックと同じフォルダに入れないことで、練習中に `pages.json` が上書きされる心配がなくなります。

tech0-search/           ← Streamlit アプリ用フォルダ（新しく作る）
├── app.py              ← 自分で作る！
├── crawler.py          ← Stepで学んだ関数を参考に作る
├── search_fulltext.py  ← Stepで学んだ関数を参考に作る
├── requirements.txt    ← 下記参照
└── pages.json          ← week3-notebook/ の pages.json をコピー


## requirements.txt
streamlit>=1.32.0
requests
beautifulsoup4


## 💡 2つのフォルダを分ける理由
week3-notebook/ **学習用**（このノートブック・練習用 `pages.json`） |
tech0-search/   **アプリ用**（自分で作る `app.py` とそのデータ）

2つを分けておくことで、ノートブックを実行しても  
Streamlit アプリのデータに影響しません。


## 📚 参考リンク
Streamlit 公式ドキュメント https://docs.streamlit.io/
Streamlit API リファレンス  https://docs.streamlit.io/develop/api-reference
Streamlit チートシート  https://cheat-sheet.streamlit.app
Streamlit コンポーネントギャラリー https://streamlit.io/components



_Tech0 BootCamp 12期 | WEEK 3 — PROJECT ZERO 指令：Tech0 Search v0.2_
