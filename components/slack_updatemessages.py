import json
import os
import components.generate as gen
def refreshmessages(client):
    # get the messages from the file
    with open('messages.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    channel = os.environ.get("CHANNEL_ID")
    ## delete the old messages
    # delete msg1
    try:
        client.chat_delete(
            channel=channel,
            ts=data['message1']
        )
    except Exception as e:
        print(f"Error deleting msg1: {e}")
    # delete msg2
    try:
        client.chat_delete(
            channel=channel,
            ts=data['message2']
        )
    except Exception as e:
        print(f"Error deleting msg2: {e}")

    ## send new messages
    # send msg1
    try:
        response1 = client.chat_postMessage(
            channel=channel,
            text=data["old_message1"]
        )
        data['message1'] = response1['ts']
    except Exception as e:
        print(f"Error sending message 1: {e}")
    
    # send msg2
    try:
        response2 = client.chat_postMessage(
            channel=channel,
            text=data["old_message2"]
        )
        data['message2'] = response2['ts']
    except Exception as e:
        print(f"Error sending message 2: {e}")
    
    # save new stuff
    with open('messages.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    return "Messages refreshed successfully"

def generateMessages(client, update=False):
    # generate the msg
    yap = gen.generate_yap()

    # replace the msg
    with open('messages.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    data['old_message1'] = yap
    with open('messages.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    
    # refresh if update is true
    if update:
        refreshmessages(client)
        