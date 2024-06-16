from conftest import State
from test_utils import get_test_name, check_function_call
from test_utils import collect_results, get_result_template
from fn_calling import generate_output

def test_weather(state: State, iterations) -> None:  
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

  question = "What is the weather like today in New York?"

  expected_result = [{
    "name": "get_current_weather",
    "arguments": {"latitude": 40.7128, "longitude": -74.0060}
  }]

  test_results_summary = state.state[get_test_name()] = get_result_template()
  for _ in range(0, iterations):
    output = generate_output(question, definitions)
    result = check_function_call(output, expected_result)
    collect_results(test_results_summary, result, output)
