from ..base_model.llm_models import GraphState

def routing_choose_city_agent(state:GraphState):

    ai_message = state['city_planner_chat_history'][-1]

    if hasattr(ai_message, "tool_calls") and ai_message.tool_calls is not None:
        return "tool"
    
    return "end"


def routing_local_city_expert_agent(state:GraphState):
    ai_message = state['city_local_expert_chat_history'][-1]

    if hasattr(ai_message, "tool_calls") and ai_message.tool_calls is not None:
        return "tool"
    
    return "end"

def routing_trip_summarizer_agent(state:GraphState):

    ai_message = state['trip_summarizer_chat_history'][-1]

    if hasattr(ai_message, "tool_calls") and ai_message.tool_calls is not None:
        return "tool"
    
    return "end"
