# ===========================
#      Plugin Example
# ===========================

# This is a basic example/template of how a Pancake plugin should be structured.
# Use this as a starting point to create your own plugin.

# This code is free to use, it is not protected under the Pancake Development License.

# Pancake uses Python. Your entire plugin must be written in Python, 
# and compatible with the Discord API via discord.py and discord.app_commands.

# (Insert your plugin name here)
# (Insert your description here)
# (Insert your plugin categories here)

# A plugin is a group of slash commands wrapped into a single class.
# Each command is created using app_commands.Command, which requires a name, description, and a callback.
# Your class must implement a method called get_commands() that returns all commands as a list.
# Pancake uses this method to install and remove plugins dynamically.
# You MUST follow the Plugin Guidelines to get your plugin accepted.

import discord
from discord import app_commands

# Replace "Example" with a unique name for your plugin class.
# It is mandatory that you be accompanied by "Plugin" as below.
# This class represents the entire plugin and will be used to identify and install your plugin.
# It must be unique across all Pancake plugins. Avoid using generic names.
class ExamplePlugin:
    def __init__(self, bot: discord.Client):
        self.bot = bot

        # Plugin 1: /example
        # This creates a simple slash command named "example".
        # The callback points to the method that will run when the command is used.
        self._example = app_commands.Command(
            name="example",  # the actual command name in Discord
            description="A simple example command.",
            callback=self.example_callback
        )

        # Command 2: /status
        # This is another command in the same plugin. You can add as many as needed.
        self._status = app_commands.Command(
            name="status",
            description="Returns the bot latency.",
            callback=self.status_callback
        )

    # This is the function that will be triggered by /example.
    # It sends a basic response to the user.
    async def example_callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("This is an example response from your plugin.")

    # This is the function that will be triggered by /status.
    # It shows how to use internal bot data like latency.
    async def status_callback(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)  # latency in milliseconds
        await interaction.response.send_message(f"Current bot latency: {latency}ms")

    # This function must return all the commands defined in your plugin.
    # Pancake uses this list to register the commands when the plugin is installed.
    def get_commands(self):
        return [self._example, self._status]

# Notes:
# - Avoid using forbidden functions or libraries (see the Guidelines).
# - Keep your code clean and understandable.
# - You can comment your code to explain how it works; this helps us during review.
# - Use descriptive command names and clear descriptions for each command.
# - You can include optional logic, buttons, or views if you stay within safe practices.
# - Always test your plugin before submitting.
# - Good luck!