import discord
import responses
import os
from dotenv import load_dotenv
load_dotenv('.env')


async def send_message(message, user_message):
    try:
        response = responses.handle_response(user_message)
        await message.channel.send(response)
    except Exception as e:
        print("excepton" + e)

def run_discord_bot():
    TOKEN = os.getenv('TOKEN')
    #print(os.environ.get('BallsBotToken'))
    intents= discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    

    @client.event
    async def on_ready():
        print(f"{client.user} is now running")
    
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)

        print(f"{username} said {user_message}")

        await send_message(message, user_message)


    client.run(TOKEN)