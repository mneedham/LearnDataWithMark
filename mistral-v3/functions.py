import requests
import os
import json

def get_current_weather(latitude, longitude):
  """Get the current weather in a given latitude and longitude"""
  base = "https://api.openweathermap.org/data/2.5/weather"
  key = os.environ['WEATHERMAP_API_KEY']
  request_url = f"{base}?lat={latitude}&lon={longitude}&appid={key}&units=metric"
  response = requests.get(request_url)

  body = response.json()

  if not "main" in body:    
    return json.dumps({
      "latitude": latitude,
      "longitude": longitude,
      "error": body
    })
  else:
    return json.dumps({
      "latitude": latitude,
      "longitude": longitude,
      **body["main"]
    })

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
    }
  ]