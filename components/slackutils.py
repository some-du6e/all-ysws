import os 
def gatekeep(message, client, custom_message):
    if custom_message is None:
        custom_message = f"Listen up <@{message['user']}>. What you just tried to do is not allowed." # workaround cuz it doesnt work idk why
    if message['user'] == os.environ.get("OWNER"):
        return True
    else:
        client.chat_postEphemeral(
            channel=message['channel'],
            user=message['user'],
            text=custom_message
        )
        return False