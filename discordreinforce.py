import os
import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = 1287068110242713721
ALLOWED_CHANNEL_ID = 1315170569318305833
ROLE_ID = 1315146935643934770

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.members = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents, 
            application_id=1293352667317276703
        )
        self.synced = False

    async def on_ready(self):
        if not self.synced:
            await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
            self.synced = True
        print(f'Logged in as {self.user}!')

bot = MyBot()

@bot.tree.command(name="callhelp", description="Send a message to all users with a specific role", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(profilelink="The link to the profile for people to join")
async def callhelp(interaction: discord.Interaction, profilelink: str):
    if interaction.channel.id != ALLOWED_CHANNEL_ID:
        await interaction.response.send_message(f"This command can only be used in the <#{ALLOWED_CHANNEL_ID}> channel.", ephemeral=True)
        return

    if not profilelink.startswith("https://www.roblox.com"):
        await interaction.response.send_message(
            "Invalid profile link. Please provide a link that starts with `https://www.roblox.com`",
            ephemeral=True
        )
        return

    guild = interaction.guild
    if not guild:
        await interaction.response.send_message("Server not found.", ephemeral=True)
        return

    role = guild.get_role(ROLE_ID)
    if not role:
        await interaction.response.send_message(f"Role with ID '{ROLE_ID}' not found.", ephemeral=True)
        return

    embed = discord.Embed(
        title="MESSAGE FROM HIGH COMMAND",
        color=discord.Color.red()
    )
    embed.add_field(name="Message", value="High Command is calling for reinforcements!", inline=False)
    embed.add_field(name="Link", value=f"Join them through this link!\n{profilelink}", inline=False)
    embed.set_footer(text="[I] Interlude")

    count = 0
    for member in role.members:
        if not member.bot:
            try:
                await member.send(member.mention, embed=embed)
                count += 1
            except discord.Forbidden:
                pass

    await interaction.response.send_message(f"Message sent to {count} members.", ephemeral=False)

async def handle(request):
    return web.Response(text="Bot is running")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    port = int(os.getenv("PORT", 8080))  # Use environment variable for port, default to 8080
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Web server running on port {port}")

# Run both the bot and web server
async def main():
    # Start the web server
    await start_web_server()

    # Start the bot
    await bot.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
