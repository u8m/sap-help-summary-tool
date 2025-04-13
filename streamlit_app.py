import os
import streamlit as st
import pdfplumber
import matplotlib.pyplot as plt
from groq import Groq
from dotenv import load_dotenv
from wordcloud import WordCloud

# .envファイル読み込み
load_dotenv(dotenv_path="gpt-key.env")

# フォントをMicrosoft JhengHeiに指定
st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        font-family: 'Microsoft JhengHei', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Groq APIクライアントの設定
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 色設定
st.markdown(
    """
    <style>
        body {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        .stApp {
            background-color: #ffffff;
            color: #000000;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: 'Microsoft JhengHei', sans-serif;
        background-color: #ffffff;
        color: #000000;
    }

    .stApp {
        background-color: #ffffff;
        color: #000000;
    }

    /* ✅ ファイルアップロード欄 */
    .stFileUploader {
        background-color: #d1d1d1;
        border-radius: 10px;
        padding: 10px;
    }

    /* ✅ テキストボックス */
    input[type="text"] {
        background-color: #d1d1d1 !important;
        color: #000000 !important;
        border-radius: 8px;
        border: 1px solid #999;
        padding: 6px;
    }

    /* ✅ プレースホルダー文字色 */
    input[type="text"]::placeholder {
        color: #666666 !important;
        opacity: 1 !important;
    }

    /* ✅ ボタン */
    .stButton > button {
        background-color: #d1d1d1;
        color: #000;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit UI設定
st.title("SAP Help MRP 要約ツール")
uploaded_file = st.file_uploader("SAPマニュアルのPDFファイルをアップロード", type="pdf")

if uploaded_file is not None:
    with pdfplumber.open(uploaded_file) as pdf:
        content = ""
        for page in pdf.pages:
            content += page.extract_text() + "\n"

    # 日本語で要約を生成するプロンプト
    prompt = f"""
    以下はSAP HelpのMRPに関するドキュメントです。
    初心者にもわかりやすいように、要点を簡潔に【必ず日本語で】で要約してください：
    {content}
    """

    # Groq APIで要約を生成
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    summary = response.choices[0].message.content
    st.markdown("### 📝 要約結果")
    st.markdown(
        f"""
    <div style='background-color:#222222;padding:20px;border-radius:10px;margin-top:10px;color:#ffffff;'>
    {summary}
    </div>
    """,
        unsafe_allow_html=True,
    )

    # 📊 ワードクラウド生成
    st.subheader("📊 ワードクラウド（キーワードの可視化）")

    # WordCloud生成
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white",
        font_path="/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",  # Mac用の日本語フォント
    ).generate(content)

    # Matplotlibで表示
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

    # 🔍 キーワード検索欄
    st.subheader("🔍 キーワード検索")

    # ⬇️ このラベルを小さめ＆グレーで表示
    st.markdown(
        "<p style='font-size:14px; color:#444;'>調べたいキーワードを入力してください</p>",
        unsafe_allow_html=True,
    )

    keyword = st.text_input("", key="keyword_input", label_visibility="collapsed")

    if keyword:
        search_prompt = f"以下のSAPマニュアルに関連する内容から「{keyword}」について初心者向けに【必ず日本語で】で説明してください：\n{content}"

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": search_prompt}],
            temperature=0.3,
        )

        explanation = response.choices[0].message.content
        st.markdown("### 🧠 解説：")
        st.markdown(
            f"""
        <div style='background-color:#1e1e1e;padding:20px;border-radius:10px;margin-top:10px;color:#ffffff;'>
        {explanation}
        </div>
        """,
            unsafe_allow_html=True,
        )
