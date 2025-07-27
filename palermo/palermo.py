import discord
from discord import app_commands, Interaction, Embed, SelectOption
from discord.ui import View, Select
from discord.ext import commands, tasks
import random
import datetime
import asyncio
import dotenv
#import pyttsx3
import os
from player import Player
from characters import characters
from roleinfoview import *
from logic import assign_roles, is_game_over
from role import Role
from roleselection import *

dotenv.load_dotenv()

try:
  TOKEN = os.getenv("DISCORD_TOKEN")
  GUILD_ID = int(os.getenv("GUILD_ID"))  
except ValueError:
    print("Please set the DISCORD_TOKEN and GUILD_ID environment variables.")
    exit(1)


intents = discord.Intents.default()
intents.members = True  
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

roles = []
players ={}
active_games = {} # channel_id: {"players": [...], "roles_config": {...}}

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"🔁 Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

@tree.command(name="palermo_start", description="Ξεκίνα ένα παιχνίδι Wordle", guild=discord.Object(id=GUILD_ID))
async def start_palermo(interaction: discord.Interaction):
    channel_id = interaction.channel.id

    if channel_id in active_games:
        await interaction.response.send_message("⚠️ Υπάρχει ήδη ενεργό παιχνίδι σε αυτό το κανάλι.")
        return

    active_games[channel_id] = {"players": [], "roles_config": {}}
    await interaction.response.send_message("🎯 Ξεκίνησε νέο Palermo! Γράψε `/join` για να μπεις.")


@tree.command(name="join", description="Μπες στο τρέχον παιχνίδι Palermo", guild=discord.Object(id=GUILD_ID))
async def join_palermo(interaction: discord.Integration):
    channel_id = interaction.channel.id
    user = interaction.user
    if channel_id not in active_games:
        await interaction.response.send_message("Δεν υπάρχει ενεργό παιχνίδι. Γράψε `/palermo_start` πρώτα.")
        return

    game = active_games[channel_id]

    if any(p.user_id == user.id for p in game["players"]):
        await interaction.response.send_message("❌ Ήδη συμμετέχεις στο παιχνίδι.", ephemeral=True)
        return

    player = Player(display_name=user.display_name, user_id=user.id)
    game["players"].append(player)

    await interaction.response.send_message(f"{user.display_name} μπήκε στο παιχνίδι!")

@tree.command(name="list_players", description="Δες ποιοι έχουν μπει στο παιχνίδι", guild=discord.Object(id=GUILD_ID))
async def list_players(interaction: discord.Interaction):
    channel_id = interaction.channel.id
    if channel_id not in active_games or not active_games[channel_id]["players"]:
        await interaction.response.send_message("Δεν υπάρχουν παίκτες.")
        return

    player_list = "\n".join([f"• {p.display_name}" for p in active_games[channel_id]["players"]])
    await interaction.response.send_message(f"🎮 Παίκτες:\n{player_list}")

@tree.command(name="get_description", description="Δες την περιγραφη του ρόλου σου.", guild=discord.Object(id=GUILD_ID))
async def get_description(interaction: discord.Interaction):
    channel_id = interaction.channel.id

    if channel_id not in active_games:
        await interaction.response.send_message("Δεν υπάρχει ενεργό παιχνίδι.")
        return

    user_id = interaction.user.id
    game = active_games.get(channel_id)
    players = game["players"]
    player = next((p for p in players if p.user_id == user_id), None)
    if not player:
        await interaction.response.send_message("Δεν συμμετέχεις στο παιχνίδι.", ephemeral=True)
        return

    role = player.get_role()
    if not role:
        await interaction.response.send_message("❗ Δεν έχεις πάρει ακόμα ρόλο.", ephemeral=True)
        return
    
    role_title = role.get_rolename()
    role_desc = role.get_description()

    await interaction.response.send_message(
        f"🔍 Ο ρόλος σου είναι **{role_title}**\n\n{role_desc}.",
        ephemeral=True
    )

@tree.command(name="roleinfo", description="Δες τι κάνει ένας ρόλος", guild=discord.Object(id=GUILD_ID))
async def roleinfo(interaction: discord.Interaction):
    view = RoleInfoView()
    await interaction.response.send_message("Διάλεξε έναν ρόλο από το dropdown:", view=view, ephemeral=True)


@tree.command(name="set_roles", description="Ορίζει ρόλους παιχνιδιού", guild=discord.Object(id=GUILD_ID))
async def set_roles(interaction: discord.Interaction):
    channel_id = interaction.channel.id

    if channel_id not in active_games:
        await interaction.response.send_message("Δεν υπάρχει ενεργό παιχνίδι σε αυτό το κανάλι.")
        return

    await interaction.response.send_message(
        "🎭 Ξεκινά η διαμόρφωση ρόλων. Επίλεξε ρόλο από τη λίστα:",
        view=RoleSetupView(active_games)
    )


@tree.command(name="status", description="Δες αν είσαι ζωντανός ή νεκρός", guild=discord.Object(id=GUILD_ID))
async def status(interaction: discord.Interaction):
    channel_id = interaction.channel.id
    user_id = interaction.user.id

    if channel_id not in active_games:
        await interaction.response.send_message("Δεν υπάρχει ενεργό παιχνίδι.", ephemeral=True)
        return

    game = active_games[channel_id]
    players = game["players"]

    # Βρες τον Player
    player = next((p for p in players if p.user_id == user_id), None)

    if not player:
        await interaction.response.send_message("Δεν συμμετέχεις στο παιχνίδι.", ephemeral=True)
        return

    status = "🟢 Είσαι **ζωντανός**!" if player.is_alive else "🔴 Είσαι **νεκρός**."

    await interaction.response.send_message(status, ephemeral=True)

@tree.command(name="begin", description="Ξεκινάει το παιχνίδι και μοιράζονται ρόλοι", guild=discord.Object(id=GUILD_ID))
async def begin_palermo(interaction: discord.Integration):
    channel_id = interaction.channel.id
    game = active_games.get(channel_id)

    if not game or len(game["players"]) < 1:
        await interaction.response.send_message("Πρέπει να υπάρχουν τουλάχιστον 5 παίκτες για να ξεκινήσει το παιχνίδι!")
        return
    
    players = game["players"]
    roles_config = game.get("roles_config", {})

    assign_roles(players, roles_config)
    await interaction.response.send_message(f"🎲 Μοιράστηκαν ρόλοι στους παίκτες! Καλή τύχη σε όλους!")
    for player in players:
        await player.followup.send(f"{player.display_name} ο ρόλος σου είναι {player.get_role().get_rolename()}! {player.get_role().get_description()}.\n Μπορείς σε οποιαδήποτε στιγμή στο παιχνίδι να κάνεις /get_description για να δεις ποιός είναι ο ρόλος σου.", ephemeral=True)

@tree.command(name="stopgame", description="Σταμάτα το τρέχον παιχνίδι στο κανάλι.")
async def stop_game(interaction: discord.Interaction):
    channel_id = interaction.channel.id

    if channel_id not in active_games:
        await interaction.response.send_message("Δεν υπάρχει ενεργό παιχνίδι σε αυτό το κανάλι.", ephemeral=True)
        return

    del active_games[channel_id]
    await interaction.response.send_message("Το παιχνίδι σταμάτησε. 👋")

# <3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3 
bot.run(TOKEN)