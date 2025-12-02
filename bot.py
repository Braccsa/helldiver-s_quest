import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
from quest_generator import generate_quest, complete_user_quest, abandon_user_quest
from stats import get_user_stats, get_leaderboard

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # needed for reading message text

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

@bot.command()
async def get_quest(ctx, difficulty: int = 1):
    if difficulty < 1 or difficulty > 3:
        await ctx.send("Difficulty must be between 1 and 3.")
        return
    
    username = ctx.author.name
    quest, response_text = generate_quest(username, difficulty)
    
    if quest is None:
        await ctx.send(response_text)
        return
    
    await ctx.send(response_text)

@bot.command()
async def complete_quest(ctx):
    username = ctx.author.name
    complete_user_quest(username)
    await ctx.send(f"✅ Quest completed! Well done, {username}!")

@bot.command()
async def abandon_quest(ctx):
    username = ctx.author.name
    response_text = abandon_user_quest(username)
    await ctx.send(response_text)

@bot.command()
async def stats(ctx):
    username = ctx.author.name
    stats_text = get_user_stats(username)
    await ctx.send(stats_text)

@bot.command()
async def leaderboard(ctx):
    leaderboard_text = get_leaderboard()
    await ctx.send(leaderboard_text)

bot.run(TOKEN)
