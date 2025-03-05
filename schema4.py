from pydantic import BaseModel
from util import generateToken
from openai import OpenAI
import os
generateToken()

# Define the structure for each step
class Step(BaseModel):
    explanation: str
    code_snippet: str

# Define the structure for the overall response
class JavaProgramGuide(BaseModel):
    steps: list[Step]
    final_code: str

header_name = os.getenv('GATEWAY_HEADER_NAME')
header_value = os.getenv('GATEWAY_HEADER_VALUE')
headers = {
    header_name: header_value
}
client = OpenAI(default_headers=headers)

# Use OpenAI's beta chat completion API with a custom response format
completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",  # Specify the model
    messages=[
        {"role": "system", "content": "You are a programming tutor. "},
        {"role": "user", "content": "Provide me with step by step procedure to write a Java program to calculate the factorial of a number."}
    ],
    response_format=JavaProgramGuide,  # Parse response into JavaProgramGuide
)

# Extract the structured guide
java_guide = completion.choices[0].message.parsed

# Display the guide
for step in java_guide.steps:
    print(f"Step Explanation: {step.explanation}")
    print("=============TTT=============")    
    print(f"Code Snippet:\n{step.code_snippet}\n")
print("=============Complete Code=============")
print("Final Java Code:\n", java_guide.final_code)
