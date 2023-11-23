import streamlit as st
import chromadb
import llm
import time
from PIL import Image

# Streamlit config
st.set_page_config(layout="wide")
st.title("Image search engine")

# Enter search term or provide image
option = st.selectbox('How do you want to search?', ('Search Term', 'Image'))
if option == "Search Term":
    uploaded_file = None
    search_term = st.text_input("Enter search term")
else:
    search_term = None
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, width=200)

st.markdown('<hr style="border:1px #00008B; border-style: solid; margin:0;">', 
    unsafe_allow_html=True)

model = llm.get_embedding_model("clip")
chroma_client = chromadb.PersistentClient(path="images.chromadb")
collection = chroma_client.get_collection(name="images")

with st.empty():
    if option and (uploaded_file or search_term):
        start = time.time()
        with st.spinner('Searching'):
            if option == 'Search Term':
                query_embeddings = model.embed(search_term)
            else:
                query_embeddings = model.embed(uploaded_file.getvalue())
            result = collection.query(
                query_embeddings=[query_embeddings],
                n_results=3
            )
        end = time.time()

        metadatas = result["metadatas"][0]
        distances = result["distances"][0]
        with st.container():
            st.write(f"**Results** ({end-start:.2f} seconds)")
            for index, id in enumerate(result["ids"][0]):
                left, right = st.columns([0.5, 0.5])
                with left:
                    st.image(Image.open(metadatas[index]['filePath']), width=500)
                with right:
                    st.markdown(f"""**Id**: {id}  
                        **Distance**: {distances[index]}
                    """)
    else:
        st.write("No results to show. Enter a search term above.")