import ollama
import streamlit as st
import asyncio
import base64
from ollama import AsyncClient
from utils import style_page

def reset_messages():
  st.session_state.messages = []
  for index in range(0, len(models)):
    st.session_state.messages.append([])
  st.session_state.last_image = None


async def run_prompt(placeholder, model, message_history):
    with placeholder.container():
        for message in message_history:
            if 'content' in message:
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
          if 'content' in message:
            chat_entry = st.chat_message(name=message['role'])          
            chat_entry.write(message['content'])      
    
    stream = await AsyncClient().chat(model=model, stream=True, messages=message_history)

    streamed_text = ""
    time_taken = None
    async for part in stream:
      chunk_content= part['message']['content']      
      if chunk_content is not None:
        if part['done']:
          print(part)
          eval_rate = part['eval_count']/ (part['eval_duration']/1_000_000_000)
          time_taken = f"\n\n---\n\n:blue[Prompt eval duration: {part['prompt_eval_duration']/1_000_000_000:.2f} secs] | :blue[Total duration: {part['total_duration']/1_000_000_000:.2f} secs] | :blue[Tokens/sec: {eval_rate:.2f}]"
        streamed_text = streamed_text + chunk_content
        with placeholder.container():
            for message in message_history:
              if 'content' in message:
                chat_entry = st.chat_message(name=message['role'])                
                chat_entry.write(message['content'])
            assistant = st.chat_message(name="assistant")
            if time_taken is not None:
              assistant.write(streamed_text + time_taken, unsafe_allow_html=True)
            else: 
              assistant.write(streamed_text)
                   
    message_history.append({"role": "assistant", "content": streamed_text})


async def main():
    await asyncio.gather(
        *[
          run_prompt(all_body[index],  model=model, message_history=st.session_state.messages[index])
          for index, model in enumerate(models)  
        ]        
    )


title = "🆚 Comparing LMMs"
st.set_page_config(page_title=title, layout="wide")
style_page()
st.title(title)

models = ['gemma3:4b', 'gemma3:12b']

if not "messages" in st.session_state:
  reset_messages()

with st.sidebar:
    prompt = st.chat_input("What is up?", accept_file=True, file_type=["jpg", "jpeg", "png"],)
    if prompt and prompt["files"]:
      bytes_data = prompt["files"][0]
      st.session_state.last_image = bytes_data
      st.image(bytes_data)
    else: 
      if st.session_state.last_image is not None:
        st.image(st.session_state.last_image)

columns = st.columns(len(models))
all_meta = [col.empty() for col in columns]
all_body = [col.empty() for col in columns]

for index, meta in enumerate(all_meta):
  colour = "red" if index == 0 else "green"
  name = models[index].replace(":", "\\:")
  meta.write(f"## :{colour}[{name}]")

if len(st.session_state.messages[0]) > 0:
    for index in range(0, len(models)):
        with all_body[index].container():
            for message in st.session_state.messages[index]:
                if 'content' in message:
                  chat_entry = st.chat_message(name=message['role'])
                  chat_entry.write(message['content'])

if prompt:
    if prompt == "":
        st.warning("Please enter a prompt")
    else:
        for index in range(0, len(models)):
          if prompt["files"]:
            st.session_state.messages[index].append({"role": "user", "images": [bytes_data]})
          st.session_state.messages[index].append({"role": "user", "content": prompt.text})

        asyncio.run(main())
