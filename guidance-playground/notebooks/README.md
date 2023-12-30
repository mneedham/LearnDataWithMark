# Guidance AI

[Guidance](https://github.com/guidance-ai/guidance) lets us constraint generation and interleave control and generation when working with Large Language Models.

You can [download the Mistral-7B model from Hugging Face](https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF) and put it in the `notebooks/models` directory. I used the one named `mistral-7b-instruct-v0.1.Q4_K_M.gguf`. If you use another one, you'll need to tweak the notebook code to use the new model.

Set up a Python virtual environment

```bash
python -m venv .venv
source .venv/bin/active
```

Install dependencies

```bash
pip install -r requirements.txt
```

Launch the notebook

```bash
jupyter lab --notebook-dir notebooks
```
