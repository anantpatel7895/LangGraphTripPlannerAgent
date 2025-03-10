import os

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from .base_model.llm_models import GraphState
from .graph_utils.nodes import (tool_node, 
                                ChossingCityAgent, 
                                local_expert_tool_node, 
                                CityLocalExpertAgent, 
                                trip_summarizer_tool_node, 
                                TripSummarizerAgent,
                                TripAssitantAgent,
<<<<<<< HEAD
                                trip_advisor_tool_node, 
                                ChossingCityReactAgent,
                                rct_tool_node)
=======
                                trip_advisor_tool_node)
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5

from .graph_utils.edges import (routing_choose_city_agent, 
                                routing_local_city_expert_agent, 
                                routing_trip_summarizer_agent,
<<<<<<< HEAD
                                routing_trip_advisor_agent,
                                routing_choose_city_react_agent)

from .base_model.llm_models import GraphState, ReactGraphState
=======
                                routing_trip_advisor_agent)

from .base_model.llm_models import GraphState, TripAdvisorState
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5




<<<<<<< HEAD
class AIAssistant:

    def __init__(self):
        self.react_graph = self.get_react_graph()
=======
class AIAssistant(object):

    def __init__(self):
        self.graph = self.get_graph()
        self.advisor_graph = self.get_trip_advisor_graph()
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5


    def get_graph(self):
        chose_city_agent_name = "ChooseCityAgnet"
        tool_node_name = "ToolNode"
        local_expert_tool_node_name = "LocalAgentToolNode"
        local_expert_agent_name = "CityLocalExpertAgent"
        summarizer_tools_name = "SummarizerToolNode"
        tripsummarizerAgent_name = "TripSummarizerAgent"

<<<<<<< HEAD
        graph = StateGraph(GraphState)
        graph.add_node(chose_city_agent_name, ChossingCityAgent)
        graph.add_node(tool_node_name, tool_node)
        graph.add_node(local_expert_agent_name, CityLocalExpertAgent)
        graph.add_node(local_expert_tool_node_name, local_expert_tool_node)
        graph.add_node(summarizer_tools_name, trip_summarizer_tool_node)
        graph.add_node(tripsummarizerAgent_name, TripSummarizerAgent)
=======

        graph = StateGraph(GraphState)
        graph.add_node(chose_city_agent_name, ChossingCityAgent)
        graph.add_node(tool_node_name, tool_node)
        # graph.add_node(local_expert_agent_name, CityLocalExpertAgent)
        # graph.add_node(local_expert_tool_node_name, local_expert_tool_node)
        # graph.add_node(summarizer_tools_name, trip_summarizer_tool_node)
        # graph.add_node(tripsummarizerAgent_name, TripSummarizerAgent)
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5


        graph.add_edge(START, chose_city_agent_name)

        graph.add_conditional_edges(
            chose_city_agent_name,
            routing_choose_city_agent,
            {
                "tool":tool_node_name,
<<<<<<< HEAD
                "end":local_expert_agent_name
=======
                "end":END         #local_expert_agent_name
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5
            }
        )

        graph.add_edge(tool_node_name, chose_city_agent_name)

<<<<<<< HEAD
        graph.add_conditional_edges(
            local_expert_agent_name,
            routing_local_city_expert_agent,
            {
                "tool":local_expert_tool_node_name,
                "end":tripsummarizerAgent_name
            }
        )

        graph.add_edge(local_expert_tool_node_name, local_expert_agent_name)

        graph.add_conditional_edges(
            tripsummarizerAgent_name,
            routing_trip_summarizer_agent,
            {
                "tool":summarizer_tools_name,
                "end":END
            }
        )

        graph.add_edge(summarizer_tools_name, tripsummarizerAgent_name)
=======
        # graph.add_conditional_edges(
        #     local_expert_agent_name,
        #     routing_local_city_expert_agent,
        #     {
        #         "tool":local_expert_tool_node_name,
        #         "end":tripsummarizerAgent_name
        #     }
        # )

        # graph.add_edge(local_expert_tool_node_name, local_expert_agent_name)

        # graph.add_conditional_edges(
        #     tripsummarizerAgent_name,
        #     routing_trip_summarizer_agent,
        #     {
        #         "tool":summarizer_tools_name,
        #         "end":END
        #     }

        # )

        # graph.add_edge(summarizer_tools_name, tripsummarizerAgent_name)
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5

        return graph.compile()

    def query(self, query:str):
        return self.graph.invoke({"inputs":query})

    def get_trip_advisor_graph(self):

        graph = StateGraph(TripAdvisorState)

        graph.add_node("Advisor", TripAssitantAgent)
        graph.add_node("ToolNode", trip_advisor_tool_node)

        graph.add_edge(START, "Advisor")
        graph.add_conditional_edges(
            "Advisor",
            routing_trip_advisor_agent,
            {
                "tool":"ToolNode",
                "end":END
            }
        )

        graph.add_edge("ToolNode", "Advisor")
        return graph.compile()
    
    def query_trip_advisor(self, query:dict):
        return self.advisor_graph.invoke({"origin_city":query["origin_city"],
                                          "destination_city":query["destination"]})
<<<<<<< HEAD


    def get_react_graph(self):
        chose_city_react_agent_name = "ChoosingCityReactAgnet"
        react_tool_node_name = "ToolNode"
        # local_expert_tool_node_name = "LocalAgentToolNode"
        # local_expert_agent_name = "CityLocalExpertAgent"
        # summarizer_tools_name = "SummarizerToolNode"
        # tripsummarizerAgent_name = "TripSummarizerAgent"

        graph = StateGraph(ReactGraphState)
        graph.add_node(chose_city_react_agent_name, ChossingCityReactAgent)
        graph.add_node(react_tool_node_name, rct_tool_node)
        # graph.add_node(local_expert_agent_name, CityLocalExpertAgent)
        # graph.add_node(local_expert_tool_node_name, local_expert_tool_node)
        # graph.add_node(summarizer_tools_name, trip_summarizer_tool_node)
        # graph.add_node(tripsummarizerAgent_name, TripSummarizerAgent)

        graph.add_edge(START, chose_city_react_agent_name)

        graph.add_conditional_edges(
            chose_city_react_agent_name,
            routing_choose_city_react_agent,
            {
                "tool":react_tool_node_name,
                "end":END   #local_expert_agent_name
            }
        )

        graph.add_edge(react_tool_node_name, chose_city_react_agent_name)

        # graph.add_conditional_edges(
        #     local_expert_agent_name,
        #     routing_local_city_expert_agent,
        #     {
        #         "tool":local_expert_tool_node_name,
        #         "end":tripsummarizerAgent_name
        #     }
        # )

        # graph.add_edge(local_expert_tool_node_name, local_expert_agent_name)

        # graph.add_conditional_edges(
        #     tripsummarizerAgent_name,
        #     routing_trip_summarizer_agent,
        #     {
        #         "tool":summarizer_tools_name,
        #         "end":END
        #     }
        # )

        # graph.add_edge(summarizer_tools_name, tripsummarizerAgent_name)

        return graph.compile()

    def query_react_graph(self, query:dict):

        state = {
            "tool_call_by_content":False,
            "inputs":query,
            "city_planner_chat_history":[],
            "processed_tool_call_llm_response":[]
        }
        return self.react_graph.invoke(state)
=======
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5
