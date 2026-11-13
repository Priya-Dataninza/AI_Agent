from datetime import datetime
import json

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_current_weather(city):
    # Placeholder for actual weather fetching logic
    return f"The current weather in {city} is sunny with a temperature of 25°C."

def get_user_city():
    return "Bangalore"


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current time",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": (
                'Get the current weather for a given city '
                'if the user asks for "my current weather" '
                'or weather in a specific city.'
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city to get the weather for"
                    }
                },
                "required": ["city"],
            },
        
        }
    },
    {
        "type" : "function",
        "function" : {
            "name" : "get_user_city",
            "description" : "Get the user's city",
            "parameters" : {
                "type" : "object",
                "properties" : {},
            }
        }
    }
]


###making a function to get the current time and weather for a given city

FUNCTIONS_MAPPING = {
    "get_current_time": get_current_time,
    "get_current_weather": get_current_weather,
    "get_user_city": get_user_city
}


def run_tool(tool_call):
    tool_name = tool_call.function.name
    tool_args = json.loads(tool_call.function.arguments or '{}')

    fn = FUNCTIONS_MAPPING.get(tool_name)
    if fn:
        try:
            tool_result = fn(**tool_args)
        except Exception as e:
            print("An error occurred while calling the tool:", str(e))
            tool_result = f"Error occurred while calling the tool {tool_name}."
    else:
        tool_result = f"No function found for tool: {tool_name}"

    return tool_result
