import os
from dotenv import load_dotenv
from agent import Agent
from prompts import PROMPT_VARIATIONS

load_dotenv()

# Define test cases mapping input to expected behavior
TEST_CASES = [
    {
        "description": "Simple weather query",
        "input": "What is the weather like in New York?",
        "expected_tool": "get_weather",
        "requires_tool": True
    },
    {
        "description": "General knowledge (No tool needed)",
        "input": "Who wrote Romeo and Juliet?",
        "expected_tool": None,
        "requires_tool": False
    },
    {
        "description": "Vision task",
        "input": "What can you see in this image? https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg",
        "expected_tool": "analyze_image",
        "requires_tool": True
    }
]

def run_benchmark():
    """
    Evaluates different prompt variations on standard test cases to see
    how tool-calling reliability changes with prompt engineering.
    """
    if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "your_openai_api_key_here":
        print("ERROR: OPENAI_API_KEY required for evaluation.")
        return
        
    print("=== Prompt Evaluation Benchmark ===\n")
    
    results = {}
    
    for prompt_name in PROMPT_VARIATIONS.keys():
        print(f"\n--- Testing Prompt Variation: '{prompt_name}' ---")
        prompt_score = 0
        
        for case in TEST_CASES:
            # We initialize a new agent for each case to isolate memory
            agent = Agent(system_prompt_key=prompt_name, model="gpt-4o-mini")
            print(f"\nTesting: {case['description']}")
            print(f"Input: {case['input']}")
            
            try:
                # We can inspect the messages array after running to see what happened
                final_answer = agent.chat(case['input'], verbose=False)
                
                # Analyze trace
                tools_called = [msg['name'] for msg in agent.messages if msg.get('role') == 'tool']
                
                success = False
                if case['requires_tool']:
                    if case['expected_tool'] in tools_called:
                        success = True
                        print(f"✅ Success: Correctly called {case['expected_tool']}")
                    else:
                        print(f"❌ Failure: Expected {case['expected_tool']}, but got calls: {tools_called}")
                else:
                    if len(tools_called) == 0:
                        success = True
                        print(f"✅ Success: Correctly avoided tool calls.")
                    else:
                        print(f"❌ Failure: Hallucinated tool calls when none were needed: {tools_called}")
                        
                if success:
                    prompt_score += 1
                    
            except Exception as e:
                print(f"❌ Error during execution: {e}")
                
        results[prompt_name] = f"{prompt_score}/{len(TEST_CASES)}"
        
    print("\n\n=== Benchmark Results ===")
    print(f"{'Prompt Version':<20} | {'Score':<10}")
    print("-" * 35)
    for k, v in results.items():
        print(f"{k:<20} | {v:<10}")

if __name__ == "__main__":
    run_benchmark()
