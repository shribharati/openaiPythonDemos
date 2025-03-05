from util import generateToken
from openai import OpenAI
import os
generateToken()

# Make the API call
header_name = os.getenv('GATEWAY_HEADER_NAME')
header_value = os.getenv('GATEWAY_HEADER_VALUE')
headers = {
    header_name: header_value
 }
client = OpenAI(default_headers=headers)


system_message = """
Give me output in this format for queries related to product {
  "product": {
    "id": "string",                 // Unique product identifier
    "name": "string",               // Product name
    "brand": "string",              // Product brand
    "category": "string",           // Product category
    "price": {                      // Product price information
      "value": "number",            // Price value
      "currency": "string"          // Currency code (e.g., USD)
    },
    "availability": {               // Product availability
      "status": "string",           // In Stock, Out of Stock
      "quantity": "number"          // Quantity available
    },
    "rating": {                     // Product rating
      "average_rating": "number",   // Average rating
      "review_count": "number"      // Number of reviews
    },
    "summary": "string",            // Short product summary
    "description": "string",        // Product description
    "features": [                   // Key product features
      "string"
    ],
    "specifications": {             // Product specifications
      "weight": "string",           // Weight
      "dimensions": "string"       // Dimensions
    },
    "images": [                     // Product image URLs
      "string"
    ],
    "customer_reviews": [           // Customer reviews
      {
        "reviewer_name": "string",  // Customer's name
        "rating": "number"         // Rating given
      }
    ]
  }
}

"""
# Define the messages
messages = [
    {    
        "role": "system_message",
        "content": system_message
    },
    {
        "role": "user",
        "content": "Hi How are you."
    }
]

messages[1]["content"] = input("enter your promt");

completion = client.chat.completions.create(  
    model="gpt-4o-2024-05-13",
    messages=messages,
)
# Print the response
print(completion.choices[0].message.content)
