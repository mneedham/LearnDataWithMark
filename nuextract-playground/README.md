# NuExtract: Structured extraction

https://ollama.com/library/nuextract[NuExtract^] is a version of phi-3-mini, fine-tuned on a private high-quality synthetic dataset for information extraction. 

```python
from utils import read_file, view
from templates import *
import ollama
import json
```

```python
def create_user_message(template, text):
  return f"""### Template:
  {template}
  ### Text:
  {text}
  """
```

```python
def extract_info(text, template):
  user_message = create_user_message(
    template=json.dumps(template),
    text=text
  )
  return ollama.chat(
    model='nuextract',
    messages=[{'role': 'user', 'content': user_message}],
  )
```

```python
text1 = read_file("data/text1.txt")
response = extract_info(text1, template1)
print(response['message']['content'])
```

```python
text2 = read_file("data/text2.txt")
response = extract_info(text2, template2)
print(response['message']['content'])
```

```python
text3 = read_file("data/text3.txt")
response = extract_info(text3, template3)
print(response['message']['content'])
```

```python
text4 = read_file("data/text4.txt")
response = extract_info(text4, template4)
print(response['message']['content'])
```

```python
text5 = read_file("data/text5.txt")
response = extract_info(text5, template5)
print(response['message']['content'])
```