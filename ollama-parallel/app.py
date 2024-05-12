import ollama
import streamlit as st
import asyncio
import time
from openai import AsyncOpenAI
from token_count import TokenCount

title = "Running LLMs in parallel with Ollama"
st.set_page_config(page_title=title, layout="wide")
st.title(title)

if not "messages1" in st.session_state:
    st.session_state.messages1 = []

if not "messages2" in st.session_state:
    st.session_state.messages2 = []

st.write(st.session_state.messages1)
st.write(st.session_state.messages2)

client = AsyncOpenAI(base_url="http://localhost:11434/v1", api_key="ignore-me")

models = [
    m['name'] 
    for m in ollama.list()["models"]  
    if m["details"]["family"] in ["llama", "gemma"]
]

with st.sidebar:
    prompt = st.text_area("Prompt")
    model_1_index = models.index("phi3:latest")
    model_1 = st.selectbox("Model 1", options=models, index=model_1_index)
    model_2_index = models.index("llama3:latest")
    model_2 = st.selectbox("Model 2", options=models, index=model_2_index)
    generate = st.button("Generate", type="primary")

col1, col2 = st.columns(2)
col1.write(f"# :blue[{model_1}]")
col2.write(f"# :red[{model_2}]")

body_1 = col1.empty()
body_2 = col2.empty()


async def run_prompt(placeholder, prompt, model, message_history):
    with placeholder.container():
        user = st.chat_message(name="user")
        user.write(prompt)    


    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        *message_history,
        {"role": "user", "content": prompt},
    ]
    stream = await client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True
    )
    streamed_text = ""
    async for chunk in stream:
        chunk_content = chunk.choices[0].delta.content
        if chunk_content is not None:
            streamed_text = streamed_text + chunk_content
            with placeholder.container():
                user = st.chat_message(name="user")
                user.write(prompt)
                assistant = st.chat_message(name="assistant")
                assistant.write(streamed_text)
    message_history.append({"role": "assistant", "content": streamed_text})
                


async def main():
    await asyncio.gather(
        run_prompt(body_1, prompt=prompt, model=model_1, message_history=st.session_state.messages1),
        run_prompt(body_2, prompt=prompt, model=model_2, message_history=st.session_state.messages2)
    )

if generate:
    if prompt == "":
        st.warning("Please enter a prompt")
    else:
        st.session_state.messages1.append({"role": "user", "content": prompt})
        st.session_state.messages2.append({"role": "user", "content": prompt})
        asyncio.run(main())
