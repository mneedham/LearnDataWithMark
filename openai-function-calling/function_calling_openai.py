import json
import os
import requests

from openai import OpenAI

client = OpenAI()

def get_current_weather(latitude, longitude):
  """Get the current weather in a given latitude and longitude"""
  base = "https://api.openweathermap.org/data/2.5/weather"
  key = os.environ['WEATHERMAP_API_KEY']
  request_url = f"{base}?lat={latitude}&lon={longitude}&appid={key}&units=metric"
  response = requests.get(request_url)

  result = {
    "latitude": latitude,
    "longitude": longitude,
    **response.json()["main"]
  }

  return json.dumps(result)

def run_conversation(content):
  messages = [{"role": "user", "content": content}]
  tools = [
    {
      "type": "function",
      "function": {
        "name": "get_current_weather",
        "description": "Get the current weather in a given latitude and longitude",
        "parameters": {
          "type": "object",
          "properties": {
            "latitude": {
              "type": "string",
              "description": "The latitude of a place",
            },
            "longitude": {
              "type": "string",
              "description": "The longitude of a place",
            },
          },
          "required": ["latitude", "longitude"],
        },
      },
    }
  ]
  response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=messages,
    tools=tools,
    tool_choice="auto",
  )
  response_message = response.choices[0].message
  tool_calls = response_message.tool_calls

  if tool_calls:
    messages.append(response_message)

    available_functions = {
      "get_current_weather": get_current_weather,
    }
    for tool_call in tool_calls:
      print(f"Function: {tool_call.function.name}")
      print(f"Params:{tool_call.function.arguments}")
      function_name = tool_call.function.name
      function_to_call = available_functions[function_name]
      function_args = json.loads(tool_call.function.arguments)
      function_response = function_to_call(
        latitude=function_args.get("latitude"),
        longitude=function_args.get("longitude"),
      )
      print(f"API: {function_response}")
      messages.append(
        {
          "tool_call_id": tool_call.id,
          "role": "tool",
          "name": function_name,
          "content": function_response,
        }
      )

    second_response = client.chat.completions.create(
      model="gpt-3.5-turbo-0125",
      messages=messages,
      stream=True
    )
    return second_response

if __name__ == "__main__":
  question = "What's the weather like in Paris and San Francisco?"
  response = run_conversation(question)
  for chunk in response:
    print(chunk.choices[0].delta.content or "", end='', flush=True)
