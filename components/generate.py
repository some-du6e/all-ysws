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

