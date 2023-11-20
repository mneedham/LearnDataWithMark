import streamlit as st
import chromadb
import llm
from PIL import Image
from datetime import datetime

model = llm.get_embedding_model("clip")

chroma_client = chromadb.PersistentClient(path="images.chromadb")
collection = chroma_client.get_collection(name="images")

st.title("Image search engine")

option = st.selectbox(
    'How do you want to search?',
    ('Search Term', 'Image'))

if option == "Search Term":
    uploaded_file = None
    search_term = st.text_input("Enter search term")
else:
    search_term = None
    uploaded_file = st.file_uploader("Or upload an image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, width=200)


st.markdown('<hr style="border:1px solid #00008B; border-style: solid; margin:0;">', unsafe_allow_html=True)


with st.empty():
    if option and (uploaded_file or search_term):
        with st.spinner('Searching'):
            if option == 'Search Term':
                query_embeddings = model.embed(search_term)
            else:
                image = uploaded_file.getvalue()
                query_embeddings = model.embed(image)

            result = collection.query(
                query_embeddings=[query_embeddings],
                n_results=3
            )

        metadatas = result["metadatas"][0]
        distances = result["distances"][0]
        with st.container():
            st.write("**Results**")
            for index, id in enumerate(result["ids"][0]):
                left, right = st.columns([0.3, 0.7])
                with left:
                    st.image(Image.open(metadatas[index]['filePath']), width=200)
                with right:
                    st.markdown(f"""**Id**: {id}  
                        **Distance**: {distances[index]}
                    """)

    else:
        st.write("No results to show. Enter a search term above.")