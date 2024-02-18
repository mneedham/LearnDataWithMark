# SLIM: Small models for specific tasks by LLMWare

LLMware released the SLIM (Structured Language Instruction Model), which do one small task and return a dictionary or text with the result.

* SLIM Models - https://huggingface.co/collections/llmware/slim-models-65a9994ccb5b4fb08e7bb775
* LLMware AI - https://huggingface.co/collections/llmware/slim-models-65a9994ccb5b4fb08e7bb775

```bash
pip install llmware
```

```python
from llmware.configs import LLMWareConfig
from llmware.models import ModelCatalog
```

```python
model_catalog = ModelCatalog()
```

Install all the models

```python
model_catalog.get_llm_toolkit()
```

Get the model installation path

```python
LLMWareConfig.get_model_repo_path()
```

Analyse an Amazon review

```python
text = """The sound quality is okay but the buds are not suitable for the average ear! Both different sizes feel uncomfortable and constantly fall out. Also trouble connecting 1in 3 times so yeah not the greatest purchase"""
```

```python
sentiment = model_catalog.load_model("slim-sentiment-tool")

sentiment.function_call(
  context=text, 
  params=["sentiment"], 
  function="classify",
  get_logits=False
)
```

```python
emotions = model_catalog.load_model("slim-emotions-tool")

emotions.function_call(
  context=text, 
  params=["emotions"], 
  function="classify",
  get_logits=False
)
```

And with the LLMFx API:

```python
from llmware.agents import LLMfx
```

```python
llm_fx = LLMfx(verbose=False)

llm_fx.load_tool("emotions")
llm_fx.load_tool("ratings")
llm_fx.load_tool("sentiment")
```

```python
(
  llm_fx.emotions(text),
  llm_fx.ratings(text),
  llm_fx.sentiment(text)
)
```