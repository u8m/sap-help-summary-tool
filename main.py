import os
from dotenv import load_dotenv
import pdfplumber
from groq import Groq

# .envファイルの読み込み（Groq APIキー格納用）
load_dotenv(dotenv_path="gpt-key.env")

# Groqクライアントの初期化
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# PDF読み込み
file_path = "Docs/mrp_overview.pdf"
with pdfplumber.open(file_path) as pdf:
    content = ""
    for page in pdf.pages:
        content += page.extract_text() + "\n"

# プロンプト生成
prompt = f"""
以下はSAP HelpのMRPに関するドキュメントです。
初心者にもわかりやすいように、要点を簡潔に日本語で要約してください：

{content}
"""

# Groq APIで要約を実行（LLaMA3などのモデルを使用）
response = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.3
)

# 要約結果を出力
summary = response.choices[0].message.content
print("\n🔽 要約結果（Groq）：\n")
print(summary)