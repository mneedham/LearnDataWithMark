# Analysing and clustering YouTube comments

This is a Streamlit app that lets you analyse YouTube comments for a given video.
I also wrote [a blog post](https://www.markhneedham.com/blog/2024/02/27/clustering-youtube-comments-ollama-embeddings-nomic/) walking through how it works. 

## Pre requisites

You'll need to have a YouTube API key and have [Ollama](https://ollama.com/) installed locally.
The other dependenciese are in [pyproject.tom](pyproject.toml)

## Running the app

The code is in [app.py](app.py). You can run it like this:

```bash
poetry run streamlit run app.py
```
