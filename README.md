# SAP Help 要約ツール 📝

SAP Help Portal のPDFをアップロードし、AI（Groq API）で初心者向けに要約するStreamlitアプリです。

## 主な機能

- PDFファイルアップロード
- Llama3を使った要約生成
- キーワード検索機能
- ワードクラウド可視化
- ダーク＆ライト UI の組み合わせ
- 日本語フォント・モダンUI対応

## 使用技術

- Python / Streamlit
- Groq API (LLaMA3)
- pdfplumber
- WordCloud
- dotenv

## 実行方法

```bash
streamlit run streamlit_app.py