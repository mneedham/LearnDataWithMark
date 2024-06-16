import ollama
import json

def generate_output(question, definitions):
  model = "mistral:7b-instruct-v0.3-fp16"
  prompt = f"""
  [AVAILABLE_TOOLS]{json.dumps(definitions)}[/AVAILABLE_TOOLS]
  [INST] {question} [/INST]
  """
  return ollama.generate(model=model, prompt=prompt, raw=True)["response"]