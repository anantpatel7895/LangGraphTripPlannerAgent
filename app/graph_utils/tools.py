from ..services.web_search import WebSearch
from langgraph.types import Command, interrupt


def WebSearchTool(query:str)->list:
    """
    Performs a web search using the Google search engine and returns the top results.

    Args:
        query (str): The search query string.

    Returns:
        list: A list of search results containing relevant information.

    """
    searcher = WebSearch(engine="tavily")
    results = searcher.search(query, max_results=3)
    return results


def Calculate(operation: str) -> float:
    """
    Evaluates a mathematical expression and returns the result.

    Args:
        operation (str): A mathematical expression as a string.
                         Examples: "200 * 7", "5000 / 2 * 10"

    Returns:
        float: The calculated result of the expression.

    """
    try:
        return eval(operation, {"__builtins__": None}, {})
    except (SyntaxError, NameError, ZeroDivisionError):
        return "Error: Invalid mathematical expression"
    

def HumanAssistantTool(thought:str) -> str:
    """
    Requests human assistance for verifying or correcting the origin and destination cities.

    This function interrupts the automated flow and seeks human input for city verification.
    It takes the origin and destination city names as input, presents them to a human for review,
    and returns the human-provided response.

    Args:
        name_of_origin_city (str): The name of the origin city provided by the user.
        name_of_destination_city (str): The name of the destination city provided by the user.

    Returns:
        str: The corrected or confirmed city information provided by the human.

    """

    print("in HumanAssistantTool")
    human_response = interrupt(thought)
    
    print("Human Response is:", human_response)

    return human_response["data"]


