import os
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "REPLACE_WITH_YOUR_OPENAI_API_KEY":
	raise RuntimeError(
		"OPENAI_API_KEY not set. Add it to .env or set it in the environment. Do NOT commit real keys."
	)

import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# .env から環境変数を読み込む
load_dotenv()

# -----------------------------
# LLM 呼び出し関数（課題必須）
# -----------------------------
def get_llm_response(user_input: str, expert_type: str) -> str:
    """
    入力テキストと専門家タイプを受け取り、
    LLM に問い合わせて回答を返す関数
    """

    if expert_type == "AIエンジニア":
        system_prompt = (
            "あなたは経験豊富なAIエンジニアです。"
            "技術的に正確で、わかりやすい説明を行い、"
            "可能であれば実用的な例も交えて回答してください。"
        )
    else:
        system_prompt = (
            "あなたはデータサイエンスの専門家です。"
            "統計、データ分析、実務での活用例を意識して説明してください。"
        )

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]

    response = llm(messages)
    return response.content


# -----------------------------
# Streamlit 画面構成
# -----------------------------
st.set_page_config(page_title="Streamlit LLMアプリ", page_icon="🤖")

st.title("🤖 Streamlit LLM 専門家アプリ")

st.markdown("""
### このアプリについて
このアプリは **Streamlit** と **LangChain** を使って作成した  
**大規模言語モデル（LLM）搭載Webアプリ**です。

### 使い方
1. AIに担当させたい「専門家タイプ」を選択します  
2. 質問や相談内容を入力します  
3. 「専門家に質問する」ボタンを押すと、AIが回答します
""")

# 専門家タイプ選択（ラジオボタン）
expert_type = st.radio(
    "AIに担当させる専門家を選択してください：",
    ("AIエンジニア", "データサイエンティスト")
)

# ユーザー入力欄
user_input = st.text_area(
    "質問内容を入力してください：",
    placeholder="例：プロンプトエンジニアリングとは何ですか？"
)

# 実行ボタン
if st.button("専門家に質問する"):
    if user_input.strip() == "":
        st.warning("質問内容を入力してください。")
    else:
        with st.spinner("AIが回答を生成中です..."):
            answer = get_llm_response(user_input, expert_type)

        st.subheader("回答結果")
        st.write(answer)
