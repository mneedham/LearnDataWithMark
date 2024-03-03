import os
import streamlit as st
from pyyoutube import Api
from comments_util import get_all_comment_threads, cosine_similarity
import ollama
import plotly.figure_factory as ff
import numpy as np
from scipy.cluster.hierarchy import linkage, cut_tree, dendrogram
from collections import defaultdict

st.title("YouTube Comment Analysis")
st.markdown("""
<style>
.block-container
{
    padding-top: 1rem;
    padding-bottom: 1rem;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

video_id = st.text_input('Video ID', 'RXDWkiuXtG0')
st.components.v1.iframe(f"https://www.youtube.com/embed/{video_id}", height=350)

API_KEY = os.environ.get("YOUTUBE_API_KEY")
api = Api(api_key=API_KEY)

threads = get_all_comment_threads(api, video_id, per_page=100)

all_comments = [
    item.snippet.topLevelComment.snippet.textDisplay 
    for t in threads for item in t.items
]

@st.cache_data
def create_embeddings(all_comments):
    return [
        ollama.embeddings(model='nomic-embed-text', prompt=comment)['embedding']
        for comment in all_comments
    ]
embeddings = create_embeddings(all_comments)
st.header("Searching Comments")
search_term = st.text_input('Search Term', 'I love this video!')
if search_term:
    with st.status("Searching.....", expanded=True):
        search_embedding = ollama.embeddings(
            model='nomic-embed-text',
            prompt=search_term
        )['embedding']

        results = [
            (comment, cosine_similarity(embedding, search_embedding))
            for comment, embedding in zip(all_comments, embeddings)
        ]
        top_results = sorted(results, key=lambda x: x[1]*-1)[:5]
        for comment, score in top_results:
            st.markdown(f"""{comment}  
            :blue[{score}]""")

st.header("Clusters")
fig = ff.create_dendrogram(np.array(embeddings))
fig.update_layout(margin=dict(l=0, r=20, t=20, b=20))
st.plotly_chart(fig)

number_of_clusters = st.slider('How many clusters?', 2, 20, 5)

def compute_clusters(n_clusters=3):
    complete_clustering = linkage(embeddings, 
        method="complete", metric="cosine")
    cluster_labels = cut_tree(complete_clustering, 
        n_clusters=n_clusters).reshape(-1, )

    groups = defaultdict(list)
    for id, label in zip(all_comments, cluster_labels):
        groups[label].append(id)
    return groups, cluster_labels

with st.status("Computing clusters.....", expanded=True):
    clusters = compute_clusters(n_clusters=number_of_clusters)[0].items()
    sorted_clusters = sorted(clusters, key=lambda x: len(x[1]) * -1)
    for cluster, labels in sorted_clusters:
        st.write(f"Cluster: {cluster} ({len(labels)})")
        st.write(labels)
