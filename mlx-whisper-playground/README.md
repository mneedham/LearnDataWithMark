# mlx_whisper

Install the [uv](https://github.com/astral-sh/uv) Python package manager.

Download the Tech Meme Ride Home podcast from the 10th October 2024

```bash
wget -O techmeme.mp3 "https://rss.art19.com/episodes/3d12c5a5-d5fb-447e-890b-d772e01528e3.mp3"
```

Create transcripts in all the output formats (`json`, `srt`,  `tsv`, `txt`, `vtt`)

```bash
time uv run --with mlx_whisper mlx_whisper \
  --model mlx-community/whisper-turbo \
  --output-dir transcripts \
  --output-format all \
  techmeme.mp3
```

Install llm with llm-ollama

```bash
uv run --with llm --with llm-ollama \
  llm install llm-ollama
```

Summarise the transcript in 3-5 points:

```bash
cat transcripts/techmeme.txt |
  uv run --with llm --with llm-ollama \
  llm -m llama3.2 -o num_ctx 20000 \
  "Summarise this in 3-5 points"
```