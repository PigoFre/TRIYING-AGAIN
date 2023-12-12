import os
import json
import time
import openai
from tavily import TavilyClient

# Initialize OpenAI and Tavily clients with API keys
openai_api_key = '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'
# Your Tavily API key
tavily_api_key = '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'
openai_client = openai.Client(api_key=openai_api_key)
tavily_client = TavilyClient(api_key=tavily_api_key)
password = '15399'
# Assistant prompt instruction (replace with your actual instruction)
assistant_prompt_instruction = """Debate Block Wizard is a specialized tool for crafting debate counter-arguments with a focus on legal precision. When presented with a debate resolution and argument, whether for the negative (A2NEG:) or affirmative (A2AFF:) side, it creates a counter-argument. IF it is given an A2NEG, it should take this argument and find a good counter to it, same with A2 AFF. it is VERY important that the argument is a counter to the one given. YOU NEED TO MAKE SURE THAT THE ARGUMENT IS AGAINST THE ONE GIVEN AND NOT FOR. Each response begins with 'a bold tagline summarizing the counter-argument in one concise sentence. This is crucial for clear and effective communication. The GPT then provides a direct quote from a credible source, obtained using its web browsing ability. The quote is presented in quotation marks, including the author's name for credibility it is important that this quote has the website it is gotten from aswell. This quote should be credible, and should be so professional that a lawyer should be able to say it, if it is not this way it should find a new quote. It is essential that the tagline and the quoted content are in sync, presenting a clear, direct, and legally cogent counter-argument. The GPT must ensure the accuracy of the quoted material, enabling users to directly verify the source of the quote by visiting the website where it was sourced. This level of precision and verification is paramount for effective debate preparation."""

# Create the OpenAI assistant
assistant = openai_client.beta.assistants.create(
    instructions=assistant_prompt_instruction,
    model="gpt-4-1106-preview",
    tools=[{
        "type": "function",
        "function": {
            "name": "tavily_search",
            "description": "Get information on recent events from the web.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query to use."},
                },
                "required": ["query"]
            }
        }
    }]
)
assistant_id = assistant.id

# Function to perform a Tavily search
def tavily_search(query, advanced=False):
    try:
        if advanced:
            search_result = tavily_client.search(query=query, search_depth="advanced")
        else:
            search_result = tavily_client.search(query=query)
        print("Search Result:", search_result)  # Debugging line
        return search_result
    except Exception as e:
        print(f"Error during Tavily search: {e}")
        return None



# Function to wait for a run to complete
def wait_for_run_completion(thread_id, run_id):
    while True:
        time.sleep(1)
        run = openai_client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        if run.status in ['completed', 'failed', 'requires_action']:
            return run

# Function to handle tool output submission
# Function to handle tool output submission
def submit_tool_outputs(thread_id, run_id, tools_to_call):
    tool_output_array = []
    for tool in tools_to_call:
        output = None
        tool_call_id = tool.id
        function_name = tool.function.name
        function_args = tool.function.arguments

        if function_name == "tavily_search":
            # Ensure the output is a string
            output = json.dumps(tavily_search(json.loads(function_args)["query"]))

        if output:
            tool_output_array.append({"tool_call_id": tool_call_id, "output": output})

    return openai_client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread_id,
        run_id=run_id,
        tool_outputs=tool_output_array
    )


# Function to print messages from a thread and return the response
def print_messages_from_thread(thread_id):
    messages = openai_client.beta.threads.messages.list(thread_id=thread_id)
    response = ""
    for msg in messages:
        if msg.role == "assistant":
            response += msg.content[0].text.value + "\n"
    return response.strip()





# Main function to process user input
def process_user_input(user_input):
    # Create a thread
    thread = openai_client.beta.threads.create()

    # Create a message in the thread
    message = openai_client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input,
    )

    # Create a run in the thread
    run = openai_client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

    # Wait for the run to complete
    run = wait_for_run_completion(thread.id, run.id)

    # Handle run status
    if run.status == 'failed':
        return "Error: " + str(run.error)
    elif run.status == 'requires_action':
        run = submit_tool_outputs(thread.id, run.id, run.required_action.submit_tool_outputs.tool_calls)
        run = wait_for_run_completion(thread.id, run.id)

    # Retrieve and return the response
    return print_messages_from_thread(thread.id)
