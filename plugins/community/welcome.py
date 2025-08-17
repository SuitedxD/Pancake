# Plugin Title: Welcome Commands
# Plugin Version: 0.1.18
# Plugin Author: Suited
# © 2025 Suited. All rights reserved.
# Licensed under Pancake Development License v1.0

# --- Imports ---

# Main
import os
import discord
from discord import app_commands
import asyncio
import traceback
# Pillow
from PIL import Image, ImageDraw, ImageFont
# Download Welcome
import requests
from io import BytesIO
# Database
from db import set_welcome_setting, get_welcome_settings

# --- Embed Colors ---

EMBED_COLOR_MAP = {
    "default": discord.Color.gold(),
    "dark_theme": discord.Color.dark_theme(),
    "red": discord.Color.red(),
    "blue": discord.Color.blue(),
    "green": discord.Color.green(),
    "purple": discord.Color.purple(),
    "orange": discord.Color.orange(),
    "gold": discord.Color.gold()
}

# --- Get Font ---

def _resolve_font_path() -> str | None:
    here = os.path.abspath(os.path.dirname(__file__))
    # directories to check
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
# Load font. If not found will return ImageFont.load_default().
    px = int(max(50, min(1024, px)))
    if _FONT_PATH:
        try:
            with open(_FONT_PATH, "rb") as f:
                b = f.read()
            return ImageFont.truetype(BytesIO(b), px)
        except Exception:
            pass
    # Emergency fallback.
    return ImageFont.load_default()

# --- Plugin ---

class WelcomePlugin:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        
        # Default setttings
        self.default_background = "https://i.imgur.com/Zbkuta8.png"
        self.default_avatar_position = 1
        self.default_avatar_size = 800
        self.default_welcome_text = None
        self.default_embed_color = discord.Color.gold()
        self.default_nick_size = 200
        # Commands
        # set-welcome-channel
        @app_commands.command(name="set-welcome-channel", description="Set the channel where welcome messages will be sent.")
        @app_commands.describe(channel="Select where Pancake will sent the welcome message when a new user joins or when you execute '/welcome-fire'.")
        async def set_channel(interaction: discord.Interaction, channel: discord.TextChannel):
            if not await self._check_perms(interaction):
                return
            set_welcome_setting(interaction.guild.id, "channel_id", channel.id)
            await interaction.response.send_message(f"Welcome channel set to {channel.mention}. The new welcome messages will be sent there.", ephemeral=True)
        # set-welcome-background
        @app_commands.command(name="set-welcome-background", description="Set the background image URL for the welcome message.")
        @app_commands.describe(url="Inset the URL of the image to use as background. ")
        async def set_background(interaction: discord.Interaction, url: str):
            if not await self._check_perms(interaction):
                return
            set_welcome_setting(interaction.guild.id, "background_url", url)
            await interaction.response.send_message("Welcome background updated.", ephemeral=True)
        # set-welcome-avatar-position
        @app_commands.command(name="set-welcome-avatar-position", description="Set the avatar position on the welcome image.")
        @app_commands.describe(position="1=center, 2=right, 3=left")
        async def set_avatar_position(interaction: discord.Interaction, position: int):
            if not await self._check_perms(interaction):
                return
            if position not in (1, 2, 3):
                await interaction.response.send_message("Invalid position. Use 1, 2, or 3.", ephemeral=True)
                return
            set_welcome_setting(interaction.guild.id, "avatar_position", position)
            await interaction.response.send_message(f"Avatar position set to {position}.", ephemeral=True)
        # set-welcome-text
        @app_commands.command(name="set-welcome-text", description="Set the welcome text for the embed title.")
        @app_commands.describe(text="Text for the embed title. Use {user} for user mention and {server_name} for server name. Type 'none' to disable.")
        async def set_welcome_text(interaction: discord.Interaction, *, text: str):
            if not await self._check_perms(interaction):
                return
            if text.lower() == "none":
                text = None
            set_welcome_setting(interaction.guild.id, "welcome_text", text)
            await interaction.response.send_message("Welcome text updated.", ephemeral=True)
        # set-welcome-avatar-size
        @app_commands.command(name="set-welcome-avatar-size", description="Set the size of the avatar in the welcome image.")
        @app_commands.describe(size="Avatar size in pixels (50 to 1024).")
        async def set_avatar_size(interaction: discord.Interaction, size: int):
            if not await self._check_perms(interaction):
                return
            if size < 50 or size > 1024:
                await interaction.response.send_message("Avatar size must be between 50 and 1024.", ephemeral=True)
                return
            set_welcome_setting(interaction.guild.id, "avatar_size", size)
            await interaction.response.send_message(f"Avatar size set to {size}px.", ephemeral=True)
        # set-welcome-nick-size
        @app_commands.command(name="set-welcome-nick-size", description="Set the font size (px) of the nickname shown under the avatar.")
        @app_commands.describe(size="Nickname font size in pixels (50 to 1024).")
        async def set_nick_size(interaction: discord.Interaction, size: int):
            if not await self._check_perms(interaction):
                return
            if size < 50 or size > 1024:
                await interaction.response.send_message("Nick size must be between 50 and 1024.", ephemeral=True)
                return
            set_welcome_setting(interaction.guild.id, "nick_size", size)
            await interaction.response.send_message(f"Nickname size set to {size}px.", ephemeral=True)
        # set-welcome-embed-color
        @app_commands.command(name="set-welcome-embed-color", description="Set the embed color for the welcome message.")
        @app_commands.describe(color="Color name (dark_theme, red, blue, green, purple, orange, gold).")
        async def set_embed_color(interaction: discord.Interaction, color: str):
            if not await self._check_perms(interaction):
                return
            color = color.lower()
            if color not in EMBED_COLOR_MAP:
                await interaction.response.send_message(f"Invalid color. Choose one of: {', '.join(EMBED_COLOR_MAP.keys())}", ephemeral=True)
                return
            set_welcome_setting(interaction.guild.id, "embed_color", color)
            await interaction.response.send_message(f"Embed color set to {color}.", ephemeral=True)
        # welcome-fire
        @app_commands.command(name="welcome-fire", description="Test the welcome message by sending it to the configured channel.")
        async def fire_welcome(interaction: discord.Interaction):
            await interaction.response.defer(ephemeral=True)
            try:
                sent = await self._send_welcome_message(interaction.guild, interaction.user)
                if sent:
                    await interaction.followup.send("Welcome message sent.", ephemeral=True)
                else:
                    await interaction.followup.send("You need to set a valid welcome channel first.", ephemeral=True)
            except Exception as e:
                await interaction.followup.send(f"Error sending welcome: {e}", ephemeral=True)
        # callback
        self._set_channel = set_channel
        self._set_background = set_background
        self._set_avatar_position = set_avatar_position
        self._set_welcome_text = set_welcome_text
        self._set_avatar_size = set_avatar_size
        self._set_nick_size = set_nick_size
        self._set_embed_color = set_embed_color
        self._welcome_fire = fire_welcome
    # Check Permissions
    async def _check_perms(self, interaction: discord.Interaction) -> bool:
        if not (interaction.user.guild_permissions.administrator or interaction.user.guild_permissions.manage_channels):
            await interaction.response.send_message("You need Administrator or Manage Channels permissions to use this command.", ephemeral=True)
            return False
        return True
    # Welcome Message
    async def _send_welcome_message(self, guild: discord.Guild, member: discord.Member) -> bool:
        try:
            settings = get_welcome_settings(guild.id)
            if "channel_id" not in settings:
                return False
            channel = guild.get_channel(settings["channel_id"]) if isinstance(guild, discord.Guild) else None
            if not channel:
                return False
            nick_size = settings.get("nick_size", self.default_nick_size)
            img = await asyncio.to_thread(
                self.generate_welcome_image,
                member,
                settings.get("background_url", self.default_background),
                settings.get("avatar_position", self.default_avatar_position),
                settings.get("avatar_size", self.default_avatar_size),
                nick_size
            )
            welcome_text = settings.get("welcome_text", self.default_welcome_text)
            if welcome_text:
                welcome_text = welcome_text.replace("{user}", member.mention).replace("{server_name}", guild.name)
            embed_color_key = settings.get("embed_color", None)
            embed_color = EMBED_COLOR_MAP.get(embed_color_key, self.default_embed_color)
            embed = discord.Embed(color=embed_color)
            embed.set_image(url="attachment://welcome.png")
            file = discord.File(img, filename="welcome.png")
            await channel.send(welcome_text or f"Welcome to {guild.name}!", embed=embed, file=file)
            return True
        except Exception:
            traceback.print_exc()
            return False
    async def _on_member_join(self, member: discord.Member):
        try:
            await self._send_welcome_message(member.guild, member)
        except Exception:
            traceback.print_exc()
    def _measure_text(self, draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> tuple[int, int]:
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
                    return (len(text) * max(1, getattr(font, 'size', 16)) // 2, max(16, getattr(font, 'size', 16)))
    def generate_welcome_image(self, member: discord.Member, background_url: str, avatar_position: int, avatar_size: int, nick_size: int) -> BytesIO:
        try:
            def safe_download_image(url: str, fallback_url: str) -> Image.Image:
                headers = {"User-Agent": "Mozilla/5.0"}
                try:
                    resp = requests.get(url, headers=headers, timeout=6)
                    resp.raise_for_status()
                    return Image.open(BytesIO(resp.content)).convert("RGBA")
                except Exception:
                    try:
                        resp = requests.get(fallback_url, headers=headers, timeout=6)
                        resp.raise_for_status()
                        return Image.open(BytesIO(resp.content)).convert("RGBA")
                    except Exception:
                        return Image.new("RGBA", (800, 400), (30, 30, 30, 255))
            background = safe_download_image(background_url, self.default_background)
            min_w, min_h = 400, 200
            if background.width < min_w or background.height < min_h:
                background = background.resize((max(background.width, min_w), max(background.height, min_h)))
            draw = ImageDraw.Draw(background)
            # Avatar 
            try:
                avatar_size = int(avatar_size)
            except Exception:
                avatar_size = self.default_avatar_size
            avatar_size = max(50, min(1024, avatar_size))
            max_avatar = min(background.width - 40, background.height - 80)
            avatar_size = min(avatar_size, max(50, max_avatar))
            avatar_url = str(member.display_avatar.url)
            avatar = safe_download_image(avatar_url, avatar_url).resize((avatar_size, avatar_size))
            mask = Image.new("L", avatar.size, 0)
            ImageDraw.Draw(mask).ellipse((0, 0, avatar.size[0], avatar.size[1]), fill=255)
            avatar.putalpha(mask)
            if avatar_position == 1:
                x = background.width // 2 - avatar_size // 2
            elif avatar_position == 2:
                x = background.width - avatar_size - 20
            else:
                x = 20
            y = background.height // 2 - avatar_size // 2
            x = max(0, x)
            y = max(0, y)
            background.paste(avatar, (x, y), avatar)
            # Nickname
            try:
                nick_size = int(nick_size)
            except Exception:
                nick_size = self.default_nick_size
            nick_size = max(50, min(1024, nick_size))
            name_text = (getattr(member, "display_name", None) or getattr(member, "name", None) or "User").strip()
            font = _load_font(nick_size)
            text_w, text_h = self._measure_text(draw, name_text, font)
            # Keep text within avatar width, if it exceeds reduce size proportionally
            max_text_w = max(50, avatar_size)
            if text_w > max_text_w and _FONT_PATH:
                scale = max_text_w / float(text_w)
                new_px = max(12, int(nick_size * scale))
                font = _load_font(new_px)
                text_w, text_h = self._measure_text(draw, name_text, font)
            margin = 8
            text_x = x + (avatar_size - text_w) // 2
            text_y = y + avatar_size + margin
            # If it doesn't fit below, try above
            if text_y + text_h + margin > background.height:
                text_y = y - text_h - margin
                if text_y < 0:
                    text_y = max(8, background.height - text_h - margin)
                    text_x = max(8, min(text_x, background.width - text_w - 1))
            text_x = max(0, min(text_x, background.width - text_w - 1))
            text_y = max(0, min(text_y, background.height - text_h - 1))
            draw.text((text_x, text_y), name_text, font=font, fill=(255, 255, 255))
            buffer = BytesIO()
            background.save(buffer, "PNG")
            buffer.seek(0)
            return buffer
        except Exception:
            try:
                err_img = Image.new("RGBA", (800, 250), (30, 30, 30, 255))
                draw = ImageDraw.Draw(err_img)
                font = ImageFont.load_default()
                msg = "Welcome image error"
                draw.text((10, 10), msg, font=font, fill=(255, 0, 0))
                buffer = BytesIO()
                err_img.save(buffer, "PNG")
                buffer.seek(0)
                return buffer
            except Exception:
                return BytesIO(b"")
    # Get Commands
    def get_commands(self):
        return [
            self._set_channel,
            self._set_background,
            self._set_avatar_position,
            self._set_welcome_text,
            self._set_avatar_size,
            self._set_nick_size,
            self._set_embed_color,
            self._welcome_fire
        ]


# --- Setup With bot.py ---

async def setup(bot: discord.Client, guild: discord.Guild):
    if getattr(bot, "_welcome_setup_done", False):
        return getattr(bot, "_welcome_plugin", None)
    welcome_plugin = WelcomePlugin(bot)
    bot._welcome_plugin = welcome_plugin
    bot._welcome_setup_done = True
    existing_commands = {cmd.name for cmd in bot.tree.get_commands(guild=None)}
    try:
        existing_commands.update({cmd.name for cmd in bot.tree.get_commands(guild=guild)})
    except Exception:
        pass
    for cmd in welcome_plugin.get_commands():
        if cmd.name in existing_commands:
            continue
        try:
            bot.tree.add_command(cmd, guild=guild)
        except Exception:
            continue
    try:
        await bot.tree.sync(guild=guild)
    except Exception:
        pass
    if not getattr(bot, "_welcome_on_member_join_registered", False):
        bot.add_listener(welcome_plugin._on_member_join, "on_member_join")
        bot._welcome_on_member_join_registered = True
    return welcome_plugin