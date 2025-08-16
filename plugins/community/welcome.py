#Plugin Title: Welcome Commands
#Plugin Version: 0.1.16
#Plugin Author: Suited
# © 2025 Suited. All rights reserved.
# Licensed under Pancake Development License v1.0
# See LICENSE file for full terms

import discord
from discord import Guild, app_commands
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from db import set_welcome_setting, get_welcome_settings
import asyncio
import traceback

EMBED_COLOR_MAP = {
    "default": discord.Color.green(),
    "dark_theme": discord.Color.dark_theme(),
    "red": discord.Color.red(),
    "blue": discord.Color.blue(),
    "green": discord.Color.green(),
    "purple": discord.Color.purple(),
    "orange": discord.Color.orange(),
    "gold": discord.Color.gold()
}

class WelcomePlugin:
    def __init__(self, bot: discord.Client):
        self.bot = bot

        self.default_background = "https://i.imgur.com/Zbkuta8.png"
        self.default_avatar_position = 1
        self.default_avatar_size = 800
        self.default_welcome_text = None
        self.default_embed_color = discord.Color.gold()
        self.default_nick_size = 200
        self.default_nick_position = 1

        @app_commands.command(name="set-welcome-channel", description="Set the channel where welcome messages will be sent.")
        @app_commands.describe(channel="Text channel where welcome messages will appear.")
        async def set_channel(interaction: discord.Interaction, channel: discord.TextChannel):
            if not await self._check_perms(interaction):
                return
            set_welcome_setting(interaction.guild.id, "channel_id", channel.id)
            await interaction.response.send_message(f"Welcome channel set to {channel.mention}.", ephemeral=True)

        @app_commands.command(name="set-welcome-background", description="Set the background image URL for the welcome message.")
        @app_commands.describe(url="Direct URL of the image to use as background.")
        async def set_background(interaction: discord.Interaction, url: str):
            if not await self._check_perms(interaction):
                return
            set_welcome_setting(interaction.guild.id, "background_url", url)
            await interaction.response.send_message("Welcome background updated.", ephemeral=True)

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

        @app_commands.command(name="set-welcome-text", description="Set the welcome text for the embed title.")
        @app_commands.describe(text="Text for the embed title. Use {user} for user mention and {server_name} for server name. Type 'none' to disable.")
        async def set_welcome_text(interaction: discord.Interaction, *, text: str):
            if not await self._check_perms(interaction):
                return
            if text.lower() == "none":
                text = None
            set_welcome_setting(interaction.guild.id, "welcome_text", text)
            await interaction.response.send_message("Welcome text updated.", ephemeral=True)

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

        @app_commands.command(name="set-welcome-nick-size", description="Set the font size (px) of the nickname shown under the avatar.")
        @app_commands.describe(size="Nickname font size in pixels (8 to 200).")
        async def set_nick_size(interaction: discord.Interaction, size: int):
            if not await self._check_perms(interaction):
                return
            if size < 8 or size > 200:
                await interaction.response.send_message("Nick size must be between 8 and 200.", ephemeral=True)
                return
            set_welcome_setting(interaction.guild.id, "nick_size", size)
            await interaction.response.send_message(f"Nickname size set to {size}px.", ephemeral=True)

        @app_commands.command(name="set-welcome-nick-position", description="Set the nickname position relative to the avatar (1=center, 2=right, 3=left).")
        @app_commands.describe(position="1=center, 2=right, 3=left")
        async def set_nick_position(interaction: discord.Interaction, position: int):
            if not await self._check_perms(interaction):
                return
            if position not in (1, 2, 3):
                await interaction.response.send_message("Invalid position. Use 1, 2, or 3.", ephemeral=True)
                return
            set_welcome_setting(interaction.guild.id, "nick_position", position)
            await interaction.response.send_message(f"Nickname position set to {position}.", ephemeral=True)

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

        self._set_channel = set_channel
        self._set_background = set_background
        self._set_avatar_position = set_avatar_position
        self._set_welcome_text = set_welcome_text
        self._set_avatar_size = set_avatar_size
        self._set_nick_size = set_nick_size
        self._set_nick_position = set_nick_position
        self._set_embed_color = set_embed_color
        self._welcome_fire = fire_welcome

    async def _check_perms(self, interaction: discord.Interaction) -> bool:
        if not (interaction.user.guild_permissions.administrator or interaction.user.guild_permissions.manage_channels):
            await interaction.response.send_message("You need Administrator or Manage Channels permissions to use this command.", ephemeral=True)
            return False
        return True

    async def _send_welcome_message(self, guild: discord.Guild, member: discord.Member) -> bool:
        try:
            settings = get_welcome_settings(guild.id)
            if "channel_id" not in settings:
                return False

            channel = guild.get_channel(settings["channel_id"])
            if not channel:
                return False
            nick_size = settings.get("nick_size", self.default_nick_size)
            nick_position = settings.get("nick_position", self.default_nick_position)

            img = await asyncio.to_thread(
                self.generate_welcome_image,
                member,
                settings.get("background_url", self.default_background),
                settings.get("avatar_position", self.default_avatar_position),
                settings.get("avatar_size", self.default_avatar_size),
                nick_size,
                nick_position
            )

            welcome_text = settings.get("welcome_text", self.default_welcome_text)
            if welcome_text:
                welcome_text = welcome_text.replace("{user}", member.mention).replace("{server_name}", guild.name)

            embed_color_key = settings.get("embed_color", None)
            embed_color = EMBED_COLOR_MAP.get(embed_color_key, self.default_embed_color)

            embed = discord.Embed(
                color=embed_color
            )
            embed.set_image(url="attachment://welcome.png")
            file = discord.File(img, filename="welcome.png")

            await channel.send(welcome_text or f"Welcome to {guild.name}!", embed=embed, file=file)
            return True
        except Exception as e:
            print("Error sending welcome message:", e)
            traceback.print_exc()
            return False

    def generate_welcome_image(self, member: discord.Member, background_url: str, avatar_position: int, avatar_size: int, nick_size: int, nick_position: int) -> BytesIO:
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

            if x < 0:
                x = 0
            if y < 0:
                y = 0

            background.paste(avatar, (x, y), avatar)

            def load_truetype_font(preferred_size: int):
                candidates = [
                    "arial.ttf",
                    "DejaVuSans-Bold.ttf",
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                    "/Library/Fonts/Arial.ttf",
                    "/System/Library/Fonts/Supplemental/Arial.ttf"
                ]
                for c in candidates:
                    try:
                        return ImageFont.truetype(c, preferred_size)
                    except Exception:
                        continue
                return ImageFont.load_default()

            try:
                nick_size = int(nick_size)
            except Exception:
                nick_size = self.default_nick_size
            nick_size = max(8, min(200, nick_size))
            font = load_truetype_font(nick_size)

            try:
                name_text = member.name or member.display_name or "User"
                bbox = draw.textbbox((0, 0), name_text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            except Exception:
                try:
                    text_width, text_height = font.getsize(name_text)
                except Exception:
                    text_width, text_height = (100, 20)

            if nick_position == 1:
                text_x = x + (avatar_size - text_width) // 2
            elif nick_position == 2:
                text_x = x + avatar_size - text_width
            else:
                text_x = x

            space_below = background.height - (y + avatar_size)
            margin = 8
            if space_below >= text_height + margin:
                text_y = y + avatar_size + margin
            else:
                text_y = y - text_height - margin
                if text_y < 0:
                    text_x = max(8, min(text_x, background.width - text_width - 1))
                    text_y = max(8, background.height - text_height - margin)

            text_x = max(0, min(text_x, background.width - text_width - 1))
            text_y = max(0, min(text_y, background.height - text_height - 1))

            try:
                shadow_offset = 1
                draw.text((text_x + shadow_offset, text_y + shadow_offset), name_text, font=font, fill=(0, 0, 0))
                draw.text((text_x, text_y), name_text, font=font, fill=(255, 255, 255))
            except Exception:
                try:
                    draw.text((text_x, text_y), name_text, font=font, fill=(255, 255, 255))
                except Exception:
                    pass

            buffer = BytesIO()
            background.save(buffer, "PNG")
            buffer.seek(0)
            return buffer

        except Exception as e:
            try:
                err_img = Image.new("RGBA", (800, 250), (30, 30, 30, 255))
                draw = ImageDraw.Draw(err_img)
                font = ImageFont.load_default()
                msg = "Welcome image error"
                draw.text((10, 10), msg, font=font, fill=(255, 0, 0))
                draw.text((10, 40), str(e)[:200], font=font, fill=(255, 255, 255))
                buffer = BytesIO()
                err_img.save(buffer, "PNG")
                buffer.seek(0)
                return buffer
            except Exception:
                return BytesIO(b"")

    def get_commands(self):
        return [
            self._set_channel,
            self._set_background,
            self._set_avatar_position,
            self._set_welcome_text,
            self._set_avatar_size,
            self._set_nick_size,
            self._set_nick_position,
            self._set_embed_color,
            self._welcome_fire
        ]

# --- Setup With bot.py ---

async def setup(bot: discord.Client, guild: discord.Guild):
    welcome_plugin = WelcomePlugin(bot)
    for cmd in welcome_plugin.get_commands():
        bot.tree.add_command(cmd, guild=guild)
    await bot.tree.sync(guild=guild)

    @bot.event
    async def on_member_join(member: discord.Member):
        try:
            await welcome_plugin._send_welcome_message(member.guild, member)
        except Exception:
            print("Unhandled error in on_member_join:")
            traceback.print_exc()

    return welcome_plugin
