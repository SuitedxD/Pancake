![ ](https://i.imgur.com/yYUG27J.png)
# Introduction to Pancake
Welcome! In this repository, you'll find everything about **Pancake: the next step in Discord bots**. We invite you to read the following article to learn more.

## How does Pancake work?
Pancake works through a **simple plugin system**. Plugins are an exclusive feature of Pancake that allow you to **load and execute packages of slash commands** in your Discord server. Once installed, these slash commands will be visible and usable only by you and the members of your server.

## Advantages of Pancake and its plugin system:
On paper, this might sound a bit complex or difficult to use, but in practice, **it's very easy and straightforward to understand**. Pancake isn't just made for programmers; it's designed **for all types of Discord users**: from those simply looking for fun commands, to those in need of solid moderation for their server, or even both at the same time! That's the advantage of Pancake: thanks to its plugin system, **you can turn it into any kind of bot your server needs**, all in one.

# Getting Started with Pancake
The first step is to [add Pancake to your Discord Server](https://discord.com/oauth2/authorize?client_id=1398868186216271962&permissions=8&integration_type=0&scope=applications.commands+bot). Once you have Pancake on your server, you can use the following commands:

## Pancake Default Commands
| Command(s) | Description        |
|-           |-                   |
| /install (plugin name) | Install a plugin from the plugin list. |
| /uninstall (plugin name) | Uninstall the plugin and its commands within. |
| /installed-list | See a list of the commands you have installed and the available spaces. |

- **IMPORTANT NOTE**: Only administrators can use these commands except for `/installed-list`.

To install a plugin, use `/install` followed by the name of the plugin you want to install, in the [Plugin List](docs/plugins-list.md) you will find all the plugins you can install and their **installation command**.

## Spaces and Uninstallation
Discord **only accepts up to 100 slash commands PER SERVER**. If you install large plugins and are about to reach the limit, we recommend uninstalling unnecessary or unused plugins. To do this, use `/uninstall` followed by the name of the plugin you want to remove to free up space.

- **IMPORTANT NOTE**: The plugin you uninstall will remove all slash commands associated with it.

- You can aslo use `/installed-list` to see the list of the plugins you have installed and the available spaces.

And it's that easy to install and manage your plugins!

# Best of all is:
**You can also create your own plugins** as long as they follow our **guidelines** and are made for the **benefit of our entire community**. We invite you to read our [Plugins Creation Guide](docs/plugins-guide.md) for more information about plugin creation.

***It's time to bring your ideas to life.***

# See Also:
- [Pancake Plugins List](docs/plugins-list.md)
- [Discord Server](https://discord.gg/SgXdeVaxuh)
- [Plugin Creation Guide](docs/plugins-guide.md)
- [Plugin Guidelines](/docs/plugins-guidelines.md)
- [Invite Pancake to your Discord Server](https://discord.com/oauth2/authorize?client_id=1398868186216271962&permissions=8&integration_type=0&scope=applications.commands+bot)