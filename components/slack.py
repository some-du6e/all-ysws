import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
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
    if message['user'] == os.environ.get("OWNER"):
        pass
    else:
        client.chat_postEphemeral(
            channel=message['channel'],
            user=message['user'],
            text=f"Listen up <@{message['user']}>. What you just tried to do is not allowed."
        )
        return
    
    say("""test
test
test""")


@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")



# the console told me to
@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

def start():
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()