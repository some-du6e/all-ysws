import json
import urllib.request
from pyexpat.errors import messages

from openrouter import OpenRouter
from openai import OpenAI # this is only cuz the docs said so
import os
from dotenv import load_dotenv
from components.slack_updatemessages import refreshmessages
load_dotenv()
def generate(prompt, stream=False, model=os.environ.get("MODEL"), simple=True):
    # prob not the best idea shoving 1000+ characters thru here but it works for now

    # init client
    client = OpenRouter(api_key=os.environ.get("HACKCLUBAI_TOKEN"), server_url=os.environ.get("HACKCLUBAI_URL"))

    # generate response
    response = client.chat.send(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        stream=stream,
    )
    if simple: return response.choices[0].message.content
    return response


def generate_yap():
    # get the prompt
    try:
        with open("prompts/generate.md", "r", encoding='utf-8') as f:
            prompt = f.read()
    except Exception as e:
        print("OOPS: "+str(e))

    # get the json
    try:
        with open("ysws.json", "r", encoding='utf-8') as f:
            json = f.read()     
            print(json)
    except Exception as e:
        print("OOPS: "+str(e))

    # mix them together
    replacethisforthejson = "[JASON HERE]"
    prompt = prompt.replace(replacethisforthejson, json)
    
    respone = generate(prompt)
    print(respone)



def kinda_agentic(messages, body, logger, app):
    model = os.environ.get("MODEL")
    # add system prompt
    # i dont have any rn TODO
    # ^ added but injected in the slack file
    # init client
    client = OpenAI(api_key=os.environ.get("HACKCLUBAI_TOKEN"), base_url=os.environ.get("HACKCLUBAI_URL"))

    # make tools
    def edit_yswsjson(**kwargs):
        try:
            import json as json_mod
            with open("ysws.json", "w", encoding='utf-8') as f:
                json_mod.dump(kwargs, f, indent=2)
            return "ysws.json updated successfully"
        except Exception as e:
            return "OOPS: "+str(e)
    
    def read_yswsjson():
        try:
            with open("ysws.json", "r", encoding='utf-8') as f:
                json = f.read()     
                return json
        except Exception as e:
            return "OOPS: "+str(e)
        
    def refresh_channel_messages():
        print("Refreshing channel messages...")
        refreshmessages(app.client)
        return "Channel messages refreshed successfully"
        
    def print_hello(string_to_print):
        return str(string_to_print)
    
    def get_yswsjson():
        try:
            url = "https://github.com/hackclub/YSWS-Catalog/raw/refs/heads/main/api.json"
            response = urllib.request.urlopen(url)
            data = response.read().decode('utf-8')
            return data
        except Exception as e:
            return "OOPS: "+str(e)

    # define tools
    tools = [
        {
            "type": "function",
            "function": {
                "name": "print_message",
                "description": "Print a message to the console for debugging purposes",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "string_to_print": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "String or array of strings to print"
                        }
                    },
                    "required": ["string_to_print"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "refresh_channel_messages",
                "description": "Delete all messages in a Slack channel and repost them with the same content to refresh the view",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_overview_of_most_ysws",
                "description": "Fetch the YSWS overview JSON from GitHub (includes current, past, and draft YSWSs). Note: This is a separate dataset from the main catalog.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "read_ysws_json",
                "description": "Read the local YSWS catalog JSON file (ysws.json)",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "modify_ysws_json",
                "description": "Overwrite the local YSWS catalog JSON file (ysws.json) with new content. Only use after reading the file first.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "replacement": {
                            "type": "string",
                            "description": "Complete replacement JSON content for the YSWS catalog"
                        }
                    },
                    "required": ["replacement"]
                }
            }
        }
    ]
    tool_mapping = {
        "print_message": print_hello,
        "refresh_channel_messages": refresh_channel_messages,
        "get_overview_of_most_ysws": get_yswsjson,
        "read_ysws_json": read_yswsjson,
        "modify_ysws_json": edit_yswsjson
    }

    # # # # # # # # craft the request
    # # # # # # # request_1 = {
    # # # # # # #     "model": model,
    # # # # # # #     "tools": tools,
    # # # # # # #     "messages": messages
    # # # # # # # }

    # # # # # # # # get response
    # # # # # # # response_1 = client.chat.completions.create(**request_1)
    # # # # # # # response_message = response_1.choices[0].message
    
    # # # # # # # # process tool calls now
    # # # # # # # for tool_call in response_message.tool_calls:
    # # # # # # #     tool_name = tool_call.function.name
    # # # # # # #     tool_args = json.loads(tool_call.function.arguments)
    # # # # # # #     tool_response = tool_mapping[tool_name](**tool_args)
    # # # # # # #     messages.append({
    # # # # # # #         "role": "tool",
    # # # # # # #         "tool_call_id": tool_call.id,
    # # # # # # #         "content": json.dumps(tool_response),
    # # # # # # #     })

    # # # # # # # # fabricate the second request
    # # # # # # # request_2 = {
    # # # # # # #     "model": model,
    # # # # # # #     "messages": messages,
    # # # # # # #     "tools": tools
    # # # # # # # }
        # # # # # # # response_2 = client.chat.completions.create(**request_2)



    def call_llm(msgs):
        resp = client.chat.completions.create(
            model=model,
            tools=tools,
            messages=msgs
        )
        msgs.append(resp.choices[0].message.dict())
        return resp

    def get_tool_response(response):
        tool_call = response.choices[0].message.tool_calls[0]
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)

        # Look up the correct tool locally, and call it with the provided arguments
        # Other tools can be added without changing the agentic loop
        tool_result = tool_mapping[tool_name](**tool_args)

        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": tool_result,
        }

    max_iterations = 10
    iteration_count = 0

    while iteration_count < max_iterations:
        iteration_count += 1
        resp = call_llm(messages)

        if resp.choices[0].message.tool_calls is not None:
            texteroo = "Calling this tool: "+resp.choices[0].message.tool_calls[0].function.name+" with arguments: "+resp.choices[0].message.tool_calls[0].function.arguments
            app.client.chat_postMessage(channel=os.environ.get("OWNER_CHAT"), text=texteroo)
            messages.append(get_tool_response(resp))
        else:
            break

    if iteration_count >= max_iterations:
        print("Warning: Maximum iterations reached")

    # normalize multiple spaces into single spaces, but preserve newlines
    raw_content = messages[-1]['content']
    lines = raw_content.split('\n')
    cleaned_lines = [' '.join(line.split()) for line in lines]
    cleaned_content = '\n'.join(cleaned_lines)

    # check for 𓂀
    if '𓂀' in cleaned_content:
        cleaned_content = cleaned_content.replace('𓂀', '𓂀: cleared ')
    app.client.chat_postMessage(channel=os.environ.get("OWNER_CHAT"), text=cleaned_content)

