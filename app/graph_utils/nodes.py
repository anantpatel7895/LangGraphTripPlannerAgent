import time
import litellm

<<<<<<< HEAD
from ..base_model.llm_models import GraphState, CitySearchModel, LocalExpertModel, TripAdvisorState, ReactGraphState

# too calling prompt
# from ..prompts.tool_calling_prompts.city_planner_prompt import langgraph_city_planner_system_prompt, langgraph_city_planner_user_prompt
# from ..prompts.tool_calling_prompts.city_local_expert_prompt import city_local_expert_system_prompt, city_local_expert_user_prompt
# from ..prompts.tool_calling_prompts.trip_summarizer_prompt import trip_summarizer_system_prompt, trip_summarizer_user_prompt
# from ..prompts.tool_calling_prompts.trip_advisor_prompt import trip_advisor_system_prompt, trip_advisor_user_prompt

# react prompt
from ..prompts.react_prompts.city_planner_prompt import langgraph_city_planner_system_prompt, langgraph_city_planner_user_prompt
from ..prompts.react_prompts.city_local_expert_prompt import city_local_expert_system_prompt, city_local_expert_user_prompt
from ..prompts.react_prompts.trip_summarizer_prompt import trip_summarizer_system_prompt, trip_summarizer_user_prompt


=======
from ..base_model.llm_models import GraphState, CitySearchModel, LocalExpertModel, TripAdvisorState
from ..prompts.city_planner_prompt import langgraph_city_planner_system_prompt, langgraph_city_planner_user_prompt
from ..prompts.city_local_expert_prompt import city_local_expert_system_prompt, city_local_expert_user_prompt
from ..prompts.trip_summarizer_prompt import trip_summarizer_system_prompt, trip_summarizer_user_prompt
from ..prompts.trip_advisor_prompt import trip_advisor_system_prompt, trip_advisor_user_prompt
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5
from ..services.general_agent import GeneralAgent
from .tools import WebSearchTool, Calculate, HumanAssistantTool
from ..utils.tool_node import BasicToolNode
from ..utils.tool_utils import extract_tool_calls
<<<<<<< HEAD
from ..utils.node_utils import process_llm_output_details

from ..utils.react_tool_node import ReactToolNode
from ..utils.write_to_json import write_json_to_file
=======
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5


tools = [WebSearchTool]
summarizer_tools = [WebSearchTool]

trip_advisor_tools = [WebSearchTool, HumanAssistantTool]

trip_advisor_tool_node = BasicToolNode(trip_advisor_tools, return_state_args="chat_history")

def TripAssitantAgent(state:TripAdvisorState):
    conversation = [
        {
            "role":"system",
            "content": trip_advisor_system_prompt
        },
        {
            "role":"user",
            "content":trip_advisor_user_prompt.format(
<<<<<<< HEAD
                    name_of_city=state["origin_city"],
=======
                    origin_city=state["origin_city"],
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5
                    destination = state["destination_city"]
            )
        }
    ] + state["chat_history"]


    agent = GeneralAgent(llm_model=CitySearchModel).bind_tools(trip_advisor_tools)
    response = agent.get_response(conversation)

    print("response is : ", response)

    return {"chat_history":[response]}

<<<<<<< HEAD
=======


>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5
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
<<<<<<< HEAD
                name_of_city=state["inputs"]["origin_city"],
                destinations=state["inputs"]["destinations"],
=======
                origin_city=state["inputs"]["origin_city"],
                destinations=state["inputs"]["destinations"],
                month=state["inputs"]["month"],
                number_of_days=state["inputs"]["number_of_days"],
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5
                interests=state["inputs"]["traveller_interests"]
            )
        }
    ] + state["city_planner_chat_history"]

    # time.sleep(150)

<<<<<<< HEAD


=======
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5
    agent = GeneralAgent(llm_model=CitySearchModel).bind_tools(tools)
    response = agent.get_response(conversation)



    # tool_call_in_content = extract_tool_calls(response.content)

    print("response is : ", response)

    # if tool_call_in_content:
    #     return {
    #         "city_planner_chat_history":[response],
    #         "tool_call_by_content":True
    #     }

    # print("response is : ", response)

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
<<<<<<< HEAD
                name_of_city=state["inputs"]["origin_city"],
=======
                origin_city=state["inputs"]["origin_city"],
                month=state["inputs"]["month"],
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5
                interests=state["inputs"]["traveller_interests"],
                context_of_agent1=state["city_planner_chat_history"][-1].content
            )
        } 
    ] + state["city_local_expert_chat_history"]

    # time.sleep(150)

    agent = GeneralAgent(llm_model=LocalExpertModel).bind_tools(tools)
    response = agent.get_response(conversation)

<<<<<<< HEAD
    if response.content:
        while "tool_call" in response.content:
            print("resolving the tool calling error")
            response = agent.get_response(conversation)

=======
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5
    print("local agent response is : ", response)

    return {"city_local_expert_chat_history":[response]}


trip_summarizer_tool_node = BasicToolNode(summarizer_tools, return_state_args="trip_summarizer_chat_history")

def TripSummarizerAgent(state:GraphState):
<<<<<<< HEAD

    # print("context of agent 2: ", state["city_local_expert_chat_history"][-1].content)
=======
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5
    conversation = [
        {
            "role":"system",
            "content":trip_summarizer_system_prompt

        },
<<<<<<< HEAD

        {
            "role":"user",
            "content":trip_summarizer_user_prompt.format(
                name_of_city=state["inputs"]["origin_city"],
=======
        {
            "role":"user",
            "content":trip_summarizer_user_prompt.format(
                origin_city=state["inputs"]["origin_city"],
                number_of_days=state["inputs"]["number_of_days"],
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5
                interests=state["inputs"]["traveller_interests"],
                context_of_agent2=state["city_local_expert_chat_history"][-1].content
            )
        } 
    ] + state["trip_summarizer_chat_history"]

    # time.sleep(150)

    agent = GeneralAgent(llm_model=LocalExpertModel).bind_tools(summarizer_tools)
    response = agent.get_response(conversation)

<<<<<<< HEAD
    if response.content is None:
        while "tool_call" in response.content:
            print("resolving the tool calling error")
            response = agent.get_response(conversation)


    print("summarizer agent response is : ", response)

    return {"trip_summarizer_chat_history":[response]}


# React Agent Parts

rct_tool_node = ReactToolNode([WebSearchTool], return_state_args="processed_tool_call_llm_response")

def ChossingCityReactAgent(state:ReactGraphState):
    print(state.keys())
    if state["city_planner_chat_history"]:
        conversation = state["city_planner_chat_history"]
    else:
        conversation = [
            {
                "role":"system",
                "content":langgraph_city_planner_system_prompt
            },
            {
                "role":"user",
                "content":langgraph_city_planner_user_prompt.format(
                    name_of_city=state["inputs"]["origin_city"],
                    destinations=state["inputs"]["destinations"],
                    interests=state["inputs"]["traveller_interests"]
                )
            }
        ] 

    
    print("conversation is : ", len(conversation))

    write_json_to_file(conversation, prefix="conversation")

    # time.sleep(150)

    agent = GeneralAgent(llm_model=CitySearchModel, messages=conversation)
    response = agent.get_response(conversation)

    processed_response = process_llm_output_details(response.content)

    print()
    print("response is : ", response)
    print("processed response : ", processed_response)
    print(type(processed_response), " : ", bool(processed_response), " : len is ", len(processed_response))

    if processed_response:

        return {
        "city_planner_chat_history":conversation,
        "processed_tool_call_llm_response":processed_response,
        "tool_call_by_content":True
        }

    else:
        return {
            "city_planner_chat_history":conversation + [{
                "role":"assistant",
                "content":response.content
            }]}
=======
    print("summarizer agent response is : ", response)

    return {"trip_summarizer_chat_history":[response]}
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5
