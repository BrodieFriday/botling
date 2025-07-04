import discord
from discord.ext import commands
import logging 
from dotenv import load_dotenv
import os
import typing

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
print("token = ", token)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

chatBot = commands.Bot(command_prefix='%', intents=intents)

guest_role = "guest"

@chatBot.event
async def on_ready():
    print(f"Chat bot started, {chatBot.user.name}")

@chatBot.event
async def on_message(message):
    if message.author == chatBot.user:
        return
    if "dammit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author} please use friendly language")
    
    await chatBot.process_commands(message)

@chatBot.command()
async def whoami(ctx):
    await ctx.send(f"{ctx.author.mention}")

@chatBot.command()
async def assignRole(ctx):
    role = discord.utils.get(ctx.guild.roles, name=guest_role)

    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now designated to {guest_role}")
    else:
        await ctx.send("Role not found")

@chatBot.command()
async def removeRole(ctx):
    role = discord.utils.get(ctx.guild.roles, name=guest_role)

    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} is no longer attached to {guest_role}")
    else:
        await ctx.send("Role not found")

@chatBot.command()
@commands.has_role(guest_role)
async def guest(ctx):
    await ctx.send("You are now a guest")

@guest.error
async def guest_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("Permission Denied")

@chatBot.command()
async def helloBot(ctx):
    await ctx.author.send("Hello chat bot")

@chatBot.command()
async def reply(ctx):
    await ctx.reply(f"Hello {ctx.author.mention}")

@chatBot.command()
async def msgStats(ctx, wordCount : typing.Optional[int] = 345, charCount=400):
    await ctx.send(f'{wordCount} word count and character count of {charCount}.')


chatBot.run(token, log_handler=handler, log_level=logging.DEBUG)