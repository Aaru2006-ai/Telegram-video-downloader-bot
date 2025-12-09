# 🎬 Advanced Telegram Video Downloader Bot

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org)
[![Telegram Bot API](https://img.shields.io/badge/Telegram-Bot%20API-blue)](https://core.telegram.org/bots/api)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> **Professional-grade Telegram bot for downloading videos from 100+ websites**

## 🌟 Features

### 🎥 Download Support
- ✅ **YouTube** - All qualities up to 1080p
- ✅ **Instagram** - Reels, Posts, Stories
- ✅ **TikTok** - Complete videos
- ✅ **Facebook** - Videos & Streams
- ✅ **Twitter/X** - Video downloads
- ✅ **And 100+ more websites!**

### ⚡ Advanced Features
- 🚀 **Multiple Quality Options** - 360p, 480p, 720p, 1080p
- 🎵 **Audio Extraction** - MP3 format support
- 📊 **User Analytics** - Track downloads & statistics
- 💾 **Download History** - User-specific tracking
- 📋 **Queue System** - Handle multiple downloads
- 🔐 **User Database** - Persistent data storage
- 📈 **Statistics Dashboard** - Bot usage analytics
- ⚙️ **Professional Logging** - Error tracking & monitoring
- 👑 **Premium Ready** - Future premium features
- 🎨 **Beautiful UI** - Professional inline keyboards

## 📋 Requirements

- Python 3.8+
- FFmpeg
- telegram-bot-api library
- yt-dlp

## 🚀 Quick Start

### Local Setup (Termux/Linux)

```bash
# 1. Clone the repository
git clone https://github.com/YourUsername/telegram-video-downloader-bot.git
cd telegram-video-downloader-bot

# 2. Install dependencies
pip install -r requirements.txt
pkg install ffmpeg  # For Termux users

# 3. Get your bot token
# Visit @BotFather on Telegram and create a new bot

# 4. Update bot token in bot.py
# Replace: TOKEN = "YOUR_TOKEN_HERE"

# 5. Get your Telegram ID
# Visit @userinfobot on Telegram

# 6. Update your ID in bot.py
# Replace: ADMIN_IDS = [YOUR_ID]

# 7. Run the bot
python bot.py
```

## 📱 Usage

### Send Video Link
Simply send any video link to the bot:
```
https://youtube.com/watch?v=...
https://instagram.com/p/...
https://tiktok.com/@user/video/...
```

### Select Quality
Choose from available quality options:
- 🔥 **Best** - 1080p Maximum Quality
- 📺 **HD** - 720p High Definition
- 📱 **480p** - Mobile Friendly
- 💻 **360p** - Low Bandwidth

### Download Audio
```
/audio [video_link]
```

## 🎮 Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot |
| `/help` | Get help guide |
| `/stats` | View your statistics |
| `/history` | Download history |
| `/settings` | Bot settings |
| `/premium` | Premium features info |
| `/support` | Contact support |

## 📦 Installation Guide

### Step 1: Install Python & FFmpeg

**Termux:**
```bash
pkg update
pkg install python ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip ffmpeg
```

**macOS:**
```bash
brew install python ffmpeg
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Bot

Edit `bot.py` and update:
```python
TOKEN = "your_bot_token_here"
ADMIN_IDS = [your_telegram_id]
```

### Step 4: Run

```bash
python bot.py
```

## 🗂️ Project Structure

```
telegram-video-downloader-bot/
├── bot.py                  # Main bot file
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore             # Git ignore file
├── LICENSE                # MIT License
├── database/              # Database storage
│   ├── users.json
│   ├── stats.json
│   └── queue.json
├── downloads/             # Downloaded videos
└── bot.log               # Bot logs
```

## 🌐 Deployment Options

### Option 1: Termux (Recommended for Testing)
- ✅ Easy setup
- ✅ No server needed
- ❌ Requires device to stay on

### Option 2: VPS (Production)
- ✅ 24/7 operation
- ✅ Better performance
- 💰 Requires paid server

**Popular VPS Providers:**
- Railway - ₹0 (free tier)
- Render - ₹0 (free tier)
- Heroku - Paid only now
- AWS - ₹50+/month
- DigitalOcean - ₹150+/month

### Option 3: Vercel (Serverless)
See [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)

## 📊 Database

Bot uses JSON-based database to store:
- **Users** - User profiles & download count
- **Stats** - Bot-wide statistics
- **Queue** - Pending downloads

Files are stored in `database/` directory.

## 🔒 Security

- Never share your bot token publicly
- Don't commit `.env` or tokens to git
- Use environment variables for sensitive data
- Regular backups of database

## 📝 Logging

All bot activities are logged to `bot.log`:
- Download history
- Errors and exceptions
- User interactions
- Performance metrics

## ⚠️ Rules & Limitations

### File Size Limits
- Maximum 5GB per download
- Maximum 100MB for instant telegram upload
- Larger files get download link instead

### Content Policy
- ✅ Personal use only
- ❌ No copyright content
- ❌ No piracy
- ✅ Respect creators

### Rate Limiting
- Max 100 downloads per hour per user
- Queue system prevents overload
- Fair usage for all users

## 🆘 Troubleshooting

### Bot Not Responding
```bash
# Check if bot is running
ps aux | grep python

# Check logs
tail -f bot.log

# Restart bot
python bot.py
```

### Download Fails
- Check internet connection
- Verify video link is correct
- Ensure ffmpeg is installed
- Check available disk space

### Token Issues
- Verify token from @BotFather
- Ensure correct format
- Check no extra spaces

### Permission Errors
```bash
chmod +x bot.py
python bot.py
```

## 📈 Statistics

Track your usage:
```bash
/stats  # View personal statistics
```

Bot shows:
- Total downloads
- Data downloaded
- Last download time
- Account type (Free/Premium)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Advanced Bot Developer**
- GitHub: [@YourUsername](https://github.com/YourUsername)
- Telegram: [@YourUsername](https://t.me/YourUsername)

## 🙏 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/)

## 📮 Support

Having issues? Contact me:
- 📧 Email: aayuroy12260504gmail.com
- 💬 Telegram: @Nxt_og
- 🐛 GitHub Issues: [Create Issue](https://github.com/YourUsername/telegram-video-downloader-bot/issues)

## 📚 Documentation

- [Getting Started](docs/GETTING_STARTED.md)
- [API Reference](docs/API.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## ⭐ Show Your Support

If this project helped you, please consider giving it a star! ⭐

```
https://github.com/YourUsername/telegram-video-downloader-bot
```

---

<div align="center">

**[⬆ Back to Top](#-advanced-telegram-video-downloader-bot)**

Made with ❤️ by Advanced Bot Developer

</div>
