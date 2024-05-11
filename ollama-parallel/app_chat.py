import streamlit as st
from openai import OpenAI
import threading

st.set_page_config(layout="wide")
st.title("ChatGPT-like clone")

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="needed-but-ignored"
)

# Initialize session state for left and right if not already done
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "llama3"
if "right" not in st.session_state:
    st.session_state["right"] = {"messages": [], "latest": None}
if "left" not in st.session_state:
    st.session_state["left"] = {"messages": [], "latest": None}

left, right = st.columns(2)

def update_stream(side, messages):
    if side == "left":
        stream = client.chat.completions.create(
            model="phi3",
            messages=[{"role": m["role"], "content": m["content"]} for m in messages],
            stream=True,
        )
    elif side == "right":
        stream = client.chat.completions.create(
            model="llama3",
            messages=[{"role": m["role"], "content": m["content"]} for m in messages],
            stream=True,
        )
    return stream

def handle_streams():
    threads = []
    results = {}

    # Create threads with local copies of messages
    for side in ["left", "right"]:
        messages = st.session_state[side]["messages"]
        thread = threading.Thread(target=lambda s, m: results.update({s: update_stream(s, m)}), args=(side, messages))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Update session state with results after all threads have completed
    for side in ["left", "right"]:
        st.session_state[side]["latest"] = results[side]
    st.rerun()


with left:
    st.write("Model 1")
    messages = st.container(height=600)
    for message in st.session_state.left["messages"]:
        messages.chat_message(message['role']).write(message['content'])

    if st.session_state.left["latest"]:
        full_response = messages.chat_message("assistant").write_stream(st.session_state.left["latest"])
        st.session_state.left["messages"].append({"role": "assistant", "content": full_response})
        st.session_state.left["latest"] = None

with right:
    st.write("Model 2")
    messages = st.container(height=600)
    for message in st.session_state.right["messages"]:
        messages.chat_message(message['role']).write(message['content'])

    if st.session_state.right["latest"]:
        full_response = messages.chat_message("assistant").write_stream(st.session_state.right["latest"])
        st.session_state.right["messages"].append({"role": "assistant", "content": full_response})
        st.session_state.right["latest"] = None

if prompt := st.chat_input("Say something", key="chat"):
    st.session_state.left["messages"].append({"role": "user", "content": prompt})
    st.session_state.right["messages"].append({"role": "user", "content": prompt})

    print(st.session_state)
    handle_streams()
