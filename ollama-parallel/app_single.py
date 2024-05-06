import streamlit as st
from openai import OpenAI

st.title("ChatGPT-like clone")

client = OpenAI(
  base_url="http://localhost:11434/v1",
  api_key="needed-but-ignored"
)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "llama3"

if "messages" not in st.session_state:
    st.session_state.messages = []

# left, right = st.columns(2)

# with left:
#   st.write("Hi")

# with right:
#   st.write("I am ChatGPT")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Message ChatGPT-clone"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

  # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})