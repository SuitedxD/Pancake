# List of Pancake Plugins
Here you'll find all the plugins you can install in Pancake. Click on any of the following categories to see related

[Moderation](/docs/plugins-list.md/#Moderation) | [Fun](/docs/plugins-list.md/#Fun) | [Utility](/docs/plugins-list.md/#Utility)

# Utility

## **Welcome** - Suited
**Commands: 7**

**Install with:** `/install plugin:welcome`

- Give your new members a warm welcome with this plugin.

| Command(s) | Description        |
|-           |-                   |
| /set-welcome-channel (#channel) | Set the channel where welcome messages will be sent. |
| /set-welcome-background (Image URL) | Set the background image URL for the welcome message. |
| /set-welcome-avatar-size (50-1024) | Set the size of the avatar in the welcome image. |
| /set-welcome-avatar-position (1, 2, 3) | Set the avatar position on the welcome image. |
| /set-welcome-text (Example: Hello {user}, welcome to {server_name}!)| Set the welcome text for the embed title. |
| /set-welcome-embed-color (colors below)| Set the embed color for the welcome message. |
| /welcome-fire | Test the welcome message by sending it to the configured channel. |

- Embed Colors: `default, dark_theme, red, blue, green, purple, orange, gold`.

## **Ping** - Suited
**Commands: 2**

**Install with:** `/install plugin:ping`

- Basic ping commands for testing.

| Command(s) | Description        |
|-           |-                   |
| /ping      | Returns with pong. |
| /ping-ms   | Returns bot latency in ms. |


# Fun

## **Fun Commands Pack No. 1** - Suited
**Commands: 7**

**Install with:** `/install plugin:fun1`

- 7 basic and fun commands for your server.

| Command(s) | Description        |
|-           |-                   |
| /8ball (question) | Answers a yes/no question. |
| /coinflip  | Flips a coin and tells you the result. |
| /dare      | Dares you to do something dumb. |
| /dice      | Rolls a dice and tells you the result. |
| /howgay    | Checks your gay percentage. |
| /mood      | Detects your mood. |
| /random-number | Gives you a random number. |

# Moderation

## **Moderation Commands Pack No. 1** - Suited
**Commands: 9**

**Install with:** `/install plugin:mod1`

- 9 basic moderation commands.

| Command(s) | Description        |
|-           |-                   |
| /ban (user) (reason) | Ban a user off your server. |
| /unban (user ID) | Unban a user from your server by ID. |
| /kick (user) (reason) | Kicks a user off your server. |
| /mute (user) (duration) (reason) | Mute a user for a specific duration (format: 10m, 1h, 30s). |
| /unmute (user) | Remove mute from a user. |
| /clear (amount) | Delete a number of messages from the current channel (1-100). |
| /slowmode (delay) | Set slowmode delay (seconds) in the current channel. 0 disables slowmode. |
| /lock (role) | Lock the current channel for a specific role. |
| /unlock (role) | Unlock the current channel for a specific role. |

## **Strike Commands** - Suited
**Commands: 5**

**Install with:** `/install plugin:strike`

- Introducing Strikes, Pancake's exclusive warning system.

| Command(s) | Description        |
|-           |-                   |
| /strike (user) (reason) | Give a strike to a user. Strikes accumulate per user. |
| /remove-strike (user) (amount) | Removes a certain amount of strikes from a user. |
| /check-strikes (user)| Check the number of strikes a user has. |
| /strike-settings | View your current settings. |
| /strike-limit-settings (limit of strikes), (action: mute, kick, ban) | Configure the strike limit and what actions Pancake will take when it is reached. |

# See Also:
- [Plugins Guide](/docs/plugins-guide.md)
- [Plugin Template](/plugins/community/example.py)
- [Discord Server](https://discord.gg/SgXdeVaxuh)
- [Invite Pancake to your Discord Server](https://discord.com/oauth2/authorize?client_id=1398868186216271962&permissions=8&integration_type=0&scope=applications.commands+bot)
- [Plugin Guidelines](/docs/plugins-guidelines.md)