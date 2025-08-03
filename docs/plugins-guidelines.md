# Plugin Guidelines
Welcome! In this section you will find everything you need to know to ensure a successful integration of your plugin in Pancake.

## Requirements and prohibitions for submitting plugins:

- 1. Always explain clearly how your plugin works.
What it does, how it does it, usage examples, etc. A vague, confusing, or non-existent explanation will cause your plugin to be rejected, so be clear. We don't care if it's a long or short explanation, as long as you clearly describe how it works. You can include this clearly explanation in code comments.

- 2. Your code must be readable, organized, and compatible. 
Make sure your code is clean and error-free. A code disorganized, buggy, or incompatible with Pancake will be rejected.

- 3. No external libraries allowed.
For security reasons, we do not allow libraries not included in Pancake's codebase.

- 4. Access to system files or use of dangerous functions is prohibited.
For security reasons, functions such as:
`os, open(), eval, exec, subprocess, requests, etc.` are not allowed.

- 5. Do not use generic or already used names.
Avoid using generic names like "MyPlugin" or "command-1" in classes or in the name of your plugin itself. Make sure your class and command names aren't already taken or used in other plugins.

Note: Any malicious code or attempted scam will be penalized.

## Penalties for non-compliance with the Guidelines
The penalties can vary in intensity but here they are ordered from lowest to highest penalty.

- **Plugin Postponed**: This may be caused because we find one or more errors, bugs, or a simple incompatibility error. In any case, your plugin won't be discarded, but it will be postponed from being integrated into Pancake. We'll let you know, and depending on the reason, we'll see what the best way to resolve it is.

- **Plugin Rejected**: Your plugin is rejected for Pancake integration, meaning that unless you attempt to submit it later, it won't be integrated. We'll let you know, along with the reason for the rejection. You can resubmit it once you've made all the necessary corrections.

- **Blacklisted**: In case of suspicious activity, you will be blacklisted, which means you won't be able to submit code or access to certain Pancake services unless we confirm you're not engaging in malicious activity.

- **Closing of doors**: As the name suggests, you will be banned from the Discord server and will not be able to access or use Pancake services again.

If you have any questions, please let us know on our Discord server.

