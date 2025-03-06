import os

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from .base_model.llm_models import GraphState
from .graph_utils.nodes import (tool_node, 
                                ChossingCityAgent, 
                                local_expert_tool_node, 
                                CityLocalExpertAgent, 
                                trip_summarizer_tool_node, 
                                TripSummarizerAgent)

from .graph_utils.edges import (routing_choose_city_agent, 
                                routing_local_city_expert_agent, 
                                routing_trip_summarizer_agent)




class AIAssistant(object):

    def __init__(self):
        self.graph = self.get_graph()


    def get_graph(self):
        chose_city_agent_name = "ChooseCityAgnet"
        tool_node_name = "ToolNode"
        local_expert_tool_node_name = "LocalAgentToolNode"
        local_expert_agent_name = "CityLocalExpertAgent"
        summarizer_tools_name = "SummarizerToolNode"
        tripsummarizerAgent_name = "TripSummarizerAgent"


        graph = StateGraph(GraphState)
        graph.add_node(chose_city_agent_name, ChossingCityAgent)
        graph.add_node(tool_node_name, tool_node)
        graph.add_node(local_expert_agent_name, CityLocalExpertAgent)
        graph.add_node(local_expert_tool_node_name, local_expert_tool_node)
        graph.add_node(summarizer_tools_name, trip_summarizer_tool_node)
        graph.add_node(tripsummarizerAgent_name, TripSummarizerAgent)


        graph.add_edge(START, chose_city_agent_name)

        graph.add_conditional_edges(
            chose_city_agent_name,
            routing_choose_city_agent,
            {
                "tool":tool_node_name,
                "end":local_expert_agent_name
            }
        )

        graph.add_edge(tool_node_name, chose_city_agent_name)

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

        return graph.compile()

    def query(self, query:str):
        return self.graph.invoke({"inputs":query})
