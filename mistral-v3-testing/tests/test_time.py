from conftest import State
from test_utils import get_test_name, check_function_call
from test_utils import collect_results, get_result_template
from fn_calling import generate_output

def test_time(state: State, iterations) -> None:  
  definitions = [{
    "type": "function",
    "function": {
      "name": "get_time",
      "description": "Get the current time in a timezone, inferred from the place.",
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

  question = "What is the time in San Francisco?"

  expected_result = [{
    "name": "get_time",
    "arguments": {"timezone": "America/Los_Angeles"}
  }]

  test_results_summary = state.state[get_test_name()] = get_result_template()
  for _ in range(0, iterations):
    output = generate_output(question, definitions)
    result = check_function_call(output, expected_result)
    collect_results(test_results_summary, result, output)
