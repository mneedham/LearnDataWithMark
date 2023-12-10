# LLaVA: Large Language and Vision Assistant

1. Download [llamafile](https://github.com/Mozilla-Ocho/llamafile)

```bash
chmod +x llava-v1.5-7b-q4-server.llamafile
./llava-v1.5-7b-q4-server.llamafile
```

The server will come up on localhost:8080

2. Download [one or more of the Parquet files](https://huggingface.co/datasets/vivym/midjourney-messages/tree/main/data) from MidJourney messages.

3. Run Streamlit

```bash
poetry run streamlit run app.py
```

That server will come up on localhost:8501
