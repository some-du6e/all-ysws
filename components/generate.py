import json
import urllib.request
from pyexpat.errors import messages

from openrouter import OpenRouter
from openai import OpenAI # this is only cuz the docs said so
import os
from dotenv import load_dotenv
from components.slack_updatemessages import refreshmessages
load_dotenv()
def generate(prompt, stream=False, model="minimax/minimax-m2-her", simple=True):
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
    model = "nvidia/nemotron-3-super-120b-a12b:free"
    # add system prompt
    # i dont have any rn TODO

    # init client
    client = OpenAI(api_key=os.environ.get("HACKCLUBAI_TOKEN"), base_url=os.environ.get("HACKCLUBAI_URL"))

    # make tools
    def edit_yswsjson(content):
        try:
            with open("ysws.json", "w", encoding='utf-8') as f:
                f.write(content)
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
                "description": "Print a message in the users console",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "string_to_print": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "String to print in the console"
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
            "description": "Refresh the messages in a Slack channel by deleting the old ones and posting new ones but with the same content",
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
            "description": "Read a JSON file containing MOST (doesn NOT have all of them) current and past and draft YSWSs. THIS IS NOT RELATED TO THE OTHER YSWS CATALOG. THIS IS ONLY FOR REFERENCE",
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
            "description": "Read a JSON file containing the current YSWS catalog",
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
            "description": "Modify a JSON file containing the current YSWS catalog",
            "parameters": {
                "type": "object",
                "properties": {
                    "replacement": {
                        "type": "string",
                        "description": "The replacement content for the YSWS JSON file"
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
            messages.append(get_tool_response(resp))
        else:
            break

    if iteration_count >= max_iterations:
        print("Warning: Maximum iterations reached")

    app.client.chat_postMessage(channel=os.environ.get("OWNER_CHAT"), text=messages[-1]['content'])

