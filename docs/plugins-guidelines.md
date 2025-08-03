# Plugin Guidelines
Before submitting your plugin, make sure to comply with the following guidelines. In case of non-compliance, your plugin can be postponed or rejected.

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

If you have any questions, please let us know on our Discord server before submitting.