from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()  ## check for .env file in the current directory
import os

client = OpenAI(
    base_url=os.getenv("BASE_URL"),                ## ollama port
    api_key=os.getenv("API_KEY")                ## no need for api key since we are
)

emb = client.embeddings.create(
    model=os.getenv("EMBEDDING_MODEL"),
    input="This is a test embedding"
)

print(emb.data[0].embedding[:10])  ## print the first 10 values of the embedding vector
print(len(emb.data[0].embedding))  ## print the length of the embedding vector