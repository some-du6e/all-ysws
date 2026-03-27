import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from components.slackutils import gatekeep
from components.generate import generate, generate_yap, kinda_agentic
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
    # check if owner
    if gatekeep(body['event'], app.client, "Bye bud") == False:
        return
    
    # check if message is in owner chat
    if body['event']['channel'] != os.environ.get("OWNER_CHAT"):
        return
    
    # fetch conversation history
    history = app.client.conversations_history(channel=os.environ.get("OWNER_CHAT"), limit=100)
    
    # build messages array with system prompt + conversation
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    for msg in reversed(history['messages']):
        role = "assistant" if msg.get('user') != os.environ.get("BOT_USER_ID") else "user"
        messages.append({"role": role, "content": msg.get('text', '')})
    
    # process the message
    kinda_agentic(messages, body, logger, app)


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

def start():
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()