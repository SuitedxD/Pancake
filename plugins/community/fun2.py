# Plugin Title: Fun Commands Pack No. 2
# Plugin Version: 0.1.0
# Plugin Author: Suited
# © 2025 Suited. All rights reserved.
# Licensed under Pancake Development License v1.0

# --- Imports ---

import os
import re
import io
import time
import random
import asyncio
import traceback
from io import BytesIO
from typing import Optional, Dict, Any, List, Tuple
import aiohttp
import requests
from PIL import Image, ImageDraw, ImageFont
import discord
from discord import app_commands
import db

# --- Config ---

# Ship image background
BACKGROUND_URL = "https://i.imgur.com/zdg6c3Y.png"
# GIF sources
WAIFU_BASE = "https://api.waifu.pics/sfw"
SOME_RANDOM_BASE = "https://some-random-api.ml"
GIF_CANDIDATES: Dict[str, List[str]] = {
    "kiss": ["kiss"],
    "hug": ["hug"],
    "slap": ["slap"],
    "waifu": ["waifu", "neko", "smug", "pat"],
}
# Cat facts/gifs
MEOWFACTS_URL = "https://meowfacts.herokuapp.com/"
THECATAPI_SEARCH = "https://api.thecatapi.com/v1/images/search?mime_types=gif&limit=1"
CATAAS_GIF = "https://cataas.com/cat/gif"
# HTTP timeouts
HTTP_TIMEOUT = 12
HEAD_TIMEOUT = 6
# Default Spotify playlist (used only if the guild has NOT set a playlist)
DEFAULT_SPOTIFY_PLAYLIST_ID = "2wXCxyn5dh7IzPXhNjTK9F"  # replace if you want another public playlist
DEFAULT_SPOTIFY_PLAYLIST_URL = f"https://open.spotify.com/playlist/{DEFAULT_SPOTIFY_PLAYLIST_ID}"
# Spotify endpoints (Client Credentials)
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_PLAYLIST_URL = "https://api.spotify.com/v1/playlists/{playlist_id}"
SPOTIFY_PLAYLIST_TRACKS = "https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
# Token cache for Spotify
_spotify_token_cache: Dict[str, Any] = {"access_token": None, "expires_at": 0}

# --- Font ---

def _resolve_font_path() -> Optional[str]:
    here = os.path.abspath(os.path.dirname(__file__))
    dirs = [
        os.path.join(here, "fonts"),
        os.path.abspath(os.path.join(here, "..", "fonts")),
        os.path.abspath(os.path.join(here, "..", "..", "fonts")),
        os.path.join(os.getcwd(), "fonts"),
        "fonts",
    ]
    seen = set()
    for d in dirs:
        try:
            d = os.path.abspath(d)
            if d in seen:
                continue
            seen.add(d)
            if not os.path.isdir(d):
                continue
            for fname in os.listdir(d):
                if fname.lower().endswith(".ttf"):
                    candidate = os.path.join(d, fname)
                    if os.path.exists(candidate):
                        return candidate
        except Exception:
            continue
    return None
_FONT_PATH = _resolve_font_path()
def _load_font(px: int) -> ImageFont.ImageFont:
    px = int(max(10, min(400, px)))
    if _FONT_PATH:
        try:
            return ImageFont.truetype(_FONT_PATH, px)
        except Exception:
            pass
    return ImageFont.load_default()

# --- HTTP helpers & GIF verification ---

async def _fetch_json(session: aiohttp.ClientSession, url: str, timeout: int = HTTP_TIMEOUT) -> Optional[dict]:
    try:
        async with session.get(url, timeout=timeout) as r:
            if r.status != 200:
                return None
            return await r.json()
    except Exception:
        return None
async def _head_is_gif(session: aiohttp.ClientSession, url: str, timeout: int = HEAD_TIMEOUT) -> bool:
    try:
        async with session.head(url, timeout=timeout) as resp:
            ctype = resp.headers.get("Content-Type", "")
            if "gif" in ctype.lower():
                return True
    except Exception:
        pass
    try:
        async with session.get(url, timeout=timeout) as resp:
            ctype = resp.headers.get("Content-Type", "")
            if "gif" in ctype.lower():
                return True
    except Exception:
        pass
    return url.lower().endswith(".gif")
async def _waifu_category_url(category: str) -> Optional[str]:
    url = f"{WAIFU_BASE}/{category}"
    try:
        async with aiohttp.ClientSession() as session:
            j = await _fetch_json(session, url)
            if not j:
                return None
            candidate = j.get("url") or j.get("link") or j.get("image")
            if candidate and await _head_is_gif(session, candidate):
                return candidate
    except Exception:
        return None
    return None
async def _some_random_animu(kind: str) -> Optional[str]:
    endpoint = f"{SOME_RANDOM_BASE}/animu/{kind}"
    try:
        async with aiohttp.ClientSession() as session:
            j = await _fetch_json(session, endpoint)
            if j and isinstance(j, dict):
                for k in ("link", "image", "url"):
                    if k in j and isinstance(j[k], str):
                        url = j[k]
                        if await _head_is_gif(session, url):
                            return url
    except Exception:
        pass
    return None
async def _find_gif(kind: str) -> Optional[str]:
    candidates = GIF_CANDIDATES.get(kind, [])
    for c in candidates:
        gif = await _waifu_category_url(c)
        if gif:
            return gif
    gif = await _some_random_animu(kind)
    if gif:
        return gif
    gif = await _waifu_category_url("waifu")
    if gif:
        return gif
    return None

# --- Cat GIF fetcher ---

async def _get_cat_gif() -> Optional[str]:
    try:
        async with aiohttp.ClientSession() as session:
            # Try TheCatAPI (gif)
            async with session.get(THECATAPI_SEARCH, timeout=HTTP_TIMEOUT) as r:
                if r.status == 200:
                    j = await r.json()
                    if isinstance(j, list) and j:
                        url = j[0].get("url")
                        if url and await _head_is_gif(session, url):
                            return url
            # Fallback to cataas
            if await _head_is_gif(session, CATAAS_GIF):
                return CATAAS_GIF
    except Exception:
        pass
    return None

# --- Facts ---

async def _get_cat_fact() -> Optional[str]:
    try:
        async with aiohttp.ClientSession() as session:
            j = await _fetch_json(session, MEOWFACTS_URL)
            if j and isinstance(j, dict):
                data = j.get("data")
                if isinstance(data, list) and data:
                    return str(data[0])
    except Exception:
        pass
    return None

# --- Ship Image Generation ---

def _measure_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> Tuple[int, int]:
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]
    except Exception:
        try:
            return draw.textsize(text, font=font)
        except Exception:
            try:
                return font.getsize(text)
            except Exception:
                return (len(text) * 7, 14)
def _safe_download_image(url: Optional[str], fallback_url: str) -> Image.Image:
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        if not url:
            raise Exception("No URL")
        resp = requests.get(url, headers=headers, timeout=8)
        resp.raise_for_status()
        return Image.open(BytesIO(resp.content)).convert("RGBA")
    except Exception:
        try:
            resp = requests.get(fallback_url, headers=headers, timeout=8)
            resp.raise_for_status()
            return Image.open(BytesIO(resp.content)).convert("RGBA")
        except Exception:
            return Image.new("RGBA", (800, 400), (30, 30, 30, 255))
def generate_ship_image(user1: discord.User, user2: discord.User, background_url: str = BACKGROUND_URL) -> BytesIO:
    try:
        background = _safe_download_image(background_url, background_url)
        min_w, min_h = 600, 300
        if background.width < min_w or background.height < min_h:
            background = background.resize((max(background.width, min_w), max(background.height, min_h)))
        draw = ImageDraw.Draw(background)
        avatar_size = min(int(background.width * 0.35), int(background.height * 0.6))
        avatar_size = max(60, avatar_size)
        try:
            a1_url = str(user1.display_avatar.url)
        except Exception:
            a1_url = None
        try:
            a2_url = str(user2.display_avatar.url)
        except Exception:
            a2_url = None
        avatar1 = _safe_download_image(a1_url, background_url).resize((avatar_size, avatar_size))
        avatar2 = _safe_download_image(a2_url, background_url).resize((avatar_size, avatar_size))
        mask1 = Image.new("L", avatar1.size, 0)
        ImageDraw.Draw(mask1).ellipse((0, 0, avatar1.size[0], avatar1.size[1]), fill=255)
        avatar1.putalpha(mask1)
        mask2 = Image.new("L", avatar2.size, 0)
        ImageDraw.Draw(mask2).ellipse((0, 0, avatar2.size[0], avatar2.size[1]), fill=255)
        avatar2.putalpha(mask2)
        margin_x = int(background.width * 0.06)
        y = background.height // 2 - avatar_size // 2
        x1 = margin_x
        x2 = background.width - margin_x - avatar_size
        background.paste(avatar1, (x1, y), avatar1)
        background.paste(avatar2, (x2, y), avatar2)
        def clean(s: str) -> str:
            return re.sub(r"[^A-Za-z]", "", s) or s.replace(" ", "")
        name1 = (getattr(user1, "display_name", None) or getattr(user1, "name", "User")).strip()
        name2 = (getattr(user2, "display_name", None) or getattr(user2, "name", "User")).strip()
        a = clean(name1)
        b = clean(name2)
        if not a:
            a = name1
        if not b:
            b = name2
        half_a = (len(a) + 1) // 2
        half_b = len(b) // 2
        ship = (a[:half_a] + (b[-half_b:] if half_b > 0 else b)).title() or (a + b).title()
        ship_px = max(28, int(avatar_size * 0.35))
        font = _load_font(ship_px)
        ship_w, ship_h = _measure_text(draw, ship, font)
        ship_x = background.width // 2 - ship_w // 2
        ship_y = y + avatar_size - 30
        draw.text((ship_x, ship_y), ship, font=font, fill=(255, 220, 220))
        buffer = BytesIO()
        background.save(buffer, "PNG")
        buffer.seek(0)
        return buffer
    except Exception:
        try:
            err_img = Image.new("RGBA", (800, 250), (30, 30, 30, 255))
            draw = ImageDraw.Draw(err_img)
            font = ImageFont.load_default()
            draw.text((10, 10), "Ship image error", font=font, fill=(255, 0, 0))
            b = BytesIO()
            err_img.save(b, "PNG")
            b.seek(0)
            return b
        except Exception:
            return BytesIO(b"")

# --- Credentials ---

def _extract_playlist_id(url_or_id: str) -> Optional[str]:
    if not url_or_id:
        return None
    s = url_or_id.strip()
    if re.fullmatch(r"[0-9A-Za-z]+", s):
        return s
    m = re.search(r"playlist/([0-9A-Za-z]+)", s)
    if m:
        return m.group(1)
    m2 = re.search(r"spotify:playlist:([0-9A-Za-z]+)", s)
    if m2:
        return m2.group(1)
    return None
def _ms_to_mmss(ms: int) -> str:
    seconds = int(ms / 1000)
    m, s = divmod(seconds, 60)
    return f"{m}:{s:02d}"
async def _get_client_credentials_token(client_id: str, client_secret: str) -> Optional[str]:
    now = int(time.time())
    if _spotify_token_cache.get("access_token") and _spotify_token_cache.get("expires_at", 0) > now + 5:
        return _spotify_token_cache["access_token"]
    auth = aiohttp.BasicAuth(login=client_id, password=client_secret)
    data = {"grant_type": "client_credentials"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(SPOTIFY_TOKEN_URL, data=data, auth=auth, timeout=15) as resp:
                if resp.status != 200:
                    return None
                j = await resp.json()
                token = j.get("access_token")
                expires = int(j.get("expires_in", 3600))
                _spotify_token_cache["access_token"] = token
                _spotify_token_cache["expires_at"] = int(time.time()) + expires
                return token
    except Exception:
        traceback.print_exc()
        return None
async def _get_playlist_metadata(access_token: str, playlist_id: str) -> Optional[Dict[str, Any]]:
    headers = {"Authorization": f"Bearer {access_token}"}
    url = SPOTIFY_PLAYLIST_URL.format(playlist_id=playlist_id)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=15) as resp:
                if resp.status != 200:
                    return None
                return await resp.json()
    except Exception:
        traceback.print_exc()
        return None
async def _get_track_by_offset(access_token: str, playlist_id: str, offset: int) -> Optional[Dict[str, Any]]:
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"limit": 1, "offset": offset}
    url = SPOTIFY_PLAYLIST_TRACKS.format(playlist_id=playlist_id)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params, timeout=15) as resp:
                if resp.status != 200:
                    return None
                j = await resp.json()
                items = j.get("items", [])
                if not items:
                    return None
                tr = items[0].get("track")
                return tr
    except Exception:
        traceback.print_exc()
        return None

# --- Permissions ---

def _is_moderator(interaction: discord.Interaction) -> bool:
    if not interaction.guild:
        return False
    perms = interaction.user.guild_permissions
    return any([
        perms.administrator,
        perms.manage_guild,
        perms.manage_roles,
        perms.manage_messages,
        perms.kick_members,
        perms.ban_members
    ])

# --- Plugin ---

class Fun2Plugin:
    def __init__(self, bot: discord.Client):
        self.bot = bot

        # Fun commands
        self._ship = app_commands.Command(
            name="ship",
            description="Pancake calculates the compatibility level between two users.",
            callback=self.ship
        )
        self._fight = app_commands.Command(
            name="fight",
            description="Play a silly fight against another user.",
            callback=self.fight
        )
        self._kiss = app_commands.Command(
            name="kiss",
            description="Kiss another user.",
            callback=self.kiss
        )
        self._hug = app_commands.Command(
            name="hug",
            description="Hug another user.",
            callback=self.hug
        )
        self._pickup = app_commands.Command(
            name="pickup-line",
            description="Throw someone a pick-up line.",
            callback=self.pickup_line
        )
        self._who = app_commands.Command(
            name="who",
            description="Pancake will pick someone randomly from the server based on your question.",
            callback=self.who
        )
        self._catfact = app_commands.Command(
            name="cat-fact",
            description="Get a random cat fact.",
            callback=self.cat_fact
        )
        self._tod = app_commands.Command(
            name="truth-or-dare",
            description="Start a Truth or Dare joinable session (min 2 players).",
            callback=self.truth_or_dare
        )
        self._set_playlist = app_commands.Command(
            name="set-recommend-playlist",
            description="Set the server's Spotify public playlist (URL or ID).",
            callback=self.set_playlist_callback
        )
        self._music_recommend = app_commands.Command(
            name="music-recommendation",
            description="Pancake recommends a song you should listen to.",
            callback=self.music_callback
        )
        self.sessions: Dict[int, Dict[str, Any]] = {}

    # ---- Commands ---
    @app_commands.describe(user1="First user to ship", user2="Second user to ship")
    async def ship(self, interaction: discord.Interaction, user1: discord.User, user2: discord.User):
        try:
            await interaction.response.defer()
            percent = random.randint(0, 100)
            img_bytes = await asyncio.to_thread(generate_ship_image, user1, user2, BACKGROUND_URL)

            embed = discord.Embed(
                title=f"{user1.mention} and {user2.mention} are **{percent}%** compatible!",
                color=discord.Color.purple()
            )
            file = discord.File(img_bytes, filename="ship.png")
            embed.set_image(url="attachment://ship.png")
            await interaction.followup.send(embed=embed, file=file)
        except Exception:
            traceback.print_exc()
            await interaction.response.send_message("Error running /ship.", ephemeral=True)
    @app_commands.describe(target="User to fight")
    async def fight(self, interaction: discord.Interaction, target: discord.User):
        try:
            attacker = interaction.user
            if attacker.id == target.id:
                await interaction.response.send_message("You can't fight yourself.", ephemeral=True)
                return

            embed1 = discord.Embed(
                title="Fight",
                description=f"{attacker.mention} approaches {target.mention}... and threatens them with a rubber duck. 🦆",
                color=discord.Color.dark_red()
            )
            await interaction.response.send_message(embed=embed1)
            async def finish():
                await asyncio.sleep(random.uniform(2.0, 4.0))
                bot_user = self.bot.user
                if target.id == bot_user.id:
                    desc = f"I totally owned {attacker.mention}. My rubber duck unleashed chaos."
                    embed_win = discord.Embed(title="Fight result", description=desc, color=discord.Color.gold())
                    gif = await _find_gif("waifu")
                    if gif:
                        embed_win.set_image(url=gif)
                    try:
                        await interaction.followup.send(embed=embed_win)
                    except Exception:
                        pass
                    return
                outcome = random.choice(["attacker_wins", "target_wins", "target_runs"])
                if outcome == "attacker_wins":
                    desc = f"{attacker.mention} smacked {target.mention} with the duck."
                elif outcome == "target_wins":
                    desc = f"{target.mention} turned the tables and clobbered {attacker.mention}."
                else:
                    desc = f"{target.mention} ran away after seeing the duck."
                embed2 = discord.Embed(title="Fight result", description=desc, color=discord.Color.gold())
                gif = await _find_gif("waifu")
                if gif:
                    embed2.set_image(url=gif)
                try:
                    await interaction.followup.send(embed=embed2)
                except Exception:
                    pass
            self.bot.loop.create_task(finish())
        except Exception:
            traceback.print_exc()
            await interaction.response.send_message("Error running /fight.", ephemeral=True)
    @app_commands.describe(user="User to kiss")
    async def kiss(self, interaction: discord.Interaction, user: discord.User):
        try:
            await interaction.response.defer()
            gif = await _find_gif("kiss")
            embed = discord.Embed(title="Kiss", description=f"{interaction.user.mention} kissed {user.mention} 💋", color=discord.Color.red())
            if gif:
                embed.set_image(url=gif)
            await interaction.followup.send(embed=embed)
        except Exception:
            traceback.print_exc()
            await interaction.response.send_message("Error running /kiss.", ephemeral=True)
    @app_commands.describe(user="User to hug")
    async def hug(self, interaction: discord.Interaction, user: discord.User):
        try:
            await interaction.response.defer()
            gif = await _find_gif("hug")
            embed = discord.Embed(title="Hug", description=f"{interaction.user.mention} hugged {user.mention} 🤗", color=discord.Color.blue())
            if gif:
                embed.set_image(url=gif)
            await interaction.followup.send(embed=embed)
        except Exception:
            traceback.print_exc()
            await interaction.response.send_message("Error running /hug.", ephemeral=True)
    @app_commands.describe(user="Who to compliment with a pickup line")
    async def pickup_line(self, interaction: discord.Interaction, user: discord.User):
        try:
            await interaction.response.defer()
            line = random.choice([
                "Are you a magician? Because whenever I look at you, everyone else disappears.",
                "Do you have a name, or can I call you mine?",
                "Are you a parking ticket? 'Cause you've got FINE written all over you.",
                "If you were a vegetable, you'd be a cute-cumber.",
                "Do you have a map? I'm getting lost in your eyes."
            ])
            embed = discord.Embed(
                title="Pickup Line",
                description=f"{interaction.user.mention} approaches {user.mention} and says:\n\n\"{line}\"",
                color=discord.Color.magenta()
            )
            await interaction.followup.send(embed=embed)
        except Exception:
            traceback.print_exc()
            try:
                await interaction.response.send_message("Error running /pickup-line.", ephemeral=True)
            except Exception:
                pass
    @app_commands.describe(question="Question to ask the server")
    async def who(self, interaction: discord.Interaction, question: str):
        try:
            guild = interaction.guild
            if not guild:
                await interaction.response.send_message("This command must be used in a server.", ephemeral=True)
                return
            members = [m for m in guild.members if not m.bot]
            if not members:
                await interaction.response.send_message("No members found.", ephemeral=True)
                return
            chosen = random.choice(members)
            await interaction.response.send_message(f"{question}\nSelected: {chosen.mention}")
        except Exception:
            traceback.print_exc()
            await interaction.response.send_message("Error running /who.", ephemeral=True)
    async def cat_fact(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            fact = await _get_cat_fact()
            gif = await _get_cat_gif()
            if not fact:
                await interaction.followup.send("Couldn't fetch a cat fact right now. Try again later.", ephemeral=True)
                return
            embed = discord.Embed(title="Cat Fact", description=fact, color=discord.Color.teal())
            if gif:
                embed.set_image(url=gif)
            await interaction.followup.send(embed=embed)
        except Exception:
            traceback.print_exc()
            try:
                await interaction.response.send_message("Error running /cat-fact.", ephemeral=True)
            except Exception:
                pass
    # TOD
    async def truth_or_dare(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            if not interaction.guild:
                await interaction.followup.send("This command must be used in a server.", ephemeral=True)
                return
            gid = interaction.guild.id
            if gid in self.sessions:
                await interaction.followup.send("A Truth-or-Dare session is already active in this server.", ephemeral=True)
                return
            embed = discord.Embed(
                title="Truth or Dare",
                description=f"Creator: {interaction.user.mention}\nPlayers joined: 1/2\nClick Join to participate.",
                color=discord.Color.orange()
            )
            plugin_ref = self
            class JoinView(discord.ui.View):
                def __init__(self):
                    super().__init__(timeout=None)

                @discord.ui.button(label="Join", style=discord.ButtonStyle.primary)
                async def join_button(self, button: discord.ui.Button, inter: discord.Interaction):
                    s = plugin_ref.sessions.get(gid)
                    if not s:
                        await inter.response.send_message("Session not available.", ephemeral=True)
                        return
                    uid = inter.user.id
                    if uid in s["participants"]:
                        await inter.response.send_message("You're already joined.", ephemeral=True)
                        return
                    s["participants"].append(uid)
                    mentions = ", ".join([f"<@{u}>" for u in s["participants"]])
                    s["message"].embed.description = f"Creator: <@{s['creator']}>\nPlayers joined: {len(s['participants'])}/2\n{mentions}"
                    try:
                        await s["message"].edit(embed=s["message"].embed, view=self)
                    except Exception:
                        pass
                    await inter.response.send_message("You joined the session.", ephemeral=True)

                    if len(s["participants"]) >= 2 and not s.get("started"):
                        s["started"] = True
                        plugin_ref.bot.loop.create_task(plugin_ref._start_tod_countdown(gid))
            msg = await interaction.followup.send(embed=embed, view=JoinView())
            self.sessions[gid] = {
                "creator": interaction.user.id,
                "participants": [interaction.user.id],
                "message": msg,
                "started": False
            }
        except Exception:
            traceback.print_exc()
            try:
                await interaction.response.send_message("Error starting Truth-or-Dare.", ephemeral=True)
            except Exception:
                pass
    async def _start_tod_countdown(self, guild_id: int):
        s = self.sessions.get(guild_id)
        if not s:
            return
        for i in range(10, -1, -1):
            try:
                s["message"].embed.description = (
                    f"Creator: <@{s['creator']}>\n"
                    f"Players joined: {len(s['participants'])}/2\n"
                    f"Starting in {i}..."
                )
                await s["message"].edit(embed=s["message"].embed)
            except Exception:
                pass
            await asyncio.sleep(1)

        if not s["participants"]:
            return
        chosen_id = random.choice(s["participants"])
        try:
            chosen = self.bot.get_user(chosen_id) or await self.bot.fetch_user(chosen_id)
        except Exception:
            chosen = None
        assignment = random.choice(["Truth", "Dare"])
        final = discord.Embed(
            title=f"{(chosen.display_name if chosen else 'Player')} — {assignment}",
            description=f"{(chosen.mention if chosen else f'<@{chosen_id}>')} is chosen. They must pick {assignment.lower()}. The other players propose the question or dare.",
            color=discord.Color.dark_gold()
        )
        try:
            await s["message"].edit(embed=final, view=None)
        except Exception:
            pass
        try:
            del self.sessions[guild_id]
        except Exception:
            pass
    # Music recommend
    @app_commands.describe(playlist="Spotify playlist URL or ID")
    async def set_playlist_callback(self, interaction: discord.Interaction, playlist: str = None):
        try:
            if not _is_moderator(interaction):
                await interaction.response.send_message("You need moderator permissions to run this command.", ephemeral=True)
                return
            if not playlist:
                await interaction.response.send_message("Usage: /set-recommend-playlist <playlist URL or ID>", ephemeral=True)
                return
            await interaction.response.defer(ephemeral=True)
            playlist_id = _extract_playlist_id(playlist)
            if not playlist_id:
                await interaction.followup.send("Could not extract a playlist id from that input. Provide a Spotify playlist URL or ID.", ephemeral=True)
                return
            client_id = os.getenv("SPOTIFY_CLIENT_ID")
            client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
            if not (client_id and client_secret):
                await interaction.followup.send("Spotify client credentials are not configured (SPOTIFY_CLIENT_ID/SPOTIFY_CLIENT_SECRET).", ephemeral=True)
                return
            token = await _get_client_credentials_token(client_id, client_secret)
            if not token:
                await interaction.followup.send("Failed to obtain Spotify token. Check client credentials.", ephemeral=True)
                return
            meta = await _get_playlist_metadata(token, playlist_id)
            if not meta:
                await interaction.followup.send("Playlist not found or is not public/accessible. Please provide a valid public playlist.", ephemeral=True)
                return
            playlist_url = meta.get("external_urls", {}).get("spotify", f"https://open.spotify.com/playlist/{playlist_id}")
            success = db.set_music_recommend_playlist(interaction.guild.id if interaction.guild else 0, playlist_id, playlist_url, set_by=interaction.user.id)
            if not success:
                await interaction.followup.send("Failed to save playlist to database.", ephemeral=True)
                return
            name = meta.get("name", "Unknown playlist")
            owner = meta.get("owner", {}).get("display_name", "Unknown owner")
            await interaction.followup.send(f"Saved playlist **{name}** (owner: {owner}). Use /music-recommendation to get tracks.", ephemeral=True)
        except Exception:
            traceback.print_exc()
            try:
                await interaction.response.send_message("An unexpected error occurred while setting the playlist.", ephemeral=True)
            except Exception:
                pass
    async def music_callback(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            if not interaction.guild:
                await interaction.followup.send("This command must be used inside a server.", ephemeral=True)
                return
            doc = db.get_music_recommend_playlist(interaction.guild.id)
            playlist_id: Optional[str] = None
            playlist_was_user_set = False
            if doc and doc.get("playlist_id"):
                playlist_id = doc.get("playlist_id")
                playlist_was_user_set = True
            else:
                playlist_id = DEFAULT_SPOTIFY_PLAYLIST_ID
                playlist_was_user_set = False
            client_id = os.getenv("SPOTIFY_CLIENT_ID")
            client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
            if not (client_id and client_secret):
                await interaction.followup.send("Spotify client credentials are not configured on the bot.", ephemeral=True)
                return
            token = await _get_client_credentials_token(client_id, client_secret)
            if not token:
                await interaction.followup.send("Failed to obtain Spotify access token.", ephemeral=True)
                return
            meta = await _get_playlist_metadata(token, playlist_id)
            if not meta:
                if playlist_was_user_set:
                    await interaction.followup.send("Saved playlist appears to be invalid or private. Please ask a moderator to set a valid public playlist.", ephemeral=True)
                    return
                else:
                    await interaction.followup.send("Default playlist is not accessible at the moment.", ephemeral=True)
                    return
            tracks_info = meta.get("tracks", {}) or {}
            total = int(tracks_info.get("total", 0))
            if total <= 0:
                await interaction.followup.send("Playlist is empty.", ephemeral=True)
                return
            rand_index = random.randrange(0, total)
            tr = await _get_track_by_offset(token, playlist_id, rand_index)
            if not tr:
                await interaction.followup.send("Could not fetch the selected track. Try again.", ephemeral=True)
                return
            name = tr.get("name") or "Unknown"
            artists = ", ".join([a.get("name") for a in tr.get("artists", []) if a.get("name")]) or "Unknown"
            album = tr.get("album", {}).get("name", "Unknown")
            images = tr.get("album", {}).get("images", []) or []
            thumbnail = images[0].get("url") if images else None
            url = tr.get("external_urls", {}).get("spotify")
            duration = _ms_to_mmss(tr.get("duration_ms", 0))
            embed = discord.Embed(title=name, description=artists, color=discord.Color.blurple())
            embed.add_field(name="Album", value=album, inline=True)
            embed.add_field(name="Duration", value=duration, inline=True)
            if url:
                embed.add_field(name="Listen", value=f"[Open on Spotify]({url})", inline=False)
            if thumbnail:
                embed.set_image(url=thumbnail)
            await interaction.followup.send(embed=embed)
        except Exception:
            traceback.print_exc()
            try:
                await interaction.followup.send("An unexpected error occurred while fetching a recommendation.", ephemeral=True)
            except Exception:
                pass

    # --- Get commands ---
    def get_commands(self):
        return [
            self._ship,
            self._fight,
            self._kiss,
            self._hug,
            self._pickup,
            self._who,
            self._catfact,
            self._tod,
            self._set_playlist,
            self._music_recommend
        ]