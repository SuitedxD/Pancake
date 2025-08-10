# Plugin Guidelines
Welcome! In this section, you will find everything you need to know to ensure a successful integration of your plugin into Pancake with some frecuently asked questions.

## Requirements and Prohibitions for Submitting Plugins
To maintain the quality and security of Pancake, we ask all developers to follow these basic rules:

- **Provide a clear explanation of your plugin.**  
  Explain what your plugin does, how it works, and include usage examples. Vague, confusing, or missing explanations will result in rejection. It doesn’t have to be long — clarity is what matters. This explanation can be included as comments in the code.

- **Always specify a category.**  
  This is mandatory. If your plugin does not have a clearly specified category (such as "Fun", "Moderation", "Utility", etc. You can see all the categories below.), it will be postponed or rejected. Categories help us classify and organize plugins for users and ensure compatibility within Pancake's system.

- **Your code must be readable, organized, and compatible.**  
  Submissions must be clean, error-free, and fully compatible with Pancake's system. Poorly written or buggy code will be rejected.

- **External libraries are not allowed.**  
  For security reasons, only the libraries already included in Pancake’s core are permitted. Do not import or rely on external dependencies.

- **Access to system files or use of dangerous functions is strictly prohibited.**  
  Functions and modules such as:
  `os`, `open()`, `eval`, `exec`, `subprocess`, `requests`, and similar are **not** allowed under any circumstances.

- **Avoid using generic or already existing names.**  
  Do not name your plugin or classes using common or placeholder names such as `MyPlugin`, `Plugin1`, etc. Make sure your names are unique and not already used by existing plugins.

**Note: Submitting malicious code or any form of scam will result in immediate penalties.**

## Penalties for Non-Compliance with the Guidelines
The following penalties may be applied if a submission violates one or more of the guidelines. They are listed from the least to the most severe:

1. **Plugin Postponed**  
   This applies when we detect bugs, compatibility issues, or other minor problems. Your plugin is not discarded but temporarily postponed until the issues are resolved. We will inform you of the reasons and assist you in addressing them if needed.

2. **Plugin Rejected**  
   The plugin does not meet the minimum requirements and is rejected from integration. You will be notified along with the reason. Once corrected, you may submit it again for review.

3. **Blacklisted**  
   If suspicious or potentially harmful behavior is detected, you will be blacklisted. This means you will be unable to submit code or access certain Pancake-related services until the issue is resolved and trust is restored.

4. **Permanent Ban**  
   In cases of severe violations — such as proven malicious intent — you will be permanently banned from the Pancake Discord server and denied access to all Pancake services. This action is final and non-negotiable.


## Plugin Categories
Categories are mandatory for plugins. These are all currently available; you can use more than one or "other" if none of these accurately describe your plugin:
- Fun
- Moderation
- Utility
- Media
- Social
- Info
- Tools
- Loggin
- Security
- Only-Admin
- Permissions
- Levels
- Roles
- Messages
- Experimental
- Other

## FAQ
- ***How long does it take for my plugin to be reviewed or integrated?***
It depends on the volume of submissions and the complexity of your plugin. On average, reviews take between **2 to 5 days**, but it could be longer during high activity. We'll notify you once your plugin has been reviewed.

- ***How will I know if my plugin was accepted or rejected?***
You will receive a message from the Pancake team through Discord with the **status** of your plugin (accepted, postponed, or rejected), along with feedback if necessary.

- ***What happens if my plugin is postponed?***
This usually means your plugin has minor issues, such as bugs, missing information, or compatibility concerns. You can fix them and **resubmit** your plugin anytime.

- ***Can I submit the same plugin again if it was rejected?***
Yes, but **only after fixing the issues** that caused the rejection. Submitting the same plugin without changes may lead to a warning or blacklist.

- ***Can I use external libraries or APIs in my plugin?***
**No.** For security and compatibility reasons, only the libraries that are already part of Pancake are allowed. External libraries, HTTP requests, or system access are strictly forbidden.

- ***What kind of plugins are accepted?***
We accept all kinds of **safe, useful, and creative** plugins. From moderation tools to fun commands, as long as they follow our guidelines.

- ***Is there a limit to how many plugins I can submit?***
There's no hard limit, but spamming low-quality or repeated submissions can cause you to be blacklisted.

- ***Can I make updates to my plugin after it's accepted?***
Yes! You can submit an **updated version** at any time in your original **#send-your-plugin** Discord forum. Just make sure to clearly explain the changes made so we can review them efficiently.

- ***Will I get credit for my plugin?***
Absolutely. Each plugin will include a visible **author** or credit within Pancake's system. Your contribution will be acknowledged.

- ***What should I do if I find a bug in someone else's plugin?***
Let us know immediately on the Discord server in **#plugins-forum**. We’ll verify it and either **patch** it or **postpone/remove** the plugin if necessary.

If you haven't found your question or concern here, feel free to reach out via our official Discord server. You can find the invitation below.

# See Also:
- [Plugins Guide](/docs/plugins-guide.md)
- [Plugin Template](/plugins/community/example.py)
- [Discord Server](https://discord.gg/dT8S632nPM)
- [Pancake Plugins List](/docs/plugins-list.md)
- [Invite Pancake to your Discord Server](https://discord.com/oauth2/authorize?client_id=1398868186216271962&permissions=8&integration_type=0&scope=applications.commands+bot)