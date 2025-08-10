# Plugin Creation Guide
Welcome! Here you'll find everything you need to understand how to create, submit, and maintain your own plugin for Pancake. This guide is designed for both programmers and regular users, so everything will be clearly explained, with as much technical detail as necessary, but always focused on clarity and simplicity.

The plugins system is intended to allow the community to contribute custom features while maintaining quality, stability, and security in Pancake.

## What is a Plugin?
A **plugin** is a self-contained module that includes one or more slash commands. It is written in Python and structured to be dynamically installed per server.

It is not just a single command or a piece of code—it is the **complete installable unit** that contains the commands and logic for Pancake to load, install, uninstall, and execute within a Discord server.

In our system, we define:

- **Plugin** → The final installable package made of one or more commands.
- **Code** → The Python file(s) you submit.
- **Command** → The specific slash command(s) your plugin provides.

You don’t need to create multiple files. Each plugin should be written in a single Python file.

## How the Submission System Works
Submitting a plugin is simple. All plugin submissions are made inside our official Discord server using the forum channel named **#send-your-plugin**.

Here's how the process works:

- **IMPORTANT NOTE**: Before submitting we recommend to visit and read our [Plugin Guidelines](/docs/plugins-guidelines.md)

1. **[Join the Pancake Discord server](https://discord.gg/dT8S632nPM).**
2. **Go to #send-your-plugin.**
3. **Create a new forum post.** This is your plugin submission.
4. **Paste a link to your plugin's code** using [GitHub Gist](https://gist.github.com). This is the only format we currently accept.
5. **Include a clear explanation** of what your plugin does, what commands it includes, and how users are expected to use it.
6. **Specify the category** your plugin belongs to ("Fun", "Moderation, "Tools", etc. You can find the list [cliking here](/docs/plugins-guidelines.md#plugin-categories)).
7. Our team will **review** your submission. If everything is in order, we'll integrate it into the plugin system. If not, we’ll contact you for fixes or clarifications.

## Why Guidelines Matter
It is extremely important that your plugin follows the official guidelines. This is not optional.

We are building a stable and secure bot used by many users across different servers. Any plugin that doesn't follow our rules can potentially break functionality or pose a security risk.

Following the rules ensures:
- Your plugin is reviewed faster.
- It can be safely installed in any server.
- It works properly with Pancake’s core system.

Any plugin that fails to comply will be postponed, rejected, or permanently banned from the system depending on the severity of the violation.

**You can read all the Plugin Guidelines [cliking here](/docs/plugins-guidelines.md)**

## Writing a Plugin
Pancake uses **Python** as its programming language. That means all your code must be written in Python, using the `discord.py` library and the same structure we use internally.

**[Click here](/plugins/community/example.py) to see a template to get you started.**

## Finally
You can always join our Discord server and find more help or guidance on this process in our #plugin-forum. Finally, have fun!

# See Also:
- [Plugin Guidelines](/docs/plugins-guidelines.md)
- [Plugin Template](/plugins/community/example.py)
- [Discord Server](https://discord.gg/dT8S632nPM)
- [Pancake Plugins List](/docs/plugins-list.md)
- [Invite Pancake to your Discord Server](https://discord.com/oauth2/authorize?client_id=1398868186216271962&permissions=8&integration_type=0&scope=applications.commands+bot)