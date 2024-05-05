import requests
import json

audio_path = (
    "https://dts.podtrac.com/redirect.mp3/www.buzzsprout.com/"
    "682433/14949591-2024-artificial-intelligence-index.mp3"
)
payload = {"audio_path": audio_path}

headers = {
  "Accept": "*/*",
  "Accept-Encoding": "gzip, deflate",
  "Authorization": "Basic <your-base64-encoded-token>",
  "Connection": "keep-alive",
  "Content-Type": "application/json"
}

url = "https://<your-app>.apps.beam.cloud"

response = requests.request("POST", url, 
  headers=headers,
  data=json.dumps(payload)
)

print(response)
data = response.json()

with open('data/ai.json', 'w') as file:
  json.dump(data, file)
