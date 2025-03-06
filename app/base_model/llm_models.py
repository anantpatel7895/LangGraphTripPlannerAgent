from typing_extensions import TypedDict, Annotated
from operator import add
from pydantic import BaseModel
from typing import Dict

class CitySearchModel(BaseModel):
    model:str="llama-3.3-70b-versatile"

class LocalExpertModel(BaseModel):
    model:str="llama-3.1-8b-instant"

class TripSummarizer(BaseModel):
    model:str="llama-3.3-70b-versatile"


class InputVariable(BaseModel):
    origin_city:str
    destinations:str
    month:str
    number_of_days:str
    traveller_interests:str


class GraphState(TypedDict):
    city_planner_chat_history:Annotated[list, add]
    city_local_expert_chat_history:Annotated[list, add]
    trip_summarizer_chat_history:Annotated[list, add]
    inputs:InputVariable

