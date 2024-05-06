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
  left_messages = st.container(height=300)
  for message in st.session_state.left_messages:
      with st.chat_message(message["role"]):
          st.markdown(message["content"])

with right:
  right_messages = st.container(height=300)
  for message in st.session_state.right_messages:
      with st.chat_message(message["role"]):
          st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Message ChatGPT-clone"):
    # Add user message to chat history    
    st.session_state.left_messages.append({"role": "user", "content": prompt})
    st.session_state.right_messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

  # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.left_messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.right_messages.append({"role": "assistant", "content": response})
    st.session_state.left_messages.append({"role": "assistant", "content": response})