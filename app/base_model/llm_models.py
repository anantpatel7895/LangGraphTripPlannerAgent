from typing_extensions import TypedDict, Annotated
from operator import add
from pydantic import BaseModel
from typing import Dict, List

models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it"]

class CitySearchModel(BaseModel):
    model:str=models[0]
    max_tokens:int=4000


class LocalExpertModel(BaseModel):
    model:str=models[2]


class TripSummarizer(BaseModel):
    model:str=models[0]


class InputVariable(BaseModel):
    origin_city:str
    destinations:str
    traveller_interests:str


class GraphState(TypedDict):
    city_planner_chat_history:List
    city_local_expert_chat_history:Annotated[List, add]
    trip_summarizer_chat_history:Annotated[List, add]
    processed_tool_call_llm_response:List
    inputs:InputVariable
    tool_call_by_content:bool


class TripAdvisorState(TypedDict):
    chat_history:Annotated[list, add]
    origin_city:str
    destination_city:str


class ReactGraphState(TypedDict):
    tool_call_by_content:bool
    inputs:InputVariable
    city_planner_chat_history:List
    processed_tool_call_llm_response:List
    
    