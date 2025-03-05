import requests
import json
from util import generateToken
from openai import OpenAI
import os

generateToken()
header_name = os.getenv('GATEWAY_HEADER_NAME')
header_value = os.getenv('GATEWAY_HEADER_VALUE')
headers = {
    header_name: header_value
}
client = OpenAI(default_headers=headers)

#*********Step1: Create a function to get the weather*********
# The function will take latitude and longitude as input and return the current temperature in celsius.
def get_weather(latitude, longitude):
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()
    return data['current']['temperature_2m']

#*********Step2: Call model with functions defined – along with your system and user messages.********
get_weather_schema = {
        "name": "get_weather",
        "description": "Get current temperature for provided coordinates in celsius.",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"}
            },
            "required": ["latitude", "longitude"],
            "additionalProperties": False
        },
        "strict": True
    }

tools = [
    {
        "type": "function",
        "function": get_weather_schema
    }
]

messages = [{"role": "user", "content": "Based on the weather in Pune and Hyderabad, India, can you suggent me the clothing i should wear in respective cities?"}]
completion = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=messages,
    tools=tools
)
messages.append(completion.choices[0].message)  # append model's function call message

for tool_call in completion.choices[0].message.tool_calls:
    args = json.loads(tool_call.function.arguments)
    if (tool_call.function.name == "get_weather"):
        result = get_weather(args["latitude"], args["longitude"])
        messages.append({   # append result message
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })    

completion_2 = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=messages,
    tools=tools,
)

print(completion_2.choices[0].message.content)
