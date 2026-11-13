from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),                ## ollama port
    api_key=os.getenv("API_KEY")                ## no need for api key since we are using local model
)


messages = [{"role":"user", "content":"What is an API tell me in 100 words."}]
response = ""
stream  = client.chat.completions.create(
                        model=os.getenv("MODEL"),
                        messages=messages,
                        stream = True   
                    )

for s in stream:
    if not s.choices:
        continue

    piece = s.choices[0].delta
    if piece.content:
        print(piece.content, end="", flush=True)
        response += piece.content


print("\nDone streaming response.") 
print(response)
            


