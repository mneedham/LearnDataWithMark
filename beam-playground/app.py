from transformers import pipeline
import torch
import time
from beam import App, Runtime, Image

app = App(
  name="audio-to-text",
  runtime=Runtime(
    cpu=1,
    memory="8Gi",
    gpu="T4",
    image=Image(
      python_version="python3.9",
      python_packages=["insanely-fast-whisper", "ffmpeg-python", "rich"],
      commands=["apt update", "apt install ffmpeg -y"]
    ),
  ),
)

def create_pipeline():
  return pipeline(
    "automatic-speech-recognition",
    model="distil-whisper/distil-large-v3",
    torch_dtype=torch.float16,
    device="cuda",
    model_kwargs={"use_flash_attention_2": False}
  )



@app.rest_api(loader=create_pipeline)
def transcript(**inputs):
  pipe = inputs["context"]
  audio_path = inputs["audio_path"] 

  start = time.time()
  print(f"Starting transcription of {audio_path}")
  outputs = pipe(
      audio_path,
      chunk_length_s=30,
      batch_size=4,
      return_timestamps=True
  )
  end = time.time()
  print(f"Time taken: {end-start:.2f} seconds")

  return outputs

if __name__ == "__main__":
  audio_path = (
      "https://dts.podtrac.com/redirect.mp3/www.buzzsprout.com/"
      "682433/14949591-2024-artificial-intelligence-index.mp3"
  )
  transcript(audio_path=audio_path)
