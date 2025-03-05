from util import generateToken
from openai import OpenAI
import os
import numpy as np

generateToken()
header_name = os.getenv('GATEWAY_HEADER_NAME')
header_value = os.getenv('GATEWAY_HEADER_VALUE')
headers = {
    header_name: header_value
}
client = OpenAI(default_headers=headers)

response = client.embeddings.create(
  input=["I do programming and I am a programmer", "I am a software architect"],
  model="text-embedding-3-large",
)
#print(response.data[0].embedding)
#print(response.data[1].embedding)

#Calculate Cosine Similariy
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

#Calculate Euclidean distance
def euclidean_distance(a,b):
    return np.linalg.norm(np.array(a) - np.array(b))

print("Cosine Similarity:", cosine_similarity(response.data[0].embedding, response.data[1].embedding))
print("Euclidean Distance:", euclidean_distance(response.data[0].embedding, response.data[1].embedding))
