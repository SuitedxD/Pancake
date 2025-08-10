#Moderation Commands Pack No. 1
#Plugin Version: 0.1.0

import discord
import datetime
import re
from discord import app_commands
from typing import Optional

class Mod1Command:
    def __init__(self, bot: discord.Client):
        self.bot = bot

        self._ban = app_commands.Command(
            name="ban",
            description="Ban a member from the server.",
            callback=self.ban_callback
        )

        self._unban = app_commands.Command(
            name="unban",
            description="Unban a previously banned user by ID or mention.",
            callback=self.unban_callback
        )

        self._kick = app_commands.Command(
            name="kick",
            description="Kick a member from the server.",
            callback=self.kick_callback
        )

        self._mute = app_commands.Command(
            name="mute",
            description="Mute (timeout) a member for a specific duration (format: 10m, 1h, 30s).",
            callback=self.mute_callback
        )

        self._unmute = app_commands.Command(
            name="unmute",
            description="Remove timeout (mute) from a member.",
            callback=self.unmute_callback
        )

        self._clear = app_commands.Command(
            name="clear",
            description="Delete a number of messages from the current channel (1-100).",
            callback=self.clear_callback
        )

        self._slowmode = app_commands.Command(
            name="slowmode",
            description="Set slowmode delay (seconds) in the current channel. 0 disables slowmode.",
            callback=self.slowmode_callback
        )

        self._lock = app_commands.Command(
            name="lock",
            description="Lock the current channel for a specific role (disables send_messages).",
            callback=self.lock_callback
        )

        self._unlock = app_commands.Command(
            name="unlock",
            description="Unlock the current channel for a specific role (enables send_messages).",
            callback=self.unlock_callback
        )

    def parse_duration(self, duration_str: str) -> Optional[datetime.timedelta]:
        match = re.match(r"^(\d+)([smhd])$", duration_str)
        if not match:
            return None
        value, unit = match.groups()
        value = int(value)
        if unit == "s":
            return datetime.timedelta(seconds=value)
        if unit == "m":
            return datetime.timedelta(minutes=value)
        if unit == "h":
            return datetime.timedelta(hours=value)
        if unit == "d":
            return datetime.timedelta(days=value)
        return None

    # Commands

    @app_commands.describe(member="Member to ban", reason="Reason for the ban (optional)")
    async def ban_callback(self, interaction: discord.Interaction, member: discord.Member, reason: Optional[str] = None):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("❌ You don't have permission to ban members.", ephemeral=True)
            return

        await interaction.response.defer()
        try:
            await member.ban(reason=reason)
            await interaction.followup.send(f"✅ {member.mention} has been banned. Reason: {reason or 'No reason provided'}")
        except discord.Forbidden:
            await interaction.followup.send("**ERR**: Pancake doesn't have permission to ban that user.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"**ERR**: Failed to ban: {e}", ephemeral=True)

    @app_commands.describe(user_id="User ID (digits) or mention of the user to unban")
    async def unban_callback(self, interaction: discord.Interaction, user_id: str):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("❌ You don't have permission to unban members.", ephemeral=True)
            return

        raw_id = re.sub(r"\D", "", user_id)
        if not raw_id:
            await interaction.response.send_message("**ERR**: Invalid user id or mention.", ephemeral=True)
            return

        await interaction.response.defer()
        try:
            uid = int(raw_id)
            user = await self.bot.fetch_user(uid)
            await interaction.guild.unban(user)
            await interaction.followup.send(f"✅ {user} has been unbanned.")
        except discord.NotFound:
            await interaction.followup.send("**ERR**: That user is not in the ban list.", ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send("**ERR**: Pancake doesn't have permission to unban that user.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"**ERR**: Failed to unban: {e}", ephemeral=True)

    @app_commands.describe(member="Member to kick", reason="Reason for the kick (optional)")
    async def kick_callback(self, interaction: discord.Interaction, member: discord.Member, reason: Optional[str] = None):
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("❌ You don't have permission to kick members.", ephemeral=True)
            return

        await interaction.response.defer()
        try:
            await member.kick(reason=reason)
            await interaction.followup.send(f"✅ {member.mention} has been kicked. Reason: {reason or 'No reason provided'}")
        except discord.Forbidden:
            await interaction.followup.send("**ERR**: Pancake doesn't have permission to kick that user.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"**ERR**: Failed to kick: {e}", ephemeral=True)

    @app_commands.describe(member="Member to mute", duration="Duration like 10m, 1h, 30s (s/m/h/d)", reason="Reason for mute (optional)")
    async def mute_callback(self, interaction: discord.Interaction, member: discord.Member, duration: str, reason: Optional[str] = None):
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("❌ You don't have permission to mute members.", ephemeral=True)
            return

        parsed = self.parse_duration(duration)
        if parsed is None:
            await interaction.response.send_message("**ERR**: Invalid duration format. Use examples like: 10m, 1h, 30s, 2d.", ephemeral=True)
            return

        await interaction.response.defer()
        try:
            await member.timeout(parsed, reason=reason)
            await interaction.followup.send(f"✅ {member.mention} has been muted for {duration}. Reason: {reason or 'No reason provided'}")
        except discord.Forbidden:
            await interaction.followup.send("**ERR**: Pancake doesn't have permission to mute that user.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"**ERR**: Failed to mute: {e}", ephemeral=True)

    @app_commands.describe(member="Member to unmute")
    async def unmute_callback(self, interaction: discord.Interaction, member: discord.Member):
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("❌ You don't have permission to unmute members.", ephemeral=True)
            return

        await interaction.response.defer()
        try:
            await member.timeout(None)
            await interaction.followup.send(f"✅ {member.mention} has been unmuted.")
        except discord.Forbidden:
            await interaction.followup.send("**ERR**: Pancake doesn't have permission to unmute that user.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"**ERR**: Failed to unmute: {e}", ephemeral=True)

    @app_commands.describe(amount="Number of messages to delete (max 100).")
    async def clear_callback(self, interaction: discord.Interaction, amount: int):
        if not interaction.user.guild_permissions.manage_messages:
            return await interaction.response.send_message("❌ You do not have permission to manage messages.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)

        if amount < 1 or amount > 100:
            return await interaction.followup.send("**ERR**: Amount must be between 1 and 100.", ephemeral=True)

        try:
            deleted = await interaction.channel.purge(limit=amount)
            deleted_count = len(deleted)
            await interaction.followup.send(f"✅ Deleted {deleted_count} message(s).", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"**ERR**: Failed to delete messages: {e}", ephemeral=True)

    @app_commands.describe(delay="Slowmode delay in seconds (0 to 21600). Use 0 to disable.")
    async def slowmode_callback(self, interaction: discord.Interaction, delay: app_commands.Range[int, 0, 21600]):
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("❌ You don't have permission to set slowmode.", ephemeral=True)
            return

        await interaction.response.defer()
        try:
            await interaction.channel.edit(slowmode_delay=delay)
            if delay == 0:
                await interaction.followup.send("✅ Slowmode disabled for this channel.")
            else:
                await interaction.followup.send(f"✅ Slowmode set to {delay} second(s).")
        except discord.Forbidden:
            await interaction.followup.send("**ERR**: Pancake doesn't have permission to edit this channel.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"**ERR**: Failed to set slowmode: {e}", ephemeral=True)

    @app_commands.describe(role="Role to lock in the current channel (send_messages will be disabled for this role)")
    async def lock_callback(self, interaction: discord.Interaction, role: discord.Role):
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("❌ You don't have permission to lock channels.", ephemeral=True)
            return

        await interaction.response.defer()
        try:
            overwrite = interaction.channel.overwrites_for(role)
            overwrite.send_messages = False
            await interaction.channel.set_permissions(role, overwrite=overwrite)
            await interaction.followup.send(f"🔒 Channel locked for {role.mention}.")
        except discord.Forbidden:
            await interaction.followup.send("**ERR**: Pancake doesn't have permission to edit channel permissions.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"**ERR** Failed to lock channel: {e}", ephemeral=True)

    @app_commands.describe(role="Role to unlock in the current channel (send_messages will be enabled for this role)")
    async def unlock_callback(self, interaction: discord.Interaction, role: discord.Role):
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("❌ You don't have permission to unlock channels.", ephemeral=True)
            return

        await interaction.response.defer()
        try:
            overwrite = interaction.channel.overwrites_for(role)
            overwrite.send_messages = True
            await interaction.channel.set_permissions(role, overwrite=overwrite)
            await interaction.followup.send(f"🔓 Channel unlocked for {role.mention}.")
        except discord.Forbidden:
            await interaction.followup.send("**ERR**: Pancake doesn't have permission to edit channel permissions.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"**ERR**: Failed to unlock channel: {e}", ephemeral=True)

    def get_commands(self):
        return [
            self._ban,
            self._unban,
            self._kick,
            self._mute,
            self._unmute,
            self._clear,
            self._slowmode,
            self._lock,
            self._unlock
        ]
