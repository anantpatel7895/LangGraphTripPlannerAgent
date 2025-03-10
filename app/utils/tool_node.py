import json
from rich import print
import pyfiglet

from ..base_model.llm_models import GraphState
from .tool_utils import function_callling_to_json_schema
from operator import add
from ..utils.tool_utils import extract_tool_calls
from ..utils.write_to_json import write_json_to_file



class BasicToolNode:
    """A node that runs the tools requested in the last AIMessage."""

    def __init__(self, tools: list, *, return_state_args:str) -> None:
        self.tools_by_name = {tool.__name__: tool for tool in tools}
        self.return_state_args = return_state_args

    def __call__(self, state):

<<<<<<< HEAD
        print(f"[bold red] Tool Calling Results : [/bold red]")
=======
        print(f"[bold black] Tool Calling Results : [/bold black]")
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5

        ai_response = state[self.return_state_args][-1]
        
        messages = []

        tool_calls = ai_response.tool_calls

        if tool_calls:
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = self.tools_by_name[function_name]
                function_args = json.loads(tool_call.function.arguments)

                # print("function args : ", function_args)
                # i will have to add here the runtime argument to the function 
                # how i will get those run time arguments
                # 1. we can get runtime argument by passing in the state.
                # 2. or by difining in the global space and getting by the global Config.
                
                function_response = function_to_call(**function_args)
<<<<<<< HEAD
                
=======
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5
                if function_name == "WebSearchTool":
                    file_name = "_".join(function_args["query"].split())
                    write_json_to_file(function_response, prefix=file_name)

                    print(f"[bold green]    {function_args}[/bold green]")
                    print(f"Results for the Query is written in {file_name}")
                
                messages.append(
                    {
                        "tool_call_id": tool_call.id, 
                        "role": "tool", # Indicates this message is from tool use
                        "name": function_name,
                        "content": str(function_response),
                    }
                )    

        # pprint(json.dumps(messages, indent=4))

        # else: 
        #     content = ai_response.content

        #     too_calls = extract_tool_calls(content)

        #     for tool_call in tool_calls:

        #         function_name = tool_call["tool_name"]
        #         function_to_call = self.tools_by_name[function_name]
        #         function_args = tool_call["args"]

        #         function_response = function_to_call(**function_args)

        #         messages.append(
        #             {
        #                 "role":"tool",
        #                 "content":f"Observation:{function_response}"
        #             }
        #         )


        return {
            self.return_state_args:messages

            }
    

    def _get_runtime_args(self)->dict:
        pass

    def _inject_at_runtime(self, llm_provided_args:dict) -> dict:
        """it will inject the runtime argument value before the tool calling. """
        pass

    def _inspect_for_run_time_args(self, tool_name, llm_provided_args:dict) -> list:

        """it will return the list of argument name which must be passed at the runtime"""

        inputs_args = function_callling_to_json_schema(tool_name)["function"]["parameters"]["properties"]

        if len(inputs_args) > llm_provided_args:
            runtime_arg = []

            for name, prop in inputs_args:
                if name not in llm_provided_args.keys():
                    runtime_arg.append(name)

            raise AttributeError(f"Please provide runtime arguments {runtime_arg}")
 
def add_tool_node(state):
    last_ai_message = state["conversation"][-1]
    tool_node = BasicToolNode([add])
    tool_results = tool_node(state)
    return tool_results

