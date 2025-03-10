from typing_extensions import TypedDict, Annotated
from operator import add
from pydantic import BaseModel
<<<<<<< HEAD
from typing import Dict, List
=======
from typing import Dict
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5

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
<<<<<<< HEAD
=======
    month:str
    number_of_days:str
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5
    traveller_interests:str


class GraphState(TypedDict):
<<<<<<< HEAD
    city_planner_chat_history:List
    city_local_expert_chat_history:Annotated[List, add]
    trip_summarizer_chat_history:Annotated[List, add]
    processed_tool_call_llm_response:List
=======
    city_planner_chat_history:Annotated[list, add]
    city_local_expert_chat_history:Annotated[list, add]
    trip_summarizer_chat_history:Annotated[list, add]
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5
    inputs:InputVariable
    tool_call_by_content:bool


class TripAdvisorState(TypedDict):
    chat_history:Annotated[list, add]
    origin_city:str
<<<<<<< HEAD
    destination_city:str


class ReactGraphState(TypedDict):
    tool_call_by_content:bool
    inputs:InputVariable
    city_planner_chat_history:List
    processed_tool_call_llm_response:List
    
    
=======
    destination_city:str
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5
