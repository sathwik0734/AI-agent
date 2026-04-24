import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import PROMPT_VARIATIONS
from tools.mock_api_tool import get_weather, GET_WEATHER_SCHEMA
from tools.vision_tool import analyze_image, ANALYZE_IMAGE_SCHEMA

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

AVAILABLE_TOOLS = {
    "get_weather": get_weather,
    "analyze_image": analyze_image
}

TOOL_SCHEMAS = [GET_WEATHER_SCHEMA, ANALYZE_IMAGE_SCHEMA]

class Agent:
    def __init__(self, system_prompt_key="v3_react", model="gpt-4o-mini"):
        """Initialize the agent with a specific prompt strategy and model."""
        self.model = model
        system_prompt = PROMPT_VARIATIONS.get(system_prompt_key, PROMPT_VARIATIONS["v3_react"])
        self.messages = [
            {"role": "system", "content": system_prompt}
        ]
        
    def chat(self, user_input: str, verbose=True):
        """Processes a user input and handles tool calling loops."""
        self.messages.append({"role": "user", "content": user_input})
        
        # Agent Reasoning Loop
        while True:
            if verbose:
                print(f"[{self.model}] Thinking...")
                
            response = client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=TOOL_SCHEMAS,
                tool_choice="auto",
            )
            
            response_message = response.choices[0].message
            
            # If no tool calls, the agent has its final answer
            if not response_message.tool_calls:
                final_answer = response_message.content
                if verbose:
                    print(f"\n[Agent]: {final_answer}\n")
                self.messages.append({"role": "assistant", "content": final_answer})
                return final_answer
                
            # If there are tool calls, we need to execute them
            self.messages.append(response_message)
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_to_call = AVAILABLE_TOOLS.get(function_name)
                
                if function_to_call:
                    function_args = json.loads(tool_call.function.arguments)
                    if verbose:
                        print(f"--> [Action Required] Agent invoked '{function_name}' with args: {function_args}")
                        
                    # Execute tool
                    try:
                        function_response = function_to_call(**function_args)
                    except Exception as e:
                        function_response = json.dumps({"error": str(e)})
                        
                    if verbose:
                        print(f"<-- [Action Result] {function_response}")
                        
                    # Append result back to the conversation
                    self.messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                        }
                    )
                else:
                    # Fallback if model hallucinates a tool
                    if verbose:
                        print(f"--> [Error] Agent hallucinated tool: {function_name}")
                    self.messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": json.dumps({"error": "Tool not found"}),
                        }
                    )

if __name__ == "__main__":
    print("=== AI Agent CLI ===")
    print("Type 'quit' to exit.")
    
    # Check for API keys
    if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "your_openai_api_key_here":
        print("WARNING: OPENAI_API_KEY is not set in .env. The agent will crash when generating a response.")
        
    agent = Agent(system_prompt_key="v3_react")
    
    while True:
        user_text = input("\nYou: ")
        if user_text.lower() in ['quit', 'exit']:
            break
        agent.chat(user_text)
