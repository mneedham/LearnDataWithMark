import re
import json
import pytest
import ollama
import os


def generate_output(question, definitions):
  model = "mistral:7b-instruct-v0.3-fp16"
  prompt = f"""
  [AVAILABLE_TOOLS]{json.dumps(definitions)}[/AVAILABLE_TOOLS]
  [INST] {question} [/INST]
  """

  return ollama.generate(model=model, prompt=prompt, raw=True)["response"]



def check_function_call(output, expected_result):
  function_call_present = "[TOOL_CALLS]" in output

  pattern = r'\[TOOL_CALLS\] (\[.*?\])'
  match = re.search(pattern, output)
  if match:
    function_call_json = match.group(1)
  else:
    function_call_json = None

  extra_output_present = len(output.split("\n")) > 1

  if function_call_json:
    try:
      function_call_data = json.loads(function_call_json)
      signature_valid = True
      signature_exact_match = function_call_data == expected_result
    except json.decoder.JSONDecodeError:
      signature_valid = False
      signature_exact_match = False
  else:
    signature_valid = False
    signature_exact_match = False

  return {
    "function_call_present": function_call_present,
    "signature_exact_match": signature_exact_match,
    "signature_valid": signature_valid,
    "extra_output_present": extra_output_present
  }


results_summary = {
  "total_runs": 0,
  "signature_exact_match": 0,
  "function_call_present": 0,
  "signature_valid": 0,
  "extra_output_present": 0,
  "output": []
}


def collect_results(result, output):
  if result['function_call_present']:
    results_summary['function_call_present'] += 1
  if result['signature_valid']:
    results_summary['signature_valid'] += 1
  if result['signature_exact_match']:
    results_summary['signature_exact_match'] += 1
  if result['extra_output_present']:
    results_summary['extra_output_present'] += 1
  results_summary['total_runs'] += 1
  results_summary["output"].append(output)


class TestWeather:  
  def test_weather(self, iterations):
    question = "What is the weather like today in New York?"
    definitions = [{
      "type": "function",
      "function": {
        "name": "get_current_weather",
        "description": "Get the current weather in a given latitude and longitude",
        "parameters": {
          "type": "object",
          "properties": {
            "latitude": {
              "type": "number",
              "description": "The latitude of a place",
            },
            "longitude": {
              "type": "number",
              "description": "The longitude of a place",
            },
          },
          "required": ["latitude", "longitude"],
        },
      },
    }]

    expected_result = [{
      "name": "get_current_weather",
      "arguments": {"latitude": 40.7128, "longitude": -74.0060}
    }]

    for _ in range(0, iterations):
      output = generate_output(question, definitions)
      result = check_function_call(output, expected_result)
      collect_results(result, output)


class TestTime:  
  def test_time(self, iterations):
    question = "What is the time in Sydney?"
    definitions = [{
      "type": "function",
      "function": {
        "name": "get_time",
        "description": "Get the current time in a timezone that's inferred from the place name.",
        "parameters": {
          "type": "object",
          "properties": {
            "timezone": {
              "type": "string",
              "description": "The timezone e.g. Indian/Mauritius, US/Pacific, GMT",
            }
          },
          "required": ["timezone"],
        },
      },
    }]

    expected_result = [{
      "name": "get_time",
      "arguments": {"timezone": "America/Los_Angeles"}
    }]

    for _ in range(0, iterations):
      output = generate_output(question, definitions)
      result = check_function_call(output, expected_result)
      collect_results(result, output)


  @pytest.fixture(scope="class", autouse=True)
  def setup_teardown(self):
    yield None
    print(os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' '))
    with open("results.json", "w") as results_file:
      summary = {
        "stats": {
          "total_runs": results_summary["total_runs"],
          "function_call_present": results_summary["function_call_present"],
          "signature_valid": results_summary["signature_valid"],
          "no_extra_output": results_summary["total_runs"] - results_summary["extra_output_present"],
          "signature_exact_match": results_summary["signature_exact_match"]
        },
        "output": results_summary["output"]
      }

      results_file.write(json.dumps(summary, indent=4))