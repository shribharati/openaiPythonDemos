import requests
import json
import os
from util import generateToken
generateToken()

url = os.getenv("OPENAI_BASE_URL") + '/chat/completions';
api_key = os.getenv("OPENAI_API_KEY")
header_name = os.getenv('GATEWAY_HEADER_NAME')
header_value = os.getenv('GATEWAY_HEADER_VALUE')
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}", 
    header_name: header_value
    }
data = {
    "model": "gpt-4o-2024-05-13",
    "messages": [
        {
            "role": "user",
            "content": "What is OpenAI"
        }
    ]
}
response = requests.post(url, headers=headers, data=json.dumps(data))
# Print only the content of the response
response_content = response.json()
print(response_content['choices'][0]['message']['content'])
