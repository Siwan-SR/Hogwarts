from turtle import color
import discord
import random
import os
import asyncio
import json
import requests
import time
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from itertools import cycle
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("TOKEN")

client = commands.Bot(command_prefix="!")


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]["q"] + "\n - " + json_data[0]["a"]
    return (quote)


status = cycle(["!help", "Gobstones", "Quidditch"])


@client.event
async def on_ready():
    change_status.start()
    print("Bot is ready.")


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("This command does not exist.")


@client.command()
@commands.cooldown(5, 10, commands.BucketType.user)
async def ping(ctx):
    await ctx.send(f"Pong {round(client.latency * 1000)}ms")


@ping.error
async def ping_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Command cooldown",
                           description=f"You can use this command again in `{error.retry_after:.2f}s`.",
                           color=discord.Color.red())
        await ctx.send(embed=em)


@client.command(aliases=["8ball"])
@commands.cooldown(5, 10, commands.BucketType.user)
async def _8ball(ctx, *, question):
    responses = [

        "As I see it, yes.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don’t count on it.",
        "It is certain.",
        "It is decidedly so.",
        "Most likely.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Outlook good.",
        "Reply hazy, try again.",
        "Signs point to yes.",
        "Very doubtful.",
        "Without a doubt.",
        "Yes.",
        "Yes – definitely.",
        "You may rely on it."

    ]

    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")


@_8ball.error
async def _8ball_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Command cooldown",
                           description=f"You can use this command again in `{error.retry_after:.2f}s`.",
                           color=discord.Color.red())
        await ctx.send(embed=em)


@client.command(hidden=True)
@commands.has_permissions(manage_messages=True)
async def vanish(ctx, amount: int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)
    delete_msg = await ctx.send(f"{amount} messages have been deleted.")
    await asyncio.sleep(2050)
    await ctx.message.delete(delete_msg)


@vanish.error
async def vanish_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify an amount of messages to delete.")

    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the permission to delete messages.")


@client.command()
async def inspire(ctx):
    quote = get_quote()
    await ctx.send(quote)


@client.command(hidden=True)
@commands.has_permissions(ban_members=True)
async def tempexile(ctx, member: commands.MemberConverter, duration: int, *, reason=None):
    await ctx.guild.ban(member)
    await ctx.send(f"Member {member.mention}  has been temporarily banned for {duration} seconds.\nReason: {reason}")
    await ctx.message.delete()
    await asyncio.sleep(duration)
    await ctx.guild.unban(member)


@tempexile.error
async def tempexile_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify a duration.")

    elif isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Command cooldown",
                           description=f"You can use this command again in `{error.retry_after:.2f}s`.",
                           color=discord.Color.red())
        await ctx.send(embed=em)


@tempexile.error
async def tempexile_error2(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the permissions needed.")


@client.command(hidden=True)
@commands.has_permissions(manage_messages=True)
async def spam(ctx, amount: int, *, word=None):
    await ctx.message.delete()

    if word == None:
        word = "Spam"

    counter = 0
    while counter != amount:

        if amount == None:
            amount = 10

        if amount > 100:
            await ctx.send("Argument value cannot be over 100.")
            break

        counter = counter + 1
        await ctx.send(word)

        if counter == amount:
            await ctx.send("Spam has been stopped.")


@spam.error
async def spam_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the permission to spam.")


@client.command()
async def rule(ctx, num: int):
    if num == 1:
        rule_1 = discord.Embed(title="Rule No.1", description="""

                                                              Users in Discord are generally considered the base 
                                                              entity. Users can spawn across the entire platform, 
                                                              be members of guilds, participate in text and voice 
                                                              chat, and much more. Users are separated by a 
                                                              distinction of "bot" vs "normal." Although they are 
                                                              similar, bot users are automated users that are "owned" 
                                                              by another user. Unlike normal users, bot users do not 
                                                              have a limitation on the number of Guilds they can be a 
                                                              part of. Usernames must be between 2 and 32 characters 
                                                              long. Nicknames must be between 1 and 32 characters 
                                                              long. Names are sanitized and trimmed of leading, 
                                                              trailing, and excessive internal whitespace Usernames 
                                                              and profile pictures cannot contain any NSFW or 
                                                              inappropriate content. If a user is found with the 
                                                              following charges, the user will be banned permanently. 
                                                              The ban will only be lifted if the user has a valid 
                                                              reason to unban them. 
                                                              
                                                              """)

        await ctx.send(embed=rule_1)


@client.command(name="rps", description="Play rock paper scissors against the bot!", pass_context=True)
@commands.cooldown(5, 10, commands.BucketType.user)
async def rps(ctx):
    em1 = discord.Embed(title="Rock Paper Scissors", description="What do you pick?", color=discord.Color.blue())
    msg = await ctx.send(embed=em1)
    rock = "🪨"
    paper = "🧻"
    scissors = "✂️"
    options = ["🪨", "🧻", "✂️"]
    await msg.add_reaction(rock)
    await msg.add_reaction(paper)
    await msg.add_reaction(scissors)

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in options

    reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)

    random_number = random.randint(0, 2)
    computer_pick = options[random_number]
    wins = 0
    losses = 0

    if str(reaction.emoji) == rock and computer_pick == options[0]:
        await ctx.send("You picked: " + rock + "\n" + "Computer picked: " + rock)
        desc = "Wins: " + str(wins) + "\n" + "Losses: " + str(losses)
        emtie = discord.Embed(title="It's a tie!", description=desc, color=discord.Color.teal())
        await ctx.send(embed=emtie)

    elif str(reaction.emoji) == rock and computer_pick == options[1]:
        losses += 1
        desc = "Wins: " + str(wins) + "\n" + "Losses: " + str(losses)
        emlose = discord.Embed(title="You lost!", description=desc, color=discord.Color.red())
        await ctx.send("You picked: " + rock + "\n" + "Computer picked: " + paper)
        await ctx.send(embed=emlose)

    elif str(reaction.emoji) == rock and computer_pick == options[2]:
        wins += 1
        desc = "Wins: " + str(wins) + "\n" + "Losses: " + str(losses)
        emwin = discord.Embed(title="You win!", description=desc, color=discord.Color.green())
        await ctx.send("You picked: " + rock + "\n" + "Computer picked: " + scissors)
        await ctx.send(embed=emwin)

    elif str(reaction.emoji) == paper and computer_pick == options[0]:
        wins += 1
        desc = "Wins: " + str(wins) + "\n" + "Losses: " + str(losses)
        emwin = discord.Embed(title="You win!", description=desc, color=discord.Color.green())
        await ctx.send("You picked: " + paper + "\n" + "Computer picked: " + rock)
        await ctx.send(embed=emwin)

    elif str(reaction.emoji) == paper and computer_pick == options[1]:
        desc = "Wins: " + str(wins) + "\n" + "Losses: " + str(losses)
        emtie = discord.Embed(title="It's a tie!", description=desc, color=discord.Color.teal())
        await ctx.send("You picked: " + paper + "\n" + "Computer picked: " + paper)
        await ctx.send(embed=emtie)

    elif str(reaction.emoji) == paper and computer_pick == options[2]:
        losses += 1
        desc = "Wins: " + str(wins) + "\n" + "Losses: " + str(losses)
        emlose = discord.Embed(title="You lost!", description=desc, color=discord.Color.red())
        await ctx.send("You picked: " + paper + "\n" + "Computer picked: " + scissors)
        await ctx.send(embed=emlose)

    elif str(reaction.emoji) == scissors and computer_pick == options[0]:
        losses += 1
        desc = "Wins: " + str(wins) + "\n" + "Losses: " + str(losses)
        emlose = discord.Embed(title="You lost!", description=desc, color=discord.Color.red())
        await ctx.send("You picked: " + scissors + "\n" + "Computer picked: " + rock)
        await ctx.send(embed=emlose)

    elif str(reaction.emoji) == scissors and computer_pick == options[1]:
        wins += 1
        desc = "Wins: " + str(wins) + "\n" + "Losses: " + str(losses)
        emwin = discord.Embed(title="You win!", description=desc, color=discord.Color.green())
        await ctx.send("You picked: " + scissors + "\n" + "Computer picked: " + paper)
        await ctx.send(embed=emwin)

    elif str(reaction.emoji) == scissors and computer_pick == options[2]:
        desc = "Wins: " + str(wins) + "\n" + "Losses: " + str(losses)
        emtie = discord.Embed(title="It's a tie!", description=desc, color=discord.Color.teal())
        await ctx.send("You picked: " + scissors + "\n" + "Computer picked: " + scissors)
        await ctx.send(embed=emtie)


@rps.error
async def rps_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Command cooldown",
                           description=f"You can use this command again in `{error.retry_after:.2f}s`.",
                           color=discord.Color.red())
        await ctx.send(embed=em)


client.run(TOKEN)
