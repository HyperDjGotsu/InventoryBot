import os
import discord
from discord import app_commands
from discord.ext import commands
import requests
from urllib.parse import quote_plus

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwKst-FmmZMlzA4zEEv3UILvyE1X4v-ylA3dfb04B_bmW41iJqOXDxRlXleFtLLL6uf/exec"
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.tree.command(name="stock", description="Check if we have a card in stock")
@app_commands.describe(
    tcg="The TCG (e.g., pokemon, mtg, gundam)",
    product="Card or product name",
    set_name="Optional: Specific set name (e.g., Evolving Skies)"
)
async def stock(interaction: discord.Interaction, tcg: str, product: str, set_name: str = None):
    await interaction.response.defer(thinking=True)

    try:
        url = f"{GOOGLE_SCRIPT_URL}?tcg={quote_plus(tcg)}&product={quote_plus(product)}"
        if set_name:
            url += f"&set={quote_plus(set_name)}"

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        result = response.text.strip()

        if len(result) > 1900:
            result = result[:1900] + "... (truncated)"

        await interaction.followup.send(result)
    except Exception as e:
        await interaction.followup.send(f"⚠️ Error: {str(e)[:1900]}")

@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔁 Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"❌ Sync error: {e}")

bot.run(DISCORD_TOKEN)