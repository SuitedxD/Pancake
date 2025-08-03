# Plugin Guidelines

Welcome! In this section, you will find everything you need to know to ensure a successful integration of your plugin into Pancake.

## Requirements and Prohibitions for Submitting Plugins

To maintain the quality and security of Pancake, we ask all developers to follow these basic rules:

- **Provide a clear explanation of your plugin.**  
  Explain what your plugin does, how it works, and include usage examples. Vague, confusing, or missing explanations will result in rejection. It doesn’t have to be long — clarity is what matters. This explanation can be included as comments in the code.

- **Always specify a category.**  
  This is mandatory. If your plugin does not have a clearly specified category (such as "Fun", "Moderation", "Utility", etc.), it will be postponed or rejected. Categories help us classify and organize plugins for users and ensure compatibility within Pancake's system.

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

# FAQ

If you have any questions or concerns, feel free to reach out via our official Discord server.
