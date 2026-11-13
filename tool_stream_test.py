from openai import OPENAI
import os
from dotenv import load_dotenv
load_dotenv()
from tools import TOOLS
from types import SimpleNamespace

client = OPENAI(
    base_url=os.getenv("BASE_URL"), 
    api_key=os.getenv("API_KEY")
)

messages = {"role":"user", "content":"What is weather of my today."}
response = ""
stream  = client.chat.completions.create(
                        model=os.getenv("MODEL"),
                        messages=messages,
                        tools  = TOOLS,  ### passing tools to the model so that it can call the functions when needed
                        stream = True   
                    )

calls = {}
for s in stream:
    piece = s.choices[0].delta
    for pc in (piece.tool_call or []):
        if pc:
            if pc.index not in calls:
                calls[pc.index] = SimpleNamespace(
                    id = "",  
                    function = SimpleNamespace(
                        name = "",
                        args = ""
                    )
                )

            if pc.id:
                calls[pc.index].id = pc.id
            if pc.function and pc.function.name:
                calls[pc.index].function.name = pc.function.name
            if pc.function and pc.function.arguments:
                calls[pc.index].function.args = pc.function.arguments
            
            print(piece.content, end="", flush=True)

sorted_calls = []
for key in sorted(calls.keys()):
    sorted_calls.append(calls[key])

            


