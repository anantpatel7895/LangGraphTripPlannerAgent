
import json

class ReactToolNode:

    def __init__(self, tools: list, *, return_state_args:str) -> None:
        self.tools_by_name = {tool.__name__: tool for tool in tools}
        self.return_state_args = return_state_args

    def __call__(self, state):

        ai_response = state[self.return_state_args]
        print("ai_respons is : ", ai_response)

        messages = []

        for tool_call in ai_response:
            print(tool_call)

            thought = tool_call["Thought"]
            tool_name = tool_call["Action"]
            tool_args =  tool_call["Action Input"]
            action_and_action_input = "\n".join(["Action: " + tool_name, "Action Input: " + json.dumps(tool_args)])

            messages.append({"role":"assistant", "content":"\n".join(["Thought: ", thought])}),
            messages.append({"role":"assistant","content":action_and_action_input})

            function_to_call = self.tools_by_name[tool_name]

            function_response = function_to_call(**tool_args)
            print()
            print("tool result is : ", function_response)


            for result in function_response:
                messages.append(
                    {
                        "role":"assistant",
                        "content":str(result)
                    }
                )

        print("tool node results is : ", len(messages))
        return {
            "city_planner_chat_history":state["city_planner_chat_history"] + messages, 
            "tool_call_by_content":False,
            self.return_state_args:[]
            }