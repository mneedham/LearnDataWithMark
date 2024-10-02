# Trying out OpenAI Whisper Turbo

## Pre-Requisites

insanely-fast-whisper - https://pypi.org/project/insanely-fast-whisper/
Ollama - https://ollama.com/

## Instructions

Download MP3 file and save as `openai.mp3` - https://anchor.fm/s/f7cac464/podcast/play/92312327/https%3A%2F%2Fd3ctxlq1ktw2nl.cloudfront.net%2Fstaging%2F2024-8-28%2F387196719-44100-2-f0f9be974d84c.mp3


Transcribe the MP3 file:

```
insanely-fast-whisper \
  --file-name openai.mp3 \
  --device-id mps \
  --model-name openai/whisper-large-v3-turbo \
  --batch-size 4 \
  --transcript-path openai.mp3-large.json
```

Ask an LLM what the transcript says. 

```
cat openai.mp3.json |
jq -r '.text' |
ollama run --verbose llama3.1 \
"Above is a podcast transcript. What are your three main takeaways?"
```