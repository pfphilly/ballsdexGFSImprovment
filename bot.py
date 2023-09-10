import discord
from discord.ext import commands
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
    client = commands.Bot(description="Balls", command_prefix='/B ', intents=intents, help_command=None)
    

    @client.event
    async def on_ready():
        print(f"{client.user} is now running")
    
    @client.command()
    async def about(ctx):
        embed = discord.Embed(title="About this Lovely Bot",
                              description="Catch countryballs and trade with others. maybe even fight your friends, for honor and for GLORY.",
                              color=discord.Color.blurple())
        embed.add_field(name="More Commands", value="When i get the time to add commands they will be here.")
        embed.add_field(name="Thanks to my dads", value="Thank you to my dads Peter and Jonathan")
        await ctx.send(embed=embed)

    


    client.run(TOKEN)