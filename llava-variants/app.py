import ollama
import streamlit as st
import asyncio
import base64
from ollama import AsyncClient

def style_page():
  st.html("""
  <style>
  hr {
      margin: -0.5em 0 0 0;
      background-color: red;
  }
  p.prompt {
      margin: 0;
      font-size: 14px;
  }

  img.spinner {
      margin: 0 0 0 0;
  }

  div.block-container {
    padding-top: 2rem;
  }

  ul[data-testid="stSidebarNavItems"] {
    padding-top: 3.5rem;
  }
  </style>
  """)

def reset_messages():
  st.session_state.messages = []
  for index in range(0, len(models)):
    st.session_state.messages.append([])

title = "🆚 Comparing LMMs"
st.set_page_config(page_title=title, layout="wide")
style_page()
st.title(title)

with st.sidebar:
    uploaded_file = st.file_uploader("Choose a file", type=["png", "jpg"], on_change=reset_messages)
    if uploaded_file:
        bytes_data = uploaded_file.getvalue()
        st.image(bytes_data)
        prompt = st.chat_input("Message Ollama")

models = ['llava:v1.6', 'llava-llama3', 'llava-phi3']

if not "messages" in st.session_state:
  reset_messages()

model_1, model_2, model_3 = models

columns = st.columns(len(models))
all_meta = [col.empty() for col in columns]
all_body = [col.empty() for col in columns]

for index, meta in enumerate(all_meta):
  colour = "red" if index == 0 else "blue"
  meta.write(f"## :{colour}[{models[index].replace(":", "\\:")}]")

if len(st.session_state.messages[0]) > 0:
    for index in range(0, len(models)):
        with all_body[index].container():
            for message in st.session_state.messages[index]:
                chat_entry = st.chat_message(name=message['role'])
                chat_entry.write(message['content'])


async def run_prompt(placeholder, model, message_history):
    with placeholder.container():
        for message in message_history:
            chat_entry = st.chat_message(name=message['role'])
            chat_entry.write(message['content'])
        assistant = st.chat_message(name="assistant")

        with open("images/loading.gif", "rb") as file:
            contents = file.read()
            data_url = base64.b64encode(contents).decode("utf-8")

        assistant.html(f"<img src='data:image/gif;base64,{data_url}' class='spinner' width='25' />")

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        *message_history
    ]

    with placeholder.container():
      for message in message_history:
          chat_entry = st.chat_message(name=message['role'])
          chat_entry.write(message['content'])      

    
    stream = await AsyncClient().generate(model=model, images=[bytes_data], prompt=prompt, stream=True)
    streamed_text = ""
    async for part in stream:
      chunk_content = part['response']
      if chunk_content is not None:
        streamed_text = streamed_text + chunk_content
        with placeholder.container():
            for message in message_history:
                chat_entry = st.chat_message(name=message['role'])
                chat_entry.write(message['content'])
            assistant = st.chat_message(name="assistant")
            assistant.write(streamed_text)
                   
    message_history.append({"role": "assistant", "content": streamed_text})


async def main():
    await asyncio.gather(
        *[
          run_prompt(all_body[index],  model=model, message_history=st.session_state.messages[index])
          for index, model in enumerate(models)  
        ]        
    )


if uploaded_file and prompt:
    if prompt == "":
        st.warning("Please enter a prompt")
    else:
        for index in range(0, len(models)):
          st.session_state.messages[index].append({"role": "user", "content": prompt})

        asyncio.run(main())
