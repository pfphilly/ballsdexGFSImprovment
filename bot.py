import discord
import responses

async def send_message(message, user_message):
    try:
        response = responses.handle_response(user_message)
        await message.channel.send(response)
    except Exception as e:
        print("excepton" + e)

def run_discord_bot():
    TOKEN = "MTE1MDEyMDM0MTY3OTY1NzExMQ.GWkOdJ.LgCPe5qi0JC4JPCzNDj7mw-2fVUH2byVsrm7BU"
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