##imported from  .venv\lib\openai\_client.py
from openai import OpenAI
from dotenv import load_dotenv 
import os
from tools import TOOLS,run_tool  ## importing the functions from tools.py
import json
from types import SimpleNamespace

load_dotenv()  ## check for .env file in the current directory



client = OpenAI(
    base_url=os.getenv("BASE_URL"),                ## ollama port
    api_key=os.getenv("API_KEY")                ## no need for api key since we are using local model
)

messages = []

messages.append(
    {
        "role": "system",
        "content" : """You are a helpful general-purpose AI assistant.You can answer questions about programming, technology,
                    mathematics, science, education, and general knowledge.



                    Use tools only when the user's question requires them.

                    Do not use tools for general knowledge questions that
                    you can answer yourself.

                    If no tool is needed, answer directly.

                    Reply in around 200 words. Also explain you answer in points and with flowcharts if possible like anyone asking for a detailed explanation. If the user asks for a flowchart, provide it in mermaid syntax.
                  """
    }
)

def stream_chat(history):
    stream  = client.chat.completions.create(
                        model=os.getenv("MODEL"),
                        messages=history,
                        stream = True,
                        tools = TOOLS  
                    )

    label_printed = False
    calls = {}
    sorted_calls = []
    response = ""
    for s in stream:
        if not s.choices:
            continue

        piece = s.choices[0].delta

        ##part 1 of getting full_response
        if piece.content:

            if not label_printed:
                print("Assistant:", end="", flush=True)
                label_printed = True

            print(piece.content, end="", flush=True)
            response += piece.content

        ##part2 of getting tool_calls
        if piece.tool_calls:
            for pc in (piece.tool_calls or []):
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
                            calls[pc.index].function.args += pc.function.arguments
    if label_printed:
        print()  ##print a new line after the assistant's response
    for key in sorted(calls.keys()):
        sorted_calls.append(calls[key])
    return response, sorted_calls


def build_tool_calls_payload(tool_calls):
    payload = []
    for tool_call in tool_calls:
        payload.append({
            "id": tool_call.id,
            "type": "function",
            "function": {
                "name": tool_call.function.name,
                "arguments": tool_call.function.args
            }
        })
    return payload

##for response
while True:
    try:
        user_input = input("Enter your message (or type 'exit' to quit): ")

        if user_input.lower() in ["exit","quit"]:
            print("Exiting the program.")
            break

        messages.append(
            {
                "role": "user",
                "content" : user_input
            }
        )

        MAX_CALL = 5
        
        ## chained calling 
        for _ in range(MAX_CALL):

            full_response, tool_calls = stream_chat(messages)
           
            if not tool_calls:
                break 

            messages.append({
                "role": "assistant",
                "content": full_response,
                "tool_calls": build_tool_calls_payload(tool_calls)
            })

            for tool_call in tool_calls:
                tool_result = run_tool(tool_call)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id" : tool_call.id,
                        "content" : str(tool_result)
                                                            }
                )
        else:
            print("Maximum tool calls reached. Please refine your query or try again.")
            continue


    except KeyboardInterrupt:
        print("\nExiting the program.")
        break

    except Exception as e:
        print("An error occurred:", str(e))

        if messages and messages[-1]["role"] == "user":
            messages.pop()  ##remove the last user message if an error occurs
