import inspect
import json
import re


from typing import Any, Callable, get_origin, Dict


# Define a custom marker type for runtime parameters
class RuntimeParam:
    """Marker for parameters that will be passed at runtime."""
    pass


def function_callling_to_json_schema(func: Callable) -> dict:
    """Convert a Python function into a JSON schema for OpenAI function calling."""
    signature = inspect.signature(func)
    docstring = func.__doc__ if func.__doc__ else ""
    
    # Extract function description without args section
    function_description = re.split(r"\n\s*args:\s*", docstring, maxsplit=1)[0].strip()
    
    schema = {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": function_description,
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
    
    required_params = []
    param_descriptions = {}
    
    # Extract parameter descriptions
    match = re.search(r"args:\s*(.*)", docstring, re.DOTALL)
    if match:
        param_lines = match.group(1).split("\n")
        for line in param_lines:
            line = line.strip()
            if ":" in line:
                param_name, param_desc = map(str.strip, line.split(":", 1))
                param_descriptions[param_name] = param_desc
    
    for param_name, param in signature.parameters.items():
        # Skip parameters marked with RuntimeParam

        # print(param_name, " : ", param)
        # if param.annotation == RuntimeParam:
        #     continue
        
        param_type = param.annotation if param.annotation != inspect.Parameter.empty else Any
        
        # Handle generic types
        origin_type = get_origin(param_type) or param_type
        json_type = "string"  # Default type
        
        if origin_type in [int, float]:
            json_type = "number"
        elif origin_type == bool:
            json_type = "boolean"
        elif origin_type in [list, tuple]:
            json_type = "array"
        elif origin_type == dict:
            json_type = "object"
        
        param_description = param_descriptions.get(param_name, "No description provided.")
        if param.default != inspect.Parameter.empty:
            param_description += f" Default value: {param.default}."
        
        schema["function"]["parameters"]["properties"][param_name] = {
            "type": json_type,
            "description": param_description
        }
        
        if param.default == inspect.Parameter.empty:
            required_params.append(param_name)
    
    if required_params:
        schema["function"]["parameters"]["required"] = required_params
    
    return schema


def llm_input_json_schema(func:Callable) -> dict:
    """Convert a Python function into a JSON schema for OpenAI function calling."""
    signature = inspect.signature(func)
    docstring = func.__doc__ if func.__doc__ else ""
    
    # Extract function description without args section
    function_description = re.split(r"\n\s*args:\s*", docstring, maxsplit=1)[0].strip()
    
    schema = {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": function_description,
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
    
    required_params = []
    param_descriptions = {}
    
    # Extract parameter descriptions
    match = re.search(r"args:\s*(.*)", docstring, re.DOTALL)
    if match:
        param_lines = match.group(1).split("\n")
        for line in param_lines:
            line = line.strip()
            if ":" in line:
                param_name, param_desc = map(str.strip, line.split(":", 1))
                param_descriptions[param_name] = param_desc
    
    for param_name, param in signature.parameters.items():
        # Skip parameters marked with RuntimeParam
        if param.annotation == RuntimeParam:
            continue
        
        param_type = param.annotation if param.annotation != inspect.Parameter.empty else Any
        
        # Handle generic types
        origin_type = get_origin(param_type) or param_type
        json_type = "string"  # Default type
        
        if origin_type in [int, float]:
            json_type = "number"
        elif origin_type == bool:
            json_type = "boolean"
        elif origin_type in [list, tuple]:
            json_type = "array"
        elif origin_type == dict:
            json_type = "object"
        
        param_description = param_descriptions.get(param_name, "No description provided.")
        if param.default != inspect.Parameter.empty:
            param_description += f" Default value: {param.default}."
        
        schema["function"]["parameters"]["properties"][param_name] = {
            "type": json_type,
            "description": param_description
        }
        
        if param.default == inspect.Parameter.empty:
            required_params.append(param_name)
    
    if required_params:
        schema["function"]["parameters"]["required"] = required_params
    
    return schema



# city = "Bhopal"
# lat, lon = get_coordinates(city)
# if lat and lon:
#     print(f"Latitude: {lat}, Longitude: {lon}")
# else:
#     print("Could not find the coordinates.")


import json
from typing import Tuple, Optional

def extract_next_agent_and_query(message_content: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extracts the 'next agent' and 'summarized query' from the given ChatCompletionMessage content.
    
    Args:
        message_content (str): The content of the ChatCompletionMessage.
    
    Returns:
        Tuple[Optional[str], Optional[str]]: A tuple containing (next_agent, summarized_query).
    """
    try:
        # Extract the JSON-like part from the message content
        json_start = message_content.find("{")
        json_part = message_content[json_start:]
        
        # Parse JSON
        extracted_data = json.loads(json_part)
        
        # Retrieve values
        next_agent = extracted_data.get("next agent")
        summarized_query = extracted_data.get("summarized query")
        
        return next_agent, summarized_query

    except (json.JSONDecodeError, AttributeError, ValueError, TypeError):
        return None, None

