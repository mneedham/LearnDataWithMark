import streamlit as st
from openai import OpenAI

st.set_page_config(layout="wide")
st.title("ChatGPT-like clone")

client = OpenAI(
  base_url="http://localhost:11434/v1",
  api_key="needed-but-ignored"
)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "llama3"

if "right_messages" not in st.session_state:
    st.session_state.right_messages = []

if "left_messages" not in st.session_state:
    st.session_state.left_messages = []

left, right = st.columns(2)


with left:
    st.write("Model 1")
    messages = st.container(height=600)
    for message in st.session_state.left_messages:
        messages.chat_message(message['role']).write(message['content'])


with right:
    st.write("Model 2")
    messages = st.container(height=600)
    for message in st.session_state.right_messages:
        messages.chat_message(message['role']).write(message['content'])

if prompt := st.chat_input("Say something", key="chat"):
    st.session_state.left_messages.append({"role": "user", "content": prompt})
    st.session_state.right_messages.append({"role": "user", "content": prompt})

    stream_left = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.left_messages
        ],
        stream=True,
    )

    stream_right = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.left_messages
        ],
        stream=True,
    )
    # response = st.write_stream(stream)

    st.session_state.left_messages.append({"role": "assistant", "content": stream_left})
    st.session_state.right_messages.append({"role": "assistant", "content": stream_right})
    st.rerun()