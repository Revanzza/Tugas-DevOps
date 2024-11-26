import discord
from discord.ext import commands

# Token dari Discord Developer Portal
TOKEN = 'MTI4ODUxNjk0NzQwMjU1OTUyOA.GHgtgt.bllGeNC1sE2C3NGt_Wp2MAIvScdhXMz_RHPO0w'

# Definisikan intents
intents = discord.Intents.default()
intents.messages = True  # Agar bot dapat membaca dan mengirim pesan

# Inisialisasi bot dengan prefix "!" dan intents
bot = commands.Bot(command_prefix='!', intents =discord.Intents.all() )

# Event ketika bot berhasil online
@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} telah online!')

# Command sederhana untuk bot, misalnya !halo
@bot.command()
async def halo(ctx):
    await ctx.send('Halo! Saya adalah bot.')

# Command untuk mematikan bot dengan perintah !shutdown
@bot.command()
@commands.is_owner()  # Hanya pemilik bot yang dapat menggunakan command ini
async def shutdown(ctx):
    await ctx.send('Bot sedang dimatikan...')
    await bot.close()

# Jalankan bot
bot.run(TOKEN)