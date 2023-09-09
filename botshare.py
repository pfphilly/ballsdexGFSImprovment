from json import *

from discord.ext import commands

import discord

from random import *

import re

# P9d7q5k0*

TOKEN = "bot token here"  # Load token from environment variable

intents = discord.Intents.default()
intents.reactions = True
bot = commands.Bot(description="Baguette", command_prefix='b!', intents=intents, help_command=None)
base_template = {
    'hp': 100,
    'kills': 0,
    'money': 0,
    'inventory': [],
    'weapons': []
}

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = "Halt, spammer! Try again in {:.2f} seconds.".format(error.retry_after)
        await ctx.send(msg)


@bot.command()
async def say_something(ctx):
    await ctx.send("Something")


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Baguette Bot Help",
                          description="What is my purpose...? Wait... I don't know...",
                          color=discord.Color.blue())
    embed.add_field(name="b!say_something", value="Bot says something. Literally.", inline=False)
    embed.add_field(name="b!add_ship <person1> <person2>", value="Adds a ship to the list (quotation marks "
                                             "must be added if multiple words)", inline=False)
    embed.add_field(name="b!ships <page number>", value="Lists all compiled ships so far in the database", inline=False)
    embed.add_field(name="b!attack <@target>", value="Destroy an opponent of your choosing in an attack minigame!", inline=False)
    embed.add_field(name="b!stats <@target>", value="Check your stats across all of Baguette Bot", inline=False)
    embed.add_field(name="b!shop", value="Shows the shop",
                    inline=False)
    embed.add_field(name="b!purchase <item>", value="Purchases an item from the shop", inline=False)
    embed.add_field(name="b!heal <item>", value="Use a healing item to heal yourself", inline=False)
    embed.add_field(name="b!leaderboard <money/kills>", value="See the top baguetteers of the bot", inline=False)

    await ctx.send(embed=embed)


@bot.command()
async def add_ship(ctx, arg1, arg2):
    with open("universalbaguettefile.json", "r") as file_read:
        stats = load(file_read)
    stats["ships"].append([arg1, arg2])
    with open("universalbaguettefile.json", "w") as file_update:
        dump(stats, file_update)
    embed = discord.Embed(title=f"Shipped {arg1}x{arg2}!",
                          description="They're just perfect for each other "
                                      ":face_holding_back_tears:",
                          color=discord.Color.green())
    await ctx.send(embed=embed)


@bot.command()
async def ships(ctx, page: int = 1):
    with open("universalbaguettefile.json", "r") as file_read:
        stats = load(file_read)
    ships = []
    for i in stats["ships"]:
        ships.append(f"{i[0]} and {i[1]}")

    items_per_page = 10
    total_ships = len(ships)
    total_pages = (total_ships - 1) // items_per_page + 1

    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    ship_list = ships[start_index:end_index]

    if not ship_list:
        await ctx.send("Invalid page number.")

    embed = discord.Embed(title="Compiled Ships",
                          description=f"SHIPS :heart_eyes::heart_eyes::heart_eyes::\n\n",
                          color=discord.Color.purple())

    for ship in ship_list:
        embed.description += f"- {ship}\n"

    embed.set_footer(text=f"Page {page} of {total_pages}")

    await ctx.send(embed=embed)


def get_user_stats(user_id):
    file_name = f'{user_id}.json'
    if os.path.isfile(file_name):
        with open(file_name, 'r') as file:
            data = load(file)
            return data
    else:
        set_user_stats(user_id, 100, 0, 0, [], [])  # Create a new JSON file with default stats
        with open("universalbaguettefile.json", 'w') as file_update:
            stats = load(file_update)
            file_update.close()
        stats['ids'].append(user_id)
        with open("universalbaguettefile.json", 'r') as file_update:
            stats = dump(stats, file_update)
            file_update.close()
        return {'hp': 100, 'kills': 0, 'money': 0, 'inventory': [], 'weapons': []}


def set_user_stats(user_id, hp, kills, money, inventory, weapons):
    file_name = f'{user_id}.json'
    data = {'hp': hp, 'kills': kills, 'money': money, 'inventory': inventory, 'weapons': weapons}
    with open(file_name, 'w') as file:
        dump(data, file)


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def attack(ctx, member: discord.Member):
    if member.id == ctx.author.id or member.bot:
        embed = discord.Embed(title="Attack Error", color=discord.Color.red())
        embed.add_field(name="Invalid Target", value="You cannot attack yourself or a bot.")
        return await ctx.send(embed=embed)

    attack_methods = ["spam pings", "trolls", "scares", "impales", "atomically destructs", "punches", "liberates",
                      "[REDACTED]s", "drops a nuke on", "Thanos-snaps", "reveals all the secrets of",
                      "anschlusses", "kicks", "summons the holy light on", "shows the power of arson to", "roasts"]
    attacker_stats = get_user_stats(ctx.author.id)
    victim_stats = get_user_stats(member.id)

    attacker_hp = attacker_stats['hp']
    victim_hp = victim_stats['hp']

    attack_method = choice(attack_methods)
    damage = randint(10, 20)
    if member.id == "763181186101018675":
        damage = 0

    victim_hp -= damage
    reset = False
    if victim_hp <= 0:
        reset = True
        victim_hp = 100
        victim_stats['money'] -= 10
    set_user_stats(member.id, victim_hp, victim_stats['kills'], victim_stats['money'], victim_stats['inventory'], victim_stats['weapons'])
    if damage == 0:
        damage = "absolutely no"

    attack_sentence = f"{ctx.author.mention} {attack_method} {member.mention} and deals {damage} damage!"

    embed = discord.Embed(title="Attack", description=attack_sentence, color=discord.Color.red())
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.add_field(name="Attacker", value=ctx.author.display_name, inline=True)
    embed.add_field(name="Victim", value=member.display_name, inline=True)

    await ctx.send(embed=embed)
    if reset:
        embed_defeated = discord.Embed(title="Defeat", description=f"{member.mention} has been defeated!",
                                       color=discord.Color.red())
        embed_defeated.add_field(name=f"{ctx.author.display_name} wins the fight!", value="+10 Money\nAnother kill to your name!", inline=False)
        await ctx.send(embed=embed_defeated)
        attacker_stats['kills'] += 1  # Increment the attacker's kills
        attacker_stats['money'] += 10
        set_user_stats(ctx.author.id, attacker_stats['hp'], attacker_stats['kills'], attacker_stats['money'],
                       attacker_stats['inventory'], attacker_stats['weapons'])



@bot.command()
async def stats(ctx, member: discord.Member = None):
    if member is None:
        # If no member is mentioned, display the stats of the command invoker
        user_stats = get_user_stats(ctx.author.id)
        mention = ctx.author.mention
    else:
        # Display the stats of the mentioned member
        user_stats = get_user_stats(member.id)
        mention = member.mention

    hp = user_stats['hp']
    kills = user_stats['kills']
    money = user_stats['money']
    inventory = user_stats['inventory']

    item_counts = {}
    for item in inventory:
        item_counts[item] = item_counts.get(item, 0) + 1

    item_string = ""
    for item, count in item_counts.items():
        item_string += f"{item} x{count}\n"

    embed = discord.Embed(title="Stats", color=discord.Color.gold())
    embed.add_field(name="User", value=mention, inline=False)
    embed.add_field(name="HP", value=str(hp), inline=True)
    embed.add_field(name="Kills", value=str(kills), inline=True)
    embed.add_field(name="Money", value=str(money), inline=True)
    embed.add_field(name="Inventory", value=item_string, inline=True)

    await ctx.send(embed=embed)

@bot.command()
async def shop(ctx):
    items = [
        {"name": "Apple", "price": 20},
        {"name": "Big Mac", "price": 30},
        {"name": "Therapy", "price": 50},
        {"name": "American Healthcare", "price": 75},
        {"name": "Vaporub", "price": 100}
    ]
    weapons = [
        {"name": "Apple", "price": 20},
        {"name": "Big Mac", "price": 30},
        {"name": "Therapy", "price": 50},
        {"name": "American Healthcare", "price": 75},
        {"name": "Vaporub", "price": 100}
    ]

    embed = discord.Embed(title="Shop", description="Welcome to the Shop! Here are the available items for purchase:",
                          color=discord.Color.green())
    embed.add_field(name="\nPrescribed Drugs", value="")
    for item in items:
        embed.add_field(name=item["name"], value=f"Price: {item['price']} gold", inline=False)

    await ctx.send(embed=embed)


@bot.command()
async def purchase(ctx, item_name: str):
    items = [
        {"name": "apple", "price": 20},
        {"name": "big mac", "price": 30},
        {"name": "therapy", "price": 50},
        {"name": "american healthcare", "price": 75},
        {"name": "vaporub", "price": 100}
    ]

    user_stats = get_user_stats(ctx.author.id)
    money = user_stats['money']
    inventory = user_stats['inventory']
    weapons = user_stats['weapons']

    # Find the item in the shop
    item = next((i for i in items if i["name"].lower() == item_name.lower()), None)

    if item is None:
        await ctx.send("That item is not available in the shop.")
        return

    if money < item["price"]:
        await ctx.send("You don't have enough money to purchase this item.")
        return

    # Subtract the item price from the player's money
    money -= item["price"]

    # Add the purchased item to the player's inventory
    inventory.append(item["name"])

    # Update the player's stats in the JSON file
    set_user_stats(ctx.author.id, user_stats['hp'], user_stats['kills'], money, inventory, weapons)

    await ctx.send(f"You have purchased {item['name']}!")


@bot.command()
async def heal(ctx, item_request: str):
    user_stats = get_user_stats(ctx.author.id)
    inventory = user_stats['inventory']
    if item_request.lower() in inventory:
        if item_request.lower() == "apple":
            user_stats["hp"] += 20
            user_stats["inventory"].remove(item_request.lower())
        elif item_request.lower() == "big mac":
            user_stats["hp"] += 30
            user_stats["inventory"].remove(item_request.lower())
        elif item_request.lower() == "therapy":
            user_stats["hp"] += 50
            user_stats["inventory"].remove(item_request.lower())
        elif item_request.lower() == "american healthcare":
            user_stats["hp"] += 75
            user_stats["inventory"].remove(item_request.lower())
        elif item_request.lower() == "vaporub":
            user_stats["hp"] += 100
            user_stats["inventory"].remove(item_request.lower())
        if user_stats['hp'] > 100:
            user_stats['hp'] = 100
        set_user_stats(ctx.author.id, user_stats["hp"], user_stats["kills"], user_stats["money"], inventory, user_stats["weapons"])
        await ctx.send(f"{ctx.author.mention} has used {item_request} to heal!")
    else:
        await ctx.send(f"{ctx.author.mention} does not have {item_request} in their inventory.")


@bot.command()
async def leaderboard(ctx, mode: str, page_number: int = 1):
    valid_modes = ["money", "kills"]

    if mode not in valid_modes:
        await ctx.send("Invalid mode. Available modes: money, kills.")
        return

    with open("universalbaguettefile.json", "r") as file_read:
        stats = load(file_read)
        file_read.close()

    relevant_stats = []
    usernames = []

    for user_id in stats["ids"]:
        with open(f"{user_id}.json") as file_read:
            user_stats = load(file_read)
            file_read.close()
        relevant_stats.append(user_stats[mode])
        usernames.append(user_id)

    sorted_stats, sorted_usernames = zip(*sorted(zip(relevant_stats, usernames), reverse=True))

    if mode == "money":
        description = "The leaders of today's baguette economy."
    elif mode == "kills":
        description = "The ones that are the most committed, and the ones that have committed the most war crimes."
    embed = discord.Embed(title="Leaderboard", description=description, color=discord.Color.green())

    per_page = 10
    total_pages = (len(sorted_stats) + per_page - 1) // per_page

    if page_number < 1 or page_number > total_pages:
        await ctx.send("Invalid page number.")
        return

    start_index = (page_number - 1) * per_page
    end_index = start_index + per_page

    for index, (stat, user_id) in enumerate(zip(sorted_stats[start_index:end_index], sorted_usernames[start_index:end_index]), start=start_index):
        member = await bot.fetch_user(int(user_id))
        if member:
            embed.add_field(name=f"#{index + 1} {member.display_name}", value=str(stat), inline=False)

    embed.set_footer(text=f"Page {page_number}/{total_pages}")

    await ctx.send(embed=embed)


@bot.command()
async def update_user_files(ctx):
    allowed_user_id = 763181186101018675  # Replace with the desired user ID

    if ctx.author.id != allowed_user_id:
        error_embed = discord.Embed(
            title="Access Denied",
            description="You're not the dev, idiot.",
            color=discord.Color.red()
        )
        await ctx.send(embed=error_embed)
        return
    with open("universalbaguettefile.json", "r") as file_read:
        stats = load(file_read)

    for user_id in stats["ids"]:
        updated = update_user_file(user_id)
        if updated:
            await ctx.send(f"Updated file for user ID: {user_id}")
        else:
            await ctx.send(f"File not found for user ID: {user_id}")


def update_user_file(user_id):
    file_path = f"{user_id}.json"

    if os.path.isfile(file_path):
        with open(file_path, "r") as file_read:
            user_stats = load(file_read)

        # Check and update missing stats or fields
        for key, value in base_template.items():
            if key not in user_stats:
                user_stats[key] = value

        with open(file_path, "w") as file_write:
            dump(user_stats, file_write, indent=4)

        return True

    return False


@bot.command()
async def dev_help(ctx):
    allowed_user_id = 763181186101018675  # Replace with the desired user ID

    if ctx.author.id != allowed_user_id:
        error_embed = discord.Embed(
            title="Access Denied",
            description="You're not the dev, idiot.",
            color=discord.Color.red()
        )
        await ctx.send(embed=error_embed)
        return

    embed = discord.Embed(
        title="Developer Help Menu",
        description="List of available commands:",
        color=discord.Color.green()
    )

    embed.add_field(
        name="b!update_user_files",
        value="Update every user file",
        inline=False
    )
    embed.add_field(
        name="b!dev_help",
        value="Ooo secret help menu",
        inline=False
    )

    await ctx.send(embed=embed)


bot.run(TOKEN)
