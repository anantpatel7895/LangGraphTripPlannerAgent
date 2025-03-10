import os
import json
import instructor
<<<<<<< HEAD
import groq
=======
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5

from groq import Groq
from groq.types.chat import ChatCompletionMessage


from ..utils.tool_utils import llm_input_json_schema
from ..services.prompt_loader import PromptLoader

instant_model = "llama-3.1-8b-instant"
versatile_model = "llama-3.3-70b-versatile"


<<<<<<< HEAD

# groq

llm_context_length = {
    "gemma2-9b-it": 8192,
    "gemma-7b-it": 8192,
    "llama3-groq-70b-8192-tool-use-preview": 8192,
    "llama3-groq-8b-8192-tool-use-preview": 8192,
    "llama-3.1-70b-versatile": 131072,
    "llama-3.1-8b-instant": 131072,
    "llama-3.2-1b-preview": 8192,
    "llama-3.2-3b-preview": 8192,
    "llama-3.2-11b-text-preview": 8192,
    "llama-3.2-90b-text-preview": 8192,
    "llama3-70b-8192": 8192,
    "llama3-8b-8192": 8192,
    "mixtral-8x7b-32768": 32768,
    "llama-3.3-70b-versatile": 128000,
    "llama-3.3-70b-instruct": 128000
    }


imp_prompt_template = {
    "summarizer_system_message": "You are a helpful assistant that summarizes text.",
    "summarize_instruction": "Summarize the following text, make sure to include all the important information: {group}",
    "summary": "This is a summary of our conversation so far:\n{merged_summary}"
}


class GeneralAgent:

    def __init__(self, *, llm_model, messages, response_format=None):

      
        self.llm_config = llm_model()

        self.messages = messages
=======
class GeneralAgent:

    def __init__(self, *, llm_model, response_format=None):

      
        self.llm_config = llm_model()
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5
        

        if response_format:
            self.client = instructor.from_groq(Groq(api_key=os.environ.get("GROQ_API_KEY")), mode=instructor.Mode.JSON)
        else:
            self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
        self.response_format = response_format
        self.availabel_tools:list = None
        self.tools_schema:list = None
<<<<<<< HEAD
        self.messages = []
=======
        self.conversation_history = []
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5

        self.system_prompt:str = None

    def load_system_prompt(self, system_prompt_path):
        self.system_prompt = PromptLoader(system_prompt_path).get_prompt()
        return self.system_prompt

    def __call__(self, *args, **kwds):
        pass

    def get_response(self, messages):
        # print("messse in agnent is ", messages)
<<<<<<< HEAD

        self.messages = messages

        try:

            response = self.get_chatcompletion(messages=messages)

        except groq.BadRequestError as e:
            error_msg = str(e)
            print(e)
            
            if "context_length_exceeded" in error_msg:
                print(" Context length exceeded! Reducing message size and retrying...")

            return self._handle_context_length(messages)
=======
        response = self.get_chatcompletion(messages=messages)
        
        if self.response_format:
            return response
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5

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

<<<<<<< HEAD
    def _handle_context_length(self, messages):

        messages_groups = []

        for message in messages:
            
            if isinstance(message, ChatCompletionMessage):
                continue

            content = message["content"]

            context_length  = llm_context_length[self.llm_config.model]

            for i in range(0, len(content), context_length):
                messages_groups.append(content[i : i + context_length])

        summarized_contents = []
        for group in messages_groups:

            conversation = [{
                "role":"system",
                "content":"You are a helpful assistant that summarizes text."
            },
            {
                "role":"user",
                "content":f"Summarize the following text, make sure to include all the important information: {group}"
            }
            ]

            response = self.get_response(conversation)
            summarized_contents.append(response)

        merged_summary = " ".join(str(content) for content in summarized_contents)

        conversation = [
            {
                "role":"user",
                "content":f"This is a summary of our conversation so far:\n{merged_summary}"
            }
        ]

        return self.get_response(conversation)


    

=======
>>>>>>> 7a7281aa7d2d42162df2a09b66f8cefcf72edbe5
