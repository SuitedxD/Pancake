#Plugin Title: Fun Commands Pack No. 1
#Plugin Version: 0.1.2
#Plugin Author: Suited
# © 2025 Suited. All rights reserved.
# Licensed under Pancake Development License v1.0

# --- Imports ---

# Main
import discord
import random
from discord import app_commands

# --- Plugin ---

class Fun1Plugin:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self._dice = app_commands.Command(
            name="dice",
            description="Rolls an imaginary dice and tells you the result.",
            callback=self.dice
        )
        self._coinflip = app_commands.Command(
            name="coinflip",
            description="Flips a hypothetical coin and tells you the result.",
            callback=self.coinflip
        )
        self._eightball = app_commands.Command(
            name="8ball",
            description="Ask and let Pancake enlighten you with his wisdom.",
            callback=self.eightball
        )
        self._howgay = app_commands.Command(
            name="howgay",
            description="Checks your gay percentage... very scientific.",
            callback=self.howgay
        )
        self._mood = app_commands.Command(
            name="mood",
            description="Detects your current mood based on nothing.",
            callback=self.mood
        )
        self._randomnumber = app_commands.Command(
            name="random-number",
            description="Gives you a random number.",
            callback=self.random_number
        )
        self._dare = app_commands.Command(
            name="dare",
            description="Pancake dares you to do something dumb because why not?",
            callback=self.dare
        )
    # Commands 2    
    async def dice(self, interaction: discord.Interaction):
        result = random.randint(1, 6)
        await interaction.response.send_message(f"Your imaginary result is: {result}! 🎲")
    async def coinflip(self, interaction: discord.Interaction):
        result = random.choice(["Heads.", "Tails."])
        await interaction.response.send_message(f"You got: {result}")
    # 8ball
    @app_commands.describe(question="Type your yes/no question")
    async def eightball(self, interaction: discord.Interaction, question: str):
        responses = [
            "Yeah why not?",
            "No, just no.",
            "Try again later im making pancakes.",
            "idk.",
            "Yesss... nah better not.",
            "In another life, maybe...",
            "Definitely not... or maybe?",
            "I dont know, ask chat gpt."
        ]
        answer = random.choice(responses)
        await interaction.response.send_message(f"🎱 You asked: **{question}**\nPancake says: *{answer}*")
    # howgay
    async def howgay(self, interaction: discord.Interaction):
        percentage = random.randint(0, 100)
        await interaction.response.send_message(f"🏳️‍🌈 You're {percentage}% gay! Congrats or condolences.")
    # mood
    async def mood(self, interaction: discord.Interaction):
        moods = ["Happy 😄", "Sad 😢", "Angry 😡", "Chaotic 😈", "Sleepy 😴", "Hungry 🍕"]
        await interaction.response.send_message(f"Your current mood is: {random.choice(moods)}")
    # random num
    async def random_number(self, interaction: discord.Interaction):
        number = random.randint(0, 1000)
        await interaction.response.send_message(f"Your random number is: **{number}**")
    # dare
    async def dare(self, interaction: discord.Interaction):
        dares = [
            "Send a heart emoji to your crush right now.",
            "Change your nickname to 'Pancakes4Ever' for 10 mins.",
            "Say 'I'm Pancake's lover' in general chat.",
            "Type only in emojis for the next 5 messages.",
            "Sing your last message out loud and i want proof of that."
        ]
        await interaction.response.send_message(f"🔥 {random.choice(dares)}")
    # Get Commands
    def get_commands(self):
        return [
            self._dice,
            self._coinflip,
            self._eightball,
            self._howgay,
            self._mood,
            self._randomnumber,
            self._dare
        ]