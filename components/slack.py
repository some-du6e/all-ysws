import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from components.slackutils import gatekeep
from components.generate import generate, generate_yap, kinda_agentic
from datetime import datetime

load_dotenv()
# This sample slack application uses SocketMode
# For the companion getting started setup guide,
# see: https://docs.slack.dev/tools/bolt-python/getting-started

# Initializes your app with your bot token
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


# Listens to incoming messages that contain "hello"
@app.message("updateNOWplz")
def message_hello(message, say, client):
    
    say("NEVER EVER DELETE THIS MESSAGE, this will be added in a .env file. ")








@app.event("message")
def ownertalk(body, logger):
    wipecontext = ".clear"
    # check if owner
    if gatekeep(body['event'], app.client, "Bye bud") == False:
        return
    
    # check if message is in owner chat
    if body['event']['channel'] != os.environ.get("OWNER_CHAT"):
        return
    
    # fetch conversation history
    history = app.client.conversations_history(channel=os.environ.get("OWNER_CHAT"), limit=100)
    
    # get system prompt
    with open("prompts/agent.md", "r", encoding='utf-8') as f:
        system_prompt = f.read()

    # change some stuff in the system prompt
    ## inject the clear command 
    system_prompt = system_prompt.replace("[SUPERSIGMABOYZZZ]", wipecontext)
    ## inject the time in ISO 8601 format
    now = datetime.now().isoformat()
    system_prompt = system_prompt.replace("[TIMERN]", now) 
    ## injec t the owner id
    system_prompt = system_prompt.replace("[OWNER_CHAT_ID]", os.environ.get("OWNER"))
    ## inject the main channel id
    system_prompt = system_prompt.replace("[MAIN_CHANNEL_ID]", os.environ.get("CHANNEL_ID"))
    ## remove comments that start with <//>
    system_prompt = "\n".join([line for line in system_prompt.split("\n") if not line.strip().startswith("<//>")])
    
    # build messages array with system prompt + conversation
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    for msg in reversed(history['messages']):
        content = msg.get('text', '').strip()
        if not content:
            continue
        if content == wipecontext:
            messages = [{"role": "system", "content": system_prompt}]
            continue
        is_bot_message = (
            msg.get('user') == os.environ.get("BOT_USER_ID")
            or msg.get('bot_id') is not None
        )
        role = "assistant" if is_bot_message else "user"
        messages.append({"role": role, "content": content})
    
    # process the message
    try:
        kinda_agentic(messages, body, logger, app)
    except Exception as e:
        app.client.chat_postMessage(channel=os.environ.get("OWNER_CHAT"), text="OOPS: "+str(e))


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

def start():
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
