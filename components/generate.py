from openrouter import OpenRouter
import os
from dotenv import load_dotenv
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