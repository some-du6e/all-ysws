import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from components.slackutils import gatekeep
load_dotenv()
# This sample slack application uses SocketMode
# For the companion getting started setup guide,
# see: https://docs.slack.dev/tools/bolt-python/getting-started

# Initializes your app with your bot token
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


# Listens to incoming messages that contain "hello"
@app.message("updateNOWplz")
def message_hello(message, say, client):
    # say() sends a message to the channel where the event was triggered
    gatekeep(message, client)
    
    client.chat_update(
        channel=os.environ.get("CHANNEL_ID"),
        ts=os.environ.get("MESSAGE_TS"),
        text="This message has been edited!",
        # You can also provide a full 'blocks' payload here
    )








@app.event("message")
def ownertalk(body, logger):
    # check if owner
    if gatekeep(body['event'], app.client, "Bye bud") == False:
        return
    
    print(body)

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

def start():
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()