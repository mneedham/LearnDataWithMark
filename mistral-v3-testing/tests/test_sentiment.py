from conftest import State
from test_utils import get_test_name, check_function_call
from test_utils import collect_results, get_result_template
from fn_calling import generate_output
import pandas as pd

def test_sentiment(state: State, iterations) -> None:  
  definitions = [{
    "type": "function",
    "function": {
      "name": "extract_sentiment",
      "description": "Get the sentiment for a given review",
      "parameters": {
        "type": "object",
        "properties": {
          "reviews": {
            "type": "array",
            "items":{
              "type": "object",
              "properties": {
                "sentiment": {"type": "string", "description": "Sentiment of the review (positive/negative/neural)"},
                "sentiment_score": {"type": "integer","description": "Score between 1-100 of the sentiment"}
              }
            }
          }
        }
      },
    },
  }]

  reviews_df = pd.read_csv("tests/data/reviews.csv")
  reviews = reviews_df['review'].tolist()

  question = f"""
  {reviews}
  Analyse the sentiment of the reviews above.
  """

  expected_result = [{
    "name": "extract_sentiment",
    "arguments": {"review": [
      {"sentiment": "negative", "sentiment_score": 100},
      {"sentiment": "negative", "sentiment_score": 50},
      {"sentiment": "positive", "sentiment_score": 70},
      {"sentiment": "positive", "sentiment_score": 90},
      {"sentiment": "positive", "sentiment_score": 50},
      {"sentiment": "positive", "sentiment_score": 50}
    ]}
  }]

  test_results_summary = state.state[get_test_name()] = get_result_template()
  for _ in range(0, iterations):
    output = generate_output(question, definitions)
    result = check_function_call(output, expected_result)
    collect_results(test_results_summary, result, output)
