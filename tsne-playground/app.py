import time
import help
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.manifold import TSNE
from datasets import load_dataset

st.set_page_config(layout="wide")
st.markdown("""
<style>
.block-container, div[data-testid="stSidebarUserContent"]
{
    padding-top: 0rem;
    padding-bottom: 0.5rem;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("YouTube Comment Analysis")
    df = load_dataset("markhneedham/youtube-comments")['train'].to_pandas()
    video_id = st.selectbox(
        label='Select a video',
        options=df.videoId,
        format_func=lambda record: df[df.videoId == record].title.iloc[0]
    )
    st.components.v1.iframe(
        f"https://www.youtube.com/embed/{video_id}", height=200)

    metrics = [
        'braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation',
        'cosine', 'dice', 'euclidean', 'hamming', 'haversine',
        'jaccard', 'l1', 'l2', 'mahalanobis', 'manhattan',
        'matching', 'minkowski', 'nan_euclidean', 'precomputed', 'rogerstanimoto',
        'russellrao', 'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean',
        'wminkowski', 'yule'
    ]
    metric = st.selectbox(label="Metric", options=metrics,
                          index=metrics.index("euclidean"), help=help.metric)
    n_iter = st.number_input('Number of iterations',
                             value=1000, help=help.n_iter)
    perplexity = st.number_input('Perplexity', value=30, help=help.perplexity)
    method = st.selectbox(label="Method", options=[
                          "barnes_hut", "exact"], index=0, help=help.method)
    pressed = st.button("Visualise Comments", type="primary")

comments = df[df.videoId == video_id].comments.iloc[0]
all_comments = [c['text'] for c in comments]
embeddings = [c['embedding'] for c in comments]

st.markdown(f"""
#### {df[df.videoId == video_id].title.iloc[0]} 
*{len(all_comments)} comments*
""")

if pressed:
    with st.spinner('Running...'):
        start = time.time()
        tsne = TSNE(n_components=2, metric=metric, n_iter=n_iter,
                    perplexity=perplexity, method=method)
        tsne_results = tsne.fit_transform(np.array(embeddings))
        df = pd.DataFrame(tsne_results, columns=['x', 'y'])
        df["comments"] = all_comments

        fig = go.Figure(data=go.Scatter(
            x=df['x'],
            y=df['y'],
            marker=dict(colorscale='Jet', size=12),
            mode='markers',
            hovertemplate='%{hovertext}',
            hovertext=df.comments.str.wrap(50).apply(
                lambda x: x.replace('\n', '<br>'))
        ))
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=630
        )
        st.plotly_chart(fig, use_container_width=True)
        end = time.time()
        st.write(f":red[Rendered in **{end-start:.2f} seconds**]")
