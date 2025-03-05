from util import generateToken
from openai import OpenAI
import os
generateToken()
import json
from pydantic import BaseModel, Field
from enum import Enum
from typing import List

# Get OpenAI Client from Util.
header_name = os.getenv('GATEWAY_HEADER_NAME')
header_value = os.getenv('GATEWAY_HEADER_VALUE')
headers = {
    header_name: header_value
}
client = OpenAI(default_headers=headers)

class ReviewText(str, Enum):
    worst = "worst"
    average = "average"
    best = "best"
    good = "good"
    bad= "bad"

class Review(BaseModel):
    product_summary: List[str] = Field(..., description="A brief summary of the product being reviewed.")
    rating: float = Field(..., description="The rating given to the product, usually on a scale from 1 to 5.")
    rating_text: ReviewText = Field(..., description="The rating given to the product.")
    review_text: str = Field(..., description="The detailed review text provided by the reviewer.")
    reviewer: str = Field(..., description="The name or identifier of the reviewer.")
    IsReview: bool = Field(..., description="True if it is a review, False if it is not a review.")

class ReviewsResponse(BaseModel):
    reviews: List[Review] = Field(..., description="A list of product reviews.")

completion = client.beta.chat.completions.parse(
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
    response_format=ReviewsResponse    
)

# Extract the structured review information
ratings = completion.choices[0].message.parsed
# Display the parsed review information
#ratings_json = json.loads(ratings)
for review in ratings.reviews:
    print(f"Reviewer: {review.reviewer}")
    print(f"Rating: {review.rating}")
    print(f"Rating Text: {review.rating_text}")
    print(f"Review Text: {review.review_text}")
    print(f"Product Summary: {review.product_summary}")
    print(f"Is Review: {review.IsReview}")
    print()

