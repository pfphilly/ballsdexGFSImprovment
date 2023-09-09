import discord
import responses

async def send_message(message, user_message):
    try:
        response = response.handle_response(user_message)
        message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = "MTE1MDEyMDM0MTY3OTY1NzExMQ.GasMUs.3-sMVdT0A8_ewpKkIllsDrXl0Esz5wnRQk1zPs"
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        print(f"{client.user} is now running")
    
    async def on_message(message):
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)

        print(f"{username} said {user_message}")

        await send_message(message, user_message)


    client.run(TOKEN)