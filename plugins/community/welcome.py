#Welcome Commands
#Plugin Version: 0.1.16

import discord
from discord import Guild, app_commands
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from db import set_welcome_setting, get_welcome_settings

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

class WelcomeCommand:
    def __init__(self, bot: discord.Client):
        self.bot = bot

        self.default_background = "https://i.imgur.com/8Y40xLS.png"
        self.default_avatar_position = 1
        self.default_avatar_size = 700
        self.default_welcome_text = None
        self.default_embed_color = discord.Color.gold()

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
            guild_id = interaction.guild.id
            settings = get_welcome_settings(guild_id)
            if "channel_id" not in settings:
                await interaction.response.send_message("You need to set a welcome channel first.", ephemeral=True)
                return

            channel = interaction.guild.get_channel(settings["channel_id"])
            if not channel:
                await interaction.response.send_message("The configured welcome channel no longer exists.", ephemeral=True)
                return

            img = self.generate_welcome_image(
                interaction.user,
                settings.get("background_url", self.default_background),
                settings.get("avatar_position", self.default_avatar_position),
                settings.get("avatar_size", self.default_avatar_size)
            )

            welcome_text = settings.get("welcome_text", self.default_welcome_text)
            if welcome_text:
                welcome_text = welcome_text.replace("{user}", interaction.user.mention).replace("{server_name}", interaction.guild.name)

            embed_color_key = settings.get("embed_color", None)
            embed_color = EMBED_COLOR_MAP.get(embed_color_key, self.default_embed_color)

            embed = discord.Embed(
                description=welcome_text or f"Welcome to {interaction.guild.name}!",
                color=embed_color
            )
            embed.set_image(url="attachment://welcome.png")
            file = discord.File(img, filename="welcome.png")

            await interaction.response.send_message("Welcome message sent.", ephemeral=True)
            await channel.send(embed=embed, file=file)

        self._set_channel = set_channel
        self._set_background = set_background
        self._set_avatar_position = set_avatar_position
        self._set_welcome_text = set_welcome_text
        self._set_avatar_size = set_avatar_size
        self._set_embed_color = set_embed_color
        self._welcome_fire = fire_welcome

    async def _check_perms(self, interaction: discord.Interaction) -> bool:
        if not (interaction.user.guild_permissions.administrator or interaction.user.guild_permissions.manage_channels):
            await interaction.response.send_message("You need Administrator or Manage Channels permissions to use this command.", ephemeral=True)
            return False
        return True

    def generate_welcome_image(self, member: discord.Member, background_url: str, avatar_position: int, avatar_size: int) -> BytesIO:
        def safe_download_image(url: str, fallback_url: str) -> Image.Image:
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                resp = requests.get(url, headers=headers, timeout=5)
                resp.raise_for_status()
                return Image.open(BytesIO(resp.content)).convert("RGBA")
            except:
                try:
                    resp = requests.get(fallback_url, headers=headers, timeout=5)
                    resp.raise_for_status()
                    return Image.open(BytesIO(resp.content)).convert("RGBA")
                except:
                    return Image.new("RGBA", (800, 400), (30, 30, 30, 255))

        background = safe_download_image(background_url, self.default_background)
        draw = ImageDraw.Draw(background)

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

        background.paste(avatar, (x, y), avatar)

        font = ImageFont.load_default()
        draw.text((20, 20), f"Welcome, {member.mention}!", font=font, fill=(255, 255, 255))

        buffer = BytesIO()
        background.save(buffer, "PNG")
        buffer.seek(0)
        return buffer

    def get_commands(self):
        return [
            self._set_channel,
            self._set_background,
            self._set_avatar_position,
            self._set_welcome_text,
            self._set_avatar_size,
            self._set_embed_color,
            self._welcome_fire
        ]

async def setup(bot: discord.Client, guild: discord.Guild):
    welcome_plugin = WelcomeCommand(bot)
    for cmd in welcome_plugin.get_commands():
        bot.tree.add_command(cmd, guild=guild)
    await bot.tree.sync(guild=guild)

    @bot.event
    async def on_member_join(member: discord.Member):
        settings = get_welcome_settings(member.guild.id)
        if "channel_id" not in settings:
            return

        channel = member.guild.get_channel(settings["channel_id"])
        if not channel:
            return

        img = welcome_plugin.generate_welcome_image(
            member,
            settings.get("background_url", welcome_plugin.default_background),
            settings.get("avatar_position", welcome_plugin.default_avatar_position),
            settings.get("avatar_size", welcome_plugin.default_avatar_size)
        )

        welcome_text = settings.get("welcome_text", welcome_plugin.default_welcome_text)
        if welcome_text:
            welcome_text = welcome_text.replace("{user}", member.mention).replace("{server_name}", member.guild.name)

        embed_color_key = settings.get("embed_color", None)
        embed_color = EMBED_COLOR_MAP.get(embed_color_key, welcome_plugin.default_embed_color)

        embed = discord.Embed(
            description=welcome_text or f"Welcome to {member.guild.name}!",
            color=embed_color
        )
        embed.set_image(url="attachment://welcome.png")
        file = discord.File(img, filename="welcome.png")

        await channel.send(embed=embed, file=file)

    return welcome_plugin
