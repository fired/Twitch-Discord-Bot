# Discord.py Twitch Bot

This is a Twitch bot built using discord.py, a Python library for creating Discord bots. The bot monitors the status of a Twitch streamer and sends notifications to a specified Discord channel when the streamer goes live or offline. Additionally, it provides several other utility commands for managing channels, sending messages, and more.

## Prerequisites

Before setting up the bot, you need to have the following:

- Python (version 3.8 or higher)
- Discord Bot Token (obtainable from the Discord Developer Portal)
- Twitch Client ID and Client Secret (obtainable from the Twitch Developer Dashboard)
- Twitch Username of the streamer you want to monitor
- Discord Channel ID where the bot will send notifications

## Installation

1. Clone or download the repository to your local machine.
2. Navigate to the project directory:

   ```bash
   cd discord-twitch-bot
   ```
3. Install the required dependencies using pip:
    
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
1. Open the bot.py file in a text editor.
2. Replace the placeholders with your own values:
    ```python
    DISCORD_BOT_TOKEN = 'your-discord-bot-token'
    TWITCH_CLIENT_ID = 'your-twitch-client-id'
    TWITCH_CLIENT_SECRET = 'your-twitch-client-secret'
    TWITCH_USERNAME = 'twitch-username'
    CHANNEL_ID = 123456789012345678  # Replace with your Discord channel ID
    ```

## Usage
1. Run the bot using the following command:
    ```bash
    python bot.py
    ```
    The bot will log in to Discord and start monitoring the Twitch streamer.
2. Invite the bot to your Discord server using the OAuth2 URL generated from the [Discord Developer Portal](https://discord.com/developers/applications).
3. Set up the necessary permissions for the bot in the Discord server to ensure it can perform the desired actions.

## Available Commands
- Send Message
    - Sends a custom message to the specified channel.
    - Command: .send_message <channel_id> MESSAGE
    - Example: .send_message 123456789012345678 Hello, world!
- Send Embed Message
    - Sends a custom embed message to the specified channel.
    - Command: .sendme <channel_id> "<title>" HEX MESSAGE
    - Example: .sendme 123456789012345678 "Important Announcement" ff0000 This is an important announcement!
- List Channels
    - Lists all text channels and their IDs in the server.
    - Command: .listc
- List Colors
    - Displays a list of colors along with their hexadecimal values.
    - Command: .list_colors
- Purge Messages
    - Deletes the specified number of messages in the current channel.
    - Command: .purge AMOUNT
    - Example: .purge 10
- Toggle Channel Privacy
    - Makes the specified channel private or public.
    - Command: .tp #channel-name
    - Example: .tp #general
- Help
    - Displays the list of available commands with their descriptions.
    - Command: .help

## To Add
- Mute
- Ban
- Unban
- Timeout

## License
   [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
   
   This project is licensed under the GNU General Public License v3.0. See the [LICENSE](https://github.com/kuc/Twitch-Discord-Bot/blob/main/LICENSE) file for details.
