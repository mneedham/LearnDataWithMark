import streamlit as st
import pandas as pd

from llava import LLAVA
from streamlit_utils import st_spinner

st.set_page_config(layout="wide")
st.title("LLAVA vs Mid Journey Prompts")

@st.cache_data
def read_midjourney_file():
    return pd.read_parquet("data/000000.parquet")

df = read_midjourney_file()
row = df.sample()
prompt_text = row['content'].values[0]
image_url = row['url'].values[0]

image, prompt, lvm = st.columns(3)

with image:
    st.markdown("## Image")
    st.image(image_url, width=500)

with prompt:
    st.markdown("## Prompt")
    st.markdown(f"{prompt_text}")

with lvm:
    st.markdown("## LLAVA Description")    
    chat_box = st.empty()   
    with chat_box:
        content = ""
        first_chunk_rendered = False
        waiting = st_spinner("Generating description...")
        for chunk in LLAVA().complete(image_path=image_url, stream=True):
            content += f"{chunk}"
            if not first_chunk_rendered:
                first_chunk_rendered = True
                waiting.end()
            chat_box.markdown(content)
