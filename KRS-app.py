import hashlib
import os
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import discord
import asyncio

# Load variabel dari file .env
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
URL = os.getenv("MONITOR_URL")

client = discord.Client(intents=discord.Intents.default())

def get_data(url):
    """Mengambil konten dari URL dengan format rapi."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Tambahkan newline untuk pemisahan elemen
        return soup.get_text(separator="\n").strip()
    except requests.exceptions.RequestException as e:
        print(f"Error saat mengakses {url}: {e}")
        return None

def get_old_content(url):
    """Mendapatkan konten lama dari file."""
    file_name = hashlib.md5(url.encode('utf-8')).hexdigest() + ".txt"
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            return file.read()
    return ""

def store_new_content(url, content):
    """Menyimpan konten baru ke file."""
    file_name = hashlib.md5(url.encode('utf-8')).hexdigest() + ".txt"
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)

def extract_relevant_data(full_text):
    """Ekstrak bagian teks yang relevan untuk dikirim."""
    start_marker = "UNIVERSITAS PEMBANGUNAN NASIONAL VETERAN JAWA TIMUR"
    end_marker = "WAR"  # Kata terakhir dari bagian yang relevan
    if start_marker in full_text and end_marker in full_text:
        start_index = full_text.find(start_marker)
        end_index = full_text.rfind(end_marker) + len(end_marker)
        return full_text[start_index:end_index].strip()
    return "Tidak ditemukan data relevan."

async def send_notification(message):
    """Mengirim pesan ke Discord dengan format rapi."""
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        # Tambahkan backticks untuk memastikan format rapi
        formatted_message = f"```{message}```"
        await channel.send(formatted_message)
    else:
        print(f"Channel dengan ID {CHANNEL_ID} tidak ditemukan.")

async def monitor_website(url):
    """Memantau perubahan pada website."""
    old_content = get_old_content(url)
    new_content = get_data(url)

    if new_content is None:
        print(f"Tidak dapat mengakses {url}")
        return

    # Ekstrak bagian yang relevan dari konten
    relevant_new_content = extract_relevant_data(new_content)

    if old_content != relevant_new_content:
        await send_notification(relevant_new_content)
        store_new_content(url, relevant_new_content)
    else:
        print(f"{urlparse(url).netloc} has NOT CHANGED")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    while True:
        await monitor_website(URL)
        await asyncio.sleep(30)  # Cek setiap 30 detik

client.run(TOKEN)
