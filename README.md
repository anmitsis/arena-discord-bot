# 🎮 Arena Damage Bot (Discord + Riot API)

A Discord bot that tracks Arena-only damage statistics for League of Legends players using the Riot Games API.

It provides:

- 📊 Damage leaderboards (average & total)

- 📈 Damage graphs

- 📋 Damage tables

Arena-only filtering (queueId = 1700)

## 📸 Example Commands
!helpme

!damage 10

!damage_total 15

!damage_graph 5

!damage_table 8

## 🧩 Requirements

Python 3.10+

A Discord account

A Riot Games account

## Git

🚀 Getting Started (Local Setup)
## 1️⃣ Clone the repository
git clone https://github.com/YOUR_USERNAME/arena-damage-bot.git

cd arena-damage-bot

## 2️⃣ Create a Discord Bot

Go to 👉 https://discord.com/developers/applications

Click New Application

Go to Bot

Click Add Bot

Copy the Bot Token

Enable Message Content Intent

## 3️⃣ Get a Riot API Key

Go to 👉 https://developer.riotgames.com

Log in

Copy your Development API Key

**⚠️ Development keys expire every 24 hours.**

## 4️⃣ Create a .env file

In the project root, create a file named .env:

DISCORD_TOKEN=your_discord_bot_token_here

RIOT_API_KEY=your_riot_api_key_here

## 5️⃣ Install dependencies
pip install -r requirements.txt

## 6️⃣ Run the bot
python damage_bot.py


If successful, you’ll see:

Damage bot online ✅

## 7️⃣ Invite the bot to your Discord server

In the Discord Developer Portal:

Go to OAuth2 → URL Generator

Select scope: bot

Permissions:

- Read Messages

- Send Messages

- Embed Links

- Attach Files

Open the generated URL and invite the bot

## 8️⃣ Use the bot in Discord

### 📊 Commands Overview
#### 🔥 Leaderboards

Command	Description

!damage [games]	Average Arena damage

!damage_total [games]	Total Arena damage

#### 📈 Visuals

Command	Description

!damage_graph [games]	Bar graph of average damage

#### 📋 Tables

Command	Description

!damage_table [games]	Text-based damage table

#### Notes

[games] is optional (default = 10)

Only Arena games are counted

Results are ranked highest → lowest


## 5️⃣ Verify logs

You should see:

Damage bot online ✅


## 🧠 Architecture Notes

Riot API calls run in background threads (asyncio.to_thread)

Arena filtering is applied using queueId == 1700


## 🛠️ Tech Stack

Python

discord.py

Riot Games API (Match-V5)

matplotlib

Railway (deployment)

python-dotenv

## 📜 License

MIT — feel free to fork, modify, and build on this.
