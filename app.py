import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
import os

# --- 環境変数を読み込む ---
load_dotenv()

# --- StreamlitのUI ---
st.title("💬 LLM搭載Webアプリ（Streamlit + LangChain）")
st.write("このアプリでは、専門家のタイプを選んでAIに質問できます。")

# --- 専門家の種類を選択 ---
expert = st.radio(
    "AIにどんな専門家として回答してほしいですか？",
    ("心理カウンセラー", "経営コンサルタント", "英会話講師")
)

# --- 質問入力 ---
user_input = st.text_area("あなたの質問を入力してください:")

# --- LLM呼び出し関数 ---
def ask_ai(role, question):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    system_message = SystemMessage(content=f"あなたは優秀な{role}です。")
    user_message = HumanMessage(content=question)
    response = llm.invoke([system_message, user_message])
    return response.content

# --- 実行ボタン ---
if st.button("AIに聞く"):
    if not user_input:
        st.warning("⚠️ 質問を入力してください。")
    elif not os.getenv("OPENAI_API_KEY"):
        st.error("❌ OpenAI APIキーが設定されていません。")
    else:
        with st.spinner("AIが考えています..."):
            answer = ask_ai(expert, user_input)
            st.success("✅ 回答:")
            st.write(answer)

