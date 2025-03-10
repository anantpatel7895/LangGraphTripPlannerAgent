import time
import litellm
import re
import json

def process_llm_output_details(text):
    pattern = re.compile(r"(Thought|Action|Action Input|Observation):\s*(.*?)(?=(?:\n[A-Z]|$))", re.DOTALL)
    
    extracted_data = []
    current_entry = {}
    
    for match in pattern.finditer(text):
        key = match.group(1)
        value = match.group(2).strip()
        
        if key == "Thought" and current_entry:
            if all(k in current_entry for k in ["Thought", "Action", "Action Input", "Observation"]):
                extracted_data.append(current_entry)
            current_entry = {}
        
        if key == "Action Input":
            try:
                value = json.loads(value)  # Convert to dictionary if valid JSON
            except json.JSONDecodeError:
                pass  # Keep as string if not JSON format
        
        current_entry[key] = value
    
    if all(k in current_entry for k in ["Thought", "Action", "Action Input", "Observation"]):
        extracted_data.append(current_entry)
    
    return extracted_data



def call_groq_llm(agent, conversation, max_api_call_try=3):
    for attempt in range(max_api_call_try):  # Retry up to 3 times
        try:
            response = agent.get_response(conversation)
            return response
        except litellm.exceptions.RateLimitError as e:
            wait_time = 400  # Default 6-7 minutes wait
            if "try again in" in str(e):
                wait_time = int(float(e.args[0].split("try again in ")[1].split("s")[0])) + 5
            print(f"Rate limit hit. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    raise Exception("Rate limit exceeded too many times, please try later.")

