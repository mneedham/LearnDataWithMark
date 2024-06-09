import ollama
import json
import time
import functions
from rich.console import Console

c = Console()

available_functions = {
  functions.get_current_weather.__name__: functions.get_current_weather,
}


def extract_function_calls(model, question, fn_definitions):
  prompt = f"""
  [AVAILABLE_TOOLS]{json.dumps(fn_definitions)}[/AVAILABLE_TOOLS]
  [INST] {question} [/INST]
  """
  start = time.time()
  response = ollama.generate(model=model, prompt=prompt, raw=True)
  end = time.time()

  try:
    raw_response = response['response']
    fn_calls = json.loads(raw_response.replace("[TOOL_CALLS] ", ""))
    return raw_response, fn_calls, None, (end-start)
  except Exception as e:
    return raw_response, None, e, (end-start)


def call_function(function_calls, available_functions):
  fn_responses = []
  for call in function_calls:
    fn_to_call = available_functions[call["name"]]
    fn_response = fn_to_call(**call["arguments"])
    fn_responses.append(fn_response)
  return fn_responses


def answer_question(model, question, fn_responses):
  stream = ollama.generate(model=model, stream=True,
    prompt=f"""
    Using the following function responses: f{json.dumps(fn_responses)}
    Answer this question: {question}
  """)
  for chunk in stream:
    c.print(chunk['response'], end='')


model = "mistral:7b-instruct-v0.3-fp16"

question = "What is the weather like today in New York?"
raw, fn_calls, error, time_taken = extract_function_calls(
  model, question, functions.definitions
)

if error:
  c.print(f"Error: {error}\n{raw}", style="red")
  c.print(f"Fn Call Duration: {time_taken:.2f} seconds", style="yellow")
else:
  c.print(f"Function calls: {fn_calls}")
  fn_responses = call_function(fn_calls, available_functions)
  c.print(f"Function responses: {fn_responses}")
  start = time.time()
  answer_question(model, question, fn_responses)
  end = time.time()
  c.print(f"\nFn Call Duration: {time_taken:.2f} seconds", style="yellow")
  c.print(f"Answer Duration: {end-start:.2f} seconds", style="yellow")