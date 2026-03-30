import {
  intro,
  outro,
  confirm,
  select,
  spinner,
  isCancel,
  cancel,
  text,
} from '@clack/prompts';
import { setTimeout as sleep } from 'node:timers/promises';
import color from 'picocolors';
import * as p from '@clack/prompts';
import search from '@inquirer/search'
import { App } from '@slack/bolt';
import { promises } from 'fs';


async function main() {
    console.log();
    intro(color.inverse(' Slack Bot Setup  '));
    p.log.info(`I recommend using copying the ${color.blue("manifest.json")} from the project folder.`);
    const slackBotShinanigans = await p.group(
        {
            bot_token: () => p.text({
                message: `Lets start with the bot token. It should start with xoxb-.
   You can see a guide on how to create a bot and get the token here: ${color.blue('https://share.google/aimode/phzCa0Ihu87NKYOEI')} or just from the "Install app" section`,
                placeholder: 'xoxb-...',
                validate(value) {
                    if (value.length < 6) return "That doesnt look like a token bud"
                    if (!value.startsWith('xoxb-')) return 'The token should start with xoxb-';
                }
            }),
            app_token: () => p.text({
                message: `App token now. It should start with xapp-.
   You can see a guide on how to get the token here: ${color.blue('https://share.google/aimode/2b0WMgeLJ3uawJ7kj')} or just get it from the "App-Level Tokens" section in the "Basic Information" tab and choose "connections:write" as the scope `,
                placeholder: 'xapp-...',
                validate(value) {
                    if (value.length < 6) return "That doesnt look like a token bud"
                    if (!value.startsWith('xapp-')) return 'The token should start with xapp-';
                }
            }),
        }
    )

    console.log()
    console.log()
    intro(color.inverse(' AI Implementation '));

    let hackclubber = false
    let openrouterer = false
    
    let aistuff = {
        "baseURL": "",
        "token": "",
        "model": "",

    }

    aistuff.baseURL = await p.text({
                message: `Whats the base URL for your AI provider? (openrouter or hackclub for their presets)`,
                placeholder: 'https://openrouter.ai/api/v1',
                initialValue: "hackclub",
                validate(value) {
                    if (value.length < 6) return "That doesnt look like a URL bud"
                    if (!value.startsWith('https://') && value !== "hackclub" && value !== "openrouter") return 'The URL should start with https://';
                }
    })

    if (aistuff.baseURL === "hackclub") {
        aistuff.baseURL = "https://ai.hackclub.com/proxy/v1"
        hackclubber = true
    }
    if (aistuff.baseURL === "openrouter") {
        aistuff.baseURL = "https://openrouter.ai/api/v1"
        openrouterer = true
    }

    aistuff.token = await p.text({
                message: `Whats the token for your AI provider?`,
                placeholder: 'sk-...',
                validate(value) {
                    if (value.length < 6) return "That doesnt look like a token bud"
                    if (!value.startsWith('sk-')) return 'The token should start with sk-';
                }
    })

    // custom model list only for hackclubbers
    if (hackclubber) {
        const response = await fetch('https://ai.hackclub.com/proxy/v1/models');
        const data = await response.json();
        const hackclubberoptions = data.data.map(model => ({ value: model.id }));

        aistuff.model = await search({
            message: 'Pick a model (i recommend openai/gpt-oss-120b or the gemini flash models)',
            source: async (input) => {
                const options = hackclubberoptions.map(o => o.value)
                if (!input) return options.map(o => ({ name: o, value: o }))
                return options
                    .filter(o => o.toLowerCase().includes(input.toLowerCase()))
                    .map(o => ({ name: o, value: o }))
            }
        });
    }
    // custom model list only for openrouter users
    if (openrouterer) {
        const response = await fetch('https://openrouter.ai/api/v1/models');
        const data = await response.json();
        const openrouteroptions = data.data.map(model => ({ value: model.id }));

        aistuff.model = await search({
            message: 'Pick a model (i recommend openai/gpt-oss-120b or the gemini flash models)',
            source: async (input) => {
                const options = openrouteroptions.map(o => o.value)
                if (!input) return options.map(o => ({ name: o, value: o }))
                return options
                    .filter(o => o.toLowerCase().includes(input.toLowerCase()))
                    .map(o => ({ name: o, value: o }))
            }
        });
    }

    async function busyWait(test) {
        const delayMs = 500;
        while(!test()) await new Promise(resolve => setTimeout(resolve, delayMs));
    }
    function generateRandomAlphanumeric(length) {
        const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        let result = "";
        for (let i = 0; i < length; i++) {
          result += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return result;
    }

    console.log()
    console.log()
    // finish off with extra slack options:
    intro(color.inverse(' Finishing Touches '));

    let slackUserShinanigans = {
        "owner": "",
        "owner_chat": "",
        "yap_channel": "",


    }
    await confirm({
        message: 'Please open a DM with your bot in slack and wait until i say so',
    });
    const app = new App({
        token: slackBotShinanigans.bot_token,
        socketMode: true,
        appToken: slackBotShinanigans.app_token,
    });

    let pairedChatandOwner = false  
    let pairedYapChannel = false
    let pairingCode = generateRandomAlphanumeric(6)
    let channelPairingCode = generateRandomAlphanumeric(6)
    // listen for the pairing code in the DM and set pairedChatandOwner to true when its received
    app.message(".pair " + pairingCode, async ({ message, say }) => {
        pairedChatandOwner = true;
        say({text: "pairedChatandOwner 😁😁😁"})
        console.log(message)
        // set le shinanigans
        slackUserShinanigans.owner = message.user
        slackUserShinanigans.owner_chat = message.channel
    });
    app.message("$pair " + pairingCode, async ({ message, say }) => {
        pairedYapChannel = true;
        say({text: "pairedyapchannel 😁😁😁"})
        console.log(message)
        // set le shinanigans
        slackUserShinanigans.yap_channel = message.channel
    });
    app.start()

    await confirm({
        message: 'Please send a DM to your bot with the following message: '+ color.blue(".pair " + pairingCode) + ' (case sensitive)',
        validate(value) {if (pairedChatandOwner === false) return "You havent sent the message yet!"}
    });

    await confirm({
        message: 'Please go to the desired channel for yapping and mention ur bot and also this '+ color.blue("$pair " + pairingCode) + ' (ex. @ysws-bot .pair ' + pairingCode + ')',
        validate(value) {if (pairedYapChannel === false) return "You havent sent the message yet!"}
    });
    
    
    
    
    intro(color.inverse(' .env file '));
    // generate the .env file content
    const envContent = `# autogenerated by the setup script
    SLACK_BOT_TOKEN=${slackBotShinanigans.bot_token}
    SLACK_APP_TOKEN=${slackBotShinanigans.app_token}
    
    OWNER=${slackUserShinanigans.owner}
    OWNER_CHAT=${slackUserShinanigans.owner_chat}
    CHANNEL_ID=${slackUserShinanigans.yap_channel}
    
    HACKCLUBAI_URL=${aistuff.baseURL}
    HACKCLUBAI_TOKEN=${aistuff.token}
    MODEL=${aistuff.model}`

    p.log.info("Here is the .env file content:" + envContent)

    choiceroo = await p.confirm(
    {
        message: "Do you want to save this to the .env file?"
    }  
    )

    if (choiceroo) {
        await promises.writeFile('.env', envContent)
        p.log.success(".env file saved successfully!")
    } else {
        p.log.warning("Okay, .env file not saved. You can copy the content from above and save it to a .env file yourself.")
    } 

    p.outro("Bye bud")
    exit(0)

}

main().catch(console.error);
