from ..services.web_search import WebSearch


def WebSearchTool(query:str)->list:
    """
    Performs a web search using the Google search engine and returns the top results.

    Args:
        query (str): The search query string.

    Returns:
        list: A list of search results containing relevant information.

    """
    searcher = WebSearch(engine="tavily")
    results = searcher.search(query, max_results=2)
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



