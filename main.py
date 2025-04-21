import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

TRIGGER_CHANNEL_ID = int(os.getenv("TRIGGER_ID"))
CATEGORY_ID = int(os.getenv("CATEGORY_ID"))

@bot.event
async def on_ready():
    print(f'Bot aktif sebagai {bot.user}')

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and after.channel.id == TRIGGER_CHANNEL_ID:
        guild = member.guild
        category = discord.utils.get(guild.categories, id=CATEGORY_ID)
        channel = await guild.create_voice_channel(
            name=f"{member.name}",
            category=category
        )
        await member.move_to(channel)

        def check(x, y, z): return len(channel.members) == 0
        await bot.wait_for('voice_state_update', check=check)
        await channel.delete()

from keep_alive import keep_alive
import time

keep_alive()

while True:
    try:
        bot.run(os.getenv("TOKEN"))
    except Exception as e:
        print(f"Bot crash: {e}")
        time.sleep(5)  # Tunggu 5 detik sebelum restart
