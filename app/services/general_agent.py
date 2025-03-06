import os
import json
import instructor

from groq import Groq
from groq.types.chat import ChatCompletionMessage


from ..utils.tool_utils import llm_input_json_schema
from ..services.prompt_loader import PromptLoader

instant_model = "llama-3.1-8b-instant"
versatile_model = "llama-3.3-70b-versatile"


class GeneralAgent:

    def __init__(self, *, llm_model, response_format=None):

      
        self.llm_config = llm_model()
        

        if response_format:
            self.client = instructor.from_groq(Groq(api_key=os.environ.get("GROQ_API_KEY")), mode=instructor.Mode.JSON)
        else:
            self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
        self.response_format = response_format
        self.availabel_tools:list = None
        self.tools_schema:list = None
        self.conversation_history = []

        self.system_prompt:str = None

    def load_system_prompt(self, system_prompt_path):
        self.system_prompt = PromptLoader(system_prompt_path).get_prompt()
        return self.system_prompt

    def __call__(self, *args, **kwds):
        pass

    def get_response(self, messages):
        # print("messse in agnent is ", messages)
        response = self.get_chatcompletion(messages=messages)
        
        if self.response_format:
            return response

        return response.choices[0].message

    def handle_tools_call(self, ai_response:ChatCompletionMessage):
        self.conversation_history.append(ai_response)
        
        for tool_call in ai_response.tool_calls:
            function_name = tool_call.function.name
            function_to_call = self.availabel_tools[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)

            self.conversation_history.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
 
    def get_chatcompletion(self, messages):

        model_dict = self.llm_config.model_dump()

        model_dict["messages"] = messages

        if self.tools_schema:
            model_dict["tools"] = self.tools_schema

        response = self.client.chat.completions.create(
            **model_dict

        )

        # if self.tools_schema and self.response_format:
        #     response = self.client.chat.completions.create(
        #         messages=messages,
        #         model=self.llm_model,
        #         tools=self.tools_schema,
        #         response_model=self.response_format,
        #         reasoning_format="json",
        #         tool_choice="auto",
        #         temperature=0.5,
        #         max_tokens=60,
        #         max_completion_tokens=60
        #         )
            
        # elif self.tools_schema:
        #     response = self.client.chat.completions.create(
        #         messages=messages,
        #         model=self.llm_model,
        #         tools=self.tools_schema,
        #         tool_choice="auto",
        #         temperature=0,
        #         max_tokens=30,
        #         max_completion_tokens=35
        #         )
            
        # elif self.response_format:
       
        
        return response
        
    def bind_tools(self, tools:list):

        self.availabel_tools = {tool.__name__: tool for tool in tools}
        self.tools_schema = [llm_input_json_schema(tool) for tool in tools]

        return self

