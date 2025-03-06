import time

from ..base_model.llm_models import GraphState, CitySearchModel, LocalExpertModel
from ..prompts.city_planner_prompt import langgraph_city_planner_system_prompt, langgraph_city_planner_user_prompt
from ..prompts.city_local_expert_prompt import city_local_expert_system_prompt, city_local_expert_user_prompt
from ..services.general_agent import GeneralAgent
from .tools import WebSearchTool
from ..utils.tool_node import BasicToolNode


tools = [WebSearchTool]
tool_node = BasicToolNode(tools, return_state_args="city_planner_chat_history")

def ChossingCityAgent(state:GraphState):

    conversation = [
        {
            "role":"system",
            "content":langgraph_city_planner_system_prompt

        },
        {
            "role":"user",
            "content":langgraph_city_planner_user_prompt.format(
                origin_city=state["inputs"]["origin_city"],
                destinations=state["inputs"]["destinations"],
                month=state["inputs"]["month"],
                number_of_days=state["inputs"]["number_of_days"],
                interests=state["inputs"]["traveller_interests"]
            )
        } 
    ] + state["city_planner_chat_history"]

    time.sleep(150)

    agent = GeneralAgent(llm_model=CitySearchModel).bind_tools(tools)
    response = agent.get_response(conversation)

    print("response is : ", response)

    return {"city_planner_chat_history":[response]}


local_expert_tool_node = BasicToolNode(tools, return_state_args="city_local_expert_chat_history")

def CityLocalExpertAgent(state:GraphState):

    conversation = [
        {
            "role":"system",
            "content":city_local_expert_system_prompt

        },
        {
            "role":"user",
            "content":city_local_expert_user_prompt.format(
                origin_city=state["inputs"]["origin_city"],
                month=state["inputs"]["month"],
                interests=state["inputs"]["traveller_interests"],
                context_of_agent1=state["city_planner_chat_history"][-1].content
            )
        } 
    ] + state["city_local_expert_chat_history"]

    time.sleep(150)

    agent = GeneralAgent(llm_model=LocalExpertModel).bind_tools(tools)
    response = agent.get_response(conversation)

    print("local agent response is : ", response)

    return {"city_local_expert_chat_history":[response]}


trip_summarizer_tool_node = BasicToolNode(tools, return_state_args="trip_summarizer_chat_history")

def TripSummarizerAgent(state:GraphState):
    conversation = [
        {
            "role":"system",
            "content":city_local_expert_system_prompt

        },
        {
            "role":"user",
            "content":city_local_expert_user_prompt.format(
                origin_city=state["inputs"]["origin_city"],
                month=state["inputs"]["month"],
                interests=state["inputs"]["traveller_interests"],
                context_of_agent1=state["city_local_expert_chat_history"][-1].content
            )
        } 
    ] + state["trip_summarizer_chat_history"]

    time.sleep(150)

    agent = GeneralAgent(llm_model=LocalExpertModel).bind_tools(tools)
    response = agent.get_response(conversation)

    print("local agent response is : ", response)

    return {"trip_summarizer_chat_history":[response]}