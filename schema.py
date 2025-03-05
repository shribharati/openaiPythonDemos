from util import generateToken
from openai import OpenAI
import os
generateToken()
import json

# Get OpenAI Client from Util.
header_name = os.getenv('GATEWAY_HEADER_NAME')
header_value = os.getenv('GATEWAY_HEADER_VALUE')
print("#################")
print(header_value)
headers = {
    header_name: header_value,
}
client = OpenAI(default_headers=headers)

# Define the JSON Schema for the response
review_schema = {
    "type": "object",
    "properties": {
        "product_summary": {
            "type": "array",
            "items": {
                "type": "string",
            },
            "description": "A brief summary of the product being reviewed.",
        },
        "rating": {
            "type": "number",
            "description": "The rating given to the product, usually on a scale from 1 to 5.",
        },
        "rating_text": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": ["Neutral", "Good", "Best", "Worst", "Bad"],
                "description": "The rating given to the product.",
            },
        },
        "review_text": {
            "type": "string",
            "description": "The detailed review text provided by the reviewer.",
        },
        "reviewer": {
            "type": "string",
            "description": "The name or identifier of the reviewer.",
        },
        "IsReview": {
            "type": "boolean",
            "description": "True if it is a review, False if it is not a review.",
        },
    },
    "required": ["product_summary", "rating", "review_text", "reviewer", "rating_text", "IsReview"],
    "additionalProperties": False,
}
# Use OpenAI's chat completion API with the JSON Schema
reviews_schema = {
    "type": "object",
    "properties": {
        "reviews": {
            "type": "array",
            "items": review_schema,
        },
    },
    "required": ["reviews"],
    "additionalProperties": False,
}

completion = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    temperature=0.1,
    messages=[
        {"role": "system", "content": "Extract the review details. For the missing fields, use N/A."},
        {
            "role": "user",
            "content": """
                the laptop, mouse and keyboard purchased and rated them as best, average and worst respectively. 
                The table is good and comfortable
                The microphone is very good
            """,
        },
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "product_review",
            "strict": True,
            "schema": reviews_schema,
        },
    },
)

# Extract the structured review information
ratings = completion.choices[0].message.content
# Display the parsed review information
ratings_json = json.loads(ratings)
for review in ratings_json["reviews"]:
    print(f"Reviewer: {review['reviewer']}")
    print(f"Rating: {review['rating']}")
    print(f"Rating Text: {review['rating_text']}")
    print(f"Review Text: {review['review_text']}")
    print(f"Product Summary: {review['product_summary']}")
    print(f"Is Review: {review['IsReview']}")
    print()

