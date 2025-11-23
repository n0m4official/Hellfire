# Hellfire — Precision Server Management Bot

Hellfire is a fast, multi-server capable Discord bot built for **precision cleanup, automated moderation, and utility features**.  
Originally designed as a server-cleaner prototype, Hellfire evolved into a modular, extensible bot with powerful tools and full slash-command support.

---

## ✨ Core Features

### 🧹 **Cleanup & Moderation**
- `/purgenoroles` — remove users without a Member role  
- `/purgeinactive` — remove users inactive for X days  
- **Scheduled auto-clean** (optional per server)  
- High-speed purge logic built for large servers

### 🛡️ **Anti-Raid Detection**
- Flags rapid join spikes  
- Alerts admins in the configured channel  
- Lightweight and automatic

### 👋 **Welcome System**
- Configurable welcome channel  
- Sends greetings to new members  
- Fully optional per server

### 📡 **Status Announcements**
Hellfire can now announce:
- **Startup**
- **Shutdown**
- **Restart**

…in a **per-server configurable channel** via `/setstatuschannel`.

### 🎌 **Anime & Manga Tools**
Powered by AniList + Jikan:
- `/anime` — search anime titles/genres  
- `/manga` — search manga titles/genres  
- `/character` — search anime characters  
- `/trending` — MAL top trending  
- Multi-page result navigation

### 🛠️ **Owner Utilities**
- `/test` — ping the bot  
- `/reload` — reload all cogs  
- `/restart` — restart bot  
- `/shutdown` — shut down bot  

### 📋 **General Commands**
- `/help` — list all commands  
- `/inspire` — inspirational quote from ZenQuotes  

---

## ⚙️ Per-Server Configuration

Hellfire stores **only server-level settings**, never user data.

Stored values:
- `member_role_id`
- `inactive_days`
- `auto_clean_enabled`
- `welcome_channel_id`
- `status_channel_id` ← NEW

Set these with:
- `/setmemberrole`
- `/setwelcome`
- `/setstatuschannel`

Everything is cleanly stored in `hellfire.db`.

---

## 🚀 Setup

### 1. Install dependencies
```bash
pip install nextcord python-dotenv aiohttp
```
2. Create a .env file
```bash
DISCORD_TOKEN=[KEPT_SECRET_FOR_OBVIOUS_REASONS]
BOT_OWNER_ID=[MY_ACCOUNT_ID]
```
(Optional) If you want a default status channel for development:
```bash
CHANNEL_ID=YOUR_CHANNEL_ID
```
3. Run Hellfire
```bash
python main.py
```

## 💾 Database
Hellfire uses SQLite for:
- role configuration
- welcome/status channels
- inactive-day settings

Automatic migrations ensure new fields (like status_channel_id) are added safely.

## 🔒 Privacy & Safety
Hellfire:
- stores no personal user data
- performs only admin-approved actions
- only saves minimal server metadata
- follows Discord ToS and developer guidelines

See:
`PRIVACY_POLICY.md`
`TERMS_OF_SERVICE.md`

## 🏷️ License
MIT License (or your choice).

## ❤️ Acknowledgements
Built with:
- Nextcord
- AniList API
- Jikan API
- ZenQuotes API
- SQLite
- And a lot of perseverance, debugging, and caffeine.
