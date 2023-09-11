import discord
from discord.ext import commands
import responses
import os
import json
from dotenv import load_dotenv
load_dotenv('.env')


async def send_message(message, user_message):
    try:
        response = responses.handle_response(user_message)
        await message.channel.send(response)
    except Exception as e:
        print("excepton" + e)

#class SimpleView(discord.ui.View)

async def spawnBall(message):
    
    
    with open('balls.json', 'r') as f:
        embed = discord.Embed(
        title="Quick, Somebody, Catch this wild countryball!", 
        color=discord.Color.random()
        )
        data = json.load(f)
        flagpath = data['1']["flag"]
        embed.set_image(url=f"attachment://{flagpath}")
        view = discord.ui.View()
        button=discord.ui.Button(label="CATCH")
        view.add_item(button)
        #embed.set_image(file=discord.File(flagpath))
        #print(flagpath)
        if message.channel.name == 'alphatesting':
            await message.channel.send(embed=embed, file=discord.File(flagpath), view=view)
    #embed.set_image()
    #await message.channel.send


def run_discord_bot():
    TOKEN = os.getenv('TOKEN')
    #print(os.environ.get('BallsBotToken'))
    intents= discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(description="Balls", command_prefix='/B ', intents=intents, help_command=None)
    

    @client.event
    async def on_ready():
        print(f"{client.user} is now running")

    @client.event
    async def on_message(message):
        if message.author.display_name == client.user.display_name:
            return
        
        if last_spawn == "":
            await spawnBall(message)
    
    @client.command()
    async def about(ctx):
        embed = discord.Embed(title="About this Lovely Bot",
                              description="Catch countryballs and trade with others. maybe even fight your friends, for honor and for GLORY.",
                              color=discord.Color.blurple())
        embed.add_field(name="More Commands", value="When i get the time to add commands they will be here.")
        embed.add_field(name="Thanks to my dads", value="Thank you to my dads Peter and Jonathan")
        await ctx.send(embed=embed)
    last_spawn = ""
    


    client.run(TOKEN)