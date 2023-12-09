import requests
import json
import io
import base64

from rich import print
from PIL import Image


class LLAVA:
    DEFAULT_PROMPT = """A chat between a curious human and an artificial intelligence assistant. 
The assistant gives helpful, detailed, and polite answers to the human's questions.
USER:[img-10]
ASSISTANT:
    """

    def __init__(self):
        self.url = 'http://127.0.0.1:8080/completion'

        self.parameters = {
            "stream": True,
            "n_predict": 400,
            "temperature": 0.2,
            "stop": ["</s>", "Llama:", "User:"],
            "repeat_last_n": 256,
            "repeat_penalty": 1.18,
            "top_k": 40,
            "top_p": 0.7,
            "tfs_z": 1,
            "typical_p": 1,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "mirostat": 0,
            "mirostat_tau": 5,
            "mirostat_eta": 0.1,
            "grammar": "",
            "n_probs": 0,
            "cache_prompt": True,
            "slot_id": -1,
        }

    def complete(self, image_path, prompt=DEFAULT_PROMPT):
        with Image.open(image_path) as img:
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format=img.format)
            encoded_img_bytes = base64.b64encode(
                img_byte_arr.getvalue()).decode('utf-8')

        data = self.parameters | {
            "prompt": prompt,
            "image_data": [{"data": encoded_img_bytes, "id": 10}]
        }

        response = requests.post(
            url=self.url,
            headers={'Accept': 'text/event-stream' },
            data=json.dumps(data),
            stream=True
        )

        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    json_str = line_str[6:]
                    try:
                        json_data = json.loads(json_str)
                        print(json_data["content"], end="")
                    except json.JSONDecodeError:
                        pass
        print("")
