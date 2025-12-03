import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
from quest_generator import generate_quest, complete_user_quest, abandon_user_quest
from team_quest_generator import generate_team_quest_message, generate_team_quest, complete_team_quest as complete_tq, get_active_team_quests
from stats import get_user_stats, get_leaderboard
from utils import send_dm_to_users

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # needed for reading message text

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.command()
async def quest(ctx, difficulty: int = 1):
    """Start a new quest. Usage: !quest [difficulty 1-3]"""
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
async def done(ctx):
    """Complete your active quest."""
    username = ctx.author.name
    response_text = complete_user_quest(username)
    await ctx.send(response_text)

@bot.command()
async def abandon(ctx):
    """Abandon your active quest."""
    username = ctx.author.name
    response_text = abandon_user_quest(username)
    await ctx.send(response_text)

@bot.command()
async def profile(ctx):
    """View your personal stats and score."""
    username = ctx.author.name
    stats_text = get_user_stats(username)
    await ctx.send(stats_text)

@bot.command()
async def leaderboard(ctx):
    """View the global leaderboard."""
    leaderboard_text = get_leaderboard()
    await ctx.send(leaderboard_text)

@bot.command()
async def SOS(ctx):
    """Show all available commands."""
    help_text = """
════════════════════════════════════════
           AVAILABLE COMMANDS
════════════════════════════════════════

**!quest [difficulty]** - Start a new quest (1-3)
**!done** - Complete your active quest
**!abandon** - Abandon your active quest
**!profile** - View your stats
**!leaderboard** - View leaderboard
**!tquest [difficulty] @user1 @user2** - Create team quest
**!tdone [quest_id]** - Complete team quest
**!tactive** - View active team quests
**!SOS** - Show this message

════════════════════════════════════════
"""
    await ctx.send(help_text)

@bot.command()
async def tquest(ctx, difficulty: int = 1, *, args: str = ""):
    """Create a team quest. Usage: !tquest [difficulty] @user1 @user2"""
    mentions = ctx.message.mentions
    
    if not mentions:
        await ctx.send("Please mention at least one user. Usage: `!tquest [difficulty] @user1 @user2`")
        return
    
    if difficulty < 1 or difficulty > 3:
        await ctx.send("Difficulty must be between 1 and 3.")
        return
    
    player_names = [user.name for user in mentions]
    team_quest, response_text = generate_team_quest(player_names, difficulty)
    
    if team_quest is None:
        await ctx.send(response_text)
        return
    
    await ctx.send(response_text)

@bot.command()
async def tdone(ctx, quest_id: str):
    """Complete a team quest by ID."""
    response_text = complete_tq(quest_id)
    await ctx.send(response_text)

@bot.command()
async def tactive(ctx):
    """Display all active team quests."""
    quests_text = get_active_team_quests()
    await ctx.send(quests_text)

@bot.command()
async def dm(ctx, *, args: str = ""):
    """Send a DM to a user. Usage: !dm @user Your message here"""
    mentions = ctx.message.mentions
    
    if not mentions:
        await ctx.send("Please mention a user. Usage: `!dm @user Your message here`")
        return
    
    if len(mentions) > 1:
        await ctx.send("You can only DM one user at a time.")
        return
    
    user = mentions[0]
    message = args.replace(f"<@{user.id}>", "").strip()
    
    if not message:
        await ctx.send("Please provide a message to send.")
        return
    
    try:
        await user.send(message)
        await ctx.send(f"Message sent to {user.name}!")
    except discord.Forbidden:
        await ctx.send(f"Could not send DM to {user.name} (DMs disabled).")


bot.run(TOKEN)