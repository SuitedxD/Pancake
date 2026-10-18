# ===========================
#      Plugin Example/Template
# ===========================

# This is a basic example/template of how a Pancake plugin should be structured.
# Use this as a starting point to create your own plugin.

# This code is free to use, it is not protected under the Pancake Development License.

# Pancake uses Python. Your entire plugin must be written in Python, 
# and compatible with the Discord API via discord.py and discord.app_commands.

# A plugin is a group of slash commands wrapped into a single class.
# Each command is created using app_commands.Command, which requires a name, description, and a callback.
# Your class must implement a method called get_commands() that returns all commands as a list.
# Pancake uses this method to install and remove plugins dynamically.
# You MUST follow the Plugin Guidelines to get your plugin accepted.

# --- Your Plugin Starts Here ---

# IMPORTANT NOTE: PLEASE, IT IS IMPORTANT THAT YOU FILL OUT THE FOLLOWING FORM, 
# AS IT WILL BE THE ONE USED FOR PUBLICATION ON THE PLUGIN PORTAL.
# FAILURE TO DO SO RESULTS IN IMMEDIATE REJECTION.

# PLUGIN TITLE: (for example: Web Embeds)
# YOUR DISCORD ID: (for example: 775194414535409705)
# PLUGIN DESCRIPTION: (for example: Create embed messages quickly and easily! you can use markdown here btw)
# PLUGIN INSTALLATION COMMAND: (for example: /install plugin:web_embed)
# COVER IMAGE URL (OPTIONAL, RECOMMENDED SIZE 1200x630): (for example: https://i.imgur.com/qDtjEFw.png)
# CATEGORIES: (you can see all categories here: https://github.com/SuitedxD/Pancake/blob/main/docs/plugins-guidelines.md#plugin-categories)

# ENTER YOUR PLUGIN'S COMMANDS BELOW, 
# ALONG WITH A DESCRIPTION OF WHAT EACH ONE DOES:

# command:
# /web-embed-fire 
# description:
# Send your embed message using your previously generated Embed Code in the Pancake Embed Editor.

# command:
# /perms-web-embed (Permission level)
# description:
# Assign the permissions level required to use web-embed-fire. For example: Moderators.

# ADITIONAL IMAGE URLs (OPTIONAL GALLERY IMAGES. ONE URL PER LINE, UP TO 12 IMAGES):

# YOUTUBE VIDEO URLs (OPTIONAL VIDEOS. ADD ONE YOUTUBE PER LINE, UP TO 5 VIDEOS):

# ADDITIONAL NOTES:
# (you can aslo use markdown here)

# IMPORTANT NOTE: YOU CAN USE MARKDOWN FORMATTING
# IN THE DESCRIPTION AND ADDITIONAL NOTES.
# FOR MORE INFO ABOUT MARKDOWN FORMAT CHECK THIS
# https://www.markdownguide.org/basic-syntax/

# --- Your Code Starts Here ---

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
