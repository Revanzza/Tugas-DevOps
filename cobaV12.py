import hashlib
import os
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import discord
import difflib
import asyncio

TOKEN = 'MTI4ODUxNjk0NzQwMjU1OTUyOA.GsIc2j.QA_xhJlDu022Ez4S5tEIKwJu6J1zGDSOzF2DgM'
CHANNEL_ID = 1288541965519949975  # Ganti dengan channel ID Anda
URL = "https://vanzzza.blogspot.com/2024/09/jadwal-pengangguran.html"

client = discord.Client(intents=discord.Intents.default())

def get_data(url):
    """Mengambil konten yang relevan dari URL."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Filter konten spesifik
        content = soup.find("div", class_="post-body")  # Ganti sesuai struktur HTML
        if content:
            return content.get_text().strip()
        return None
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

def compare_content(old_content, new_content):
    """Membandingkan konten lama dan baru."""
    old_lines = old_content.splitlines()
    new_lines = new_content.splitlines()
    diff = difflib.unified_diff(old_lines, new_lines, lineterm="")
    return "\n".join(diff)

async def send_notification(message):
    """Mengirim pesan ke Discord."""
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(message)
    else:
        print(f"Channel dengan ID {CHANNEL_ID} tidak ditemukan.")

async def monitor_website(url):
    """Memantau perubahan pada website."""
    old_content = get_old_content(url)
    new_content = get_data(url)

    if new_content is None:
        print(f"Tidak dapat mengakses {url}")
        return

    if old_content != new_content:
        await send_notification(f"Website {url} telah diperbarui!\n\nKonten terbaru:\n{new_content}")
        store_new_content(url, new_content)
    else:
        print(f"{urlparse(url).netloc} tidak ada perubahan.")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    while True:
        await monitor_website(URL)
        await asyncio.sleep(60)  # Periksa setiap 60 detik

client.run(TOKEN)
