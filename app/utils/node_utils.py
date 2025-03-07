import time
import litellm

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

