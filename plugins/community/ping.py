#Plugin Title: Ping
#Plugin Version: 0.1.0
#Plugin Author: Suited
# © 2025 Suited. All rights reserved.
# Licensed under Pancake Development License v1.0
# See LICENSE file for full terms

import discord
from discord import app_commands

class PingPlugin:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self._ping = app_commands.Command(
            name="ping",
            description="If you ping to Pancake he should play along but maybe would try to dominate the world so be careful.",
            callback=self.ping
        )
        self._pingms = app_commands.Command(
            name="ping-ms",
            description="Pancake should return his latency in miliseconds. I say 'should' bc he sent me my IP address :(",
            callback=self.ping_ms
        )

    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("I'm going to take over the world muahahahah 😈— I mean... Pong! 😇")

    async def ping_ms(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"I like you so I won't steal your IP, for now... 😈🥞 *(Latenecy of this messasge: **{latency}ms**)*")

    def get_commands(self):
        return [self._ping, self._pingms]
