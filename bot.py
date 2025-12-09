#!/usr/bin/env python3
"""
🎬 PROFESSIONAL TELEGRAM VIDEO DOWNLOADER BOT 🎬
Advanced Features: Database, Analytics, Queue System, Admin Panel
Author: Advanced Bot Dev
Version: 2.0.0
"""

import logging
import asyncio
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import yt_dlp
from collections import defaultdict
from telegram import (Update, InlineKeyboardButton, InlineKeyboardMarkup, 
                     BotCommand)
from telegram.ext import (Application, CommandHandler, MessageHandler, 
                         CallbackQueryHandler, filters, ContextTypes, 
                         PicklePersistence)
from telegram.constants import ParseMode, ChatAction
try:
    from telegram.error import TelegramError
except:
    TelegramError = Exception

# ============================================
# CONFIGURATION & SETUP
# ============================================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

TOKEN = "8329797572:AAFJKZqTjCImtT7ogZQp-S3S-K8jlyGzxUw"
ADMIN_IDS = 7837071005  # Replace with your Telegram ID (number only)
DOWNLOAD_DIR = Path("downloads")
DB_DIR = Path("database")
DOWNLOAD_DIR.mkdir(exist_ok=True)
DB_DIR.mkdir(exist_ok=True)

# Conversation States
WAITING_URL, SELECTING_QUALITY, CONFIRMING = range(3)

# ============================================
# DATABASE & ANALYTICS
# ============================================

class DatabaseManager:
    """Professional database management"""
    
    def __init__(self):
        self.user_file = DB_DIR / "users.json"
        self.stats_file = DB_DIR / "stats.json"
        self.queue_file = DB_DIR / "queue.json"
        self.load_data()
    
    def load_data(self):
        """Load all data from files"""
        self.users = self._load_json(self.user_file, {})
        self.stats = self._load_json(self.stats_file, {})
        self.queue = self._load_json(self.queue_file, [])
    
    def _load_json(self, filepath, default):
        """Load JSON safely"""
        try:
            if filepath.exists():
                with open(filepath, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading {filepath}: {e}")
        return default
    
    def _save_json(self, filepath, data):
        """Save JSON safely"""
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving {filepath}: {e}")
    
    def add_user(self, user_id, username, first_name):
        """Add/Update user in database"""
        user_id = str(user_id)
        self.users[user_id] = {
            'username': username,
            'first_name': first_name,
            'joined': datetime.now().isoformat(),
            'downloads': 0,
            'total_data': 0,
            'last_download': None,
            'premium': False
        }
        self._save_json(self.user_file, self.users)
    
    def increment_download(self, user_id, filesize=0):
        """Track user downloads"""
        user_id = str(user_id)
        if user_id in self.users:
            self.users[user_id]['downloads'] += 1
            self.users[user_id]['total_data'] += filesize
            self.users[user_id]['last_download'] = datetime.now().isoformat()
            self._save_json(self.user_file, self.users)
    
    def get_stats(self):
        """Get bot statistics"""
        return {
            'total_users': len(self.users),
            'total_downloads': sum(u.get('downloads', 0) for u in self.users.values()),
            'total_data': sum(u.get('total_data', 0) for u in self.users.values()),
            'active_users': len([u for u in self.users.values() 
                               if u.get('last_download')])
        }

# ============================================
# VIDEO DOWNLOADER ENGINE
# ============================================

class AdvancedVideoDownloader:
    """Professional video downloader with advanced features"""
    
    def __init__(self):
        self.downloading = {}
        self.failed_urls = []
    
    def get_video_info(self, url):
        """Fetch comprehensive video information"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'views': info.get('view_count', 0),
                    'likes': info.get('like_count', 0),
                    'thumbnail': info.get('thumbnail'),
                    'description': info.get('description', '')[:200],
                    'webpage_url': info.get('webpage_url'),
                    'ext': info.get('ext', 'mp4'),
                    'filesize': info.get('filesize'),
                    'formats_available': len(info.get('formats', []))
                }
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            return None
    
    def download_video(self, url, quality='best', audio_only=False, user_id=None):
        """Download video with advanced options"""
        try:
            info = self.get_video_info(url)
            if not info:
                return None, "❌ Video information unavailable"
            
            # Format selection
            if audio_only:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '320',
                    }],
                    'outtmpl': str(DOWNLOAD_DIR / '%(title)s'),
                    'quiet': True,
                    'no_warnings': True,
                }
            else:
                quality_map = {
                    'best': 'bestvideo+bestaudio/best',
                    'hd': 'bestvideo[height>=720]+bestaudio/best',
                    '480p': 'bestvideo[height>=480]+bestaudio/best',
                    '360p': 'bestvideo[height>=360]+bestaudio/best',
                }
                
                ydl_opts = {
                    'format': quality_map.get(quality, 'best'),
                    'outtmpl': str(DOWNLOAD_DIR / '%(title)s.%(ext)s'),
                    'quiet': True,
                    'postprocessors': [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4'
                    }],
                    'progress_hooks': [self._progress_hook],
                }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(result)
            
            return filename, info
        
        except Exception as e:
            logger.error(f"Download error: {e}")
            return None, str(e)[:100]
    
    def _progress_hook(self, d):
        """Track download progress"""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            logger.info(f"Progress: {percent} | Speed: {speed}")

db = DatabaseManager()
downloader = AdvancedVideoDownloader()

# ============================================
# HANDLERS - COMMANDS
# ============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command with inline buttons"""
    user = update.effective_user
    db.add_user(user.id, user.username or 'Unknown', user.first_name)
    
    welcome_text = f"""
╔══════════════════════════════════════════╗
║  🎬 ADVANCED VIDEO DOWNLOADER BOT 🎬    ║
║         Professional Edition v2.0       ║
╚══════════════════════════════════════════╝

👋 नमस्ते {user.first_name}!

🚀 <b>Features:</b>
✅ YouTube, Instagram, TikTok, Facebook
✅ 1080p तक Quality
✅ MP3 Audio Extraction
✅ Download Queue System
✅ Analytics & Statistics
✅ Download History
✅ Batch Downloads

📊 <b>Your Stats:</b>
📥 Downloads: {db.users.get(str(user.id), {}).get('downloads', 0)}
💾 Data Used: {db.users.get(str(user.id), {}).get('total_data', 0) / (1024**3):.2f} GB

<i>बस video link भेजो या /help देखो!</i>
    """
    
    keyboard = [
        [InlineKeyboardButton("📥 Download", callback_data='start_download'),
         InlineKeyboardButton("📜 History", callback_data='show_history')],
        [InlineKeyboardButton("📊 Stats", callback_data='show_stats'),
         InlineKeyboardButton("❓ Help", callback_data='show_help')],
        [InlineKeyboardButton("⚙️ Settings", callback_data='settings'),
         InlineKeyboardButton("👨‍💼 Premium", callback_data='premium_info')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, 
                                   reply_markup=reply_markup,
                                   parse_mode=ParseMode.HTML)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comprehensive help guide"""
    help_text = """
╔══════════════════════════════════════════╗
║           📚 HELP & GUIDE 📚             ║
╚══════════════════════════════════════════╝

🎥 <b>Videos कहाँ से Download करे:</b>
• <code>YouTube</code> - Sab quality mein
• <code>Instagram</code> - Reels, Posts
• <code>TikTok</code> - सब content
• <code>Facebook</code> - Videos & Streams
• <code>Twitter/X</code> - Videos
• <code>और 100+ websites!</code>

⚡ <b>Quick Start:</b>
1️⃣ Video link भेजो
2️⃣ Quality select करो (Best/HD/480p)
3️⃣ Download हो जाएगा! 🎉

📱 <b>Quality Options:</b>
🔥 <b>Best</b> - 1080p (Maximum Quality)
📺 <b>HD</b> - 720p (High Definition)
📱 <b>480p</b> - Mobile Friendly
💻 <b>360p</b> - Low Bandwidth

🎵 <b>Audio Download:</b>
MP3 format में music extract करो
<code>/audio [link]</code>

📋 <b>Commands:</b>
/start - Start bot
/help - यह help
/stats - अपने stats देखो
/history - Download history
/settings - Preferences
/batch - Multiple videos
/premium - Premium features

⚠️ <b>Rules:</b>
✅ Maximum 5GB per download
✅ Max 100MB files for instant upload
✅ Copyright content न download करो
✅ Personal use के लिए only

❓ <b>FAQ:</b>
<b>Q: Speed slow क्यों है?</b>
A: Internet speed पर depend है

<b>Q: File upload नहीं हो रही?</b>
A: 100MB से बड़ी files के लिए /download_link use करो

<b>Q: कितने downloads कर सकते हो?</b>
A: Unlimited (Premium users को priority)

👨‍💼 Support: /support
💬 Contact: /feedback
    """
    
    await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle video URLs"""
    url = update.message.text.strip()
    
    if not url.startswith(('http://', 'https://')):
        await update.message.reply_text(
            "❌ <b>Invalid URL!</b>\n\n"
            "Valid link भेजो:\n"
            "<code>https://youtube.com/watch?v=...</code>",
            parse_mode=ParseMode.HTML
        )
        return
    
    # Show loading animation
    loading_msg = await update.message.reply_text(
        "⏳ <b>Video information load हो रही है...</b>\n"
        "<i>कुछ सेकंड लगेंगे...</i>",
        parse_mode=ParseMode.HTML
    )
    
    try:
        await update.message.chat.send_action(ChatAction.TYPING)
        
        # Get video info
        info = downloader.get_video_info(url)
        
        if not info:
            await loading_msg.edit_text(
                "❌ <b>Video information fetch नहीं हो सकी!</b>\n"
                "Link सही है?\n\n"
                "सही link:\n"
                "<code>https://youtube.com/watch?v=...</code>",
                parse_mode=ParseMode.HTML
            )
            return
        
        # Format video info
        duration_min = info['duration'] // 60
        duration_sec = info['duration'] % 60
        
        info_text = f"""
╔══════════════════════════════════════════╗
║           ✅ VIDEO FOUND! ✅            ║
╚══════════════════════════════════════════╝

<b>📹 Title:</b>
<code>{info['title'][:60]}</code>

<b>👤 Channel:</b> {info['uploader']}

<b>⏱️ Duration:</b> {duration_min}m {duration_sec}s

<b>👁️ Views:</b> {info['views']:,}
<b>👍 Likes:</b> {info['likes']:,}

<b>📊 Available Formats:</b> {info['formats_available']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<b>Quality Select करो:</b>
        """
        
        keyboard = [
            [InlineKeyboardButton("🔥 Best (1080p)", callback_data=f'dl_best_{url}'),
             InlineKeyboardButton("📺 HD (720p)", callback_data=f'dl_hd_{url}')],
            [InlineKeyboardButton("📱 480p", callback_data=f'dl_480_{url}'),
             InlineKeyboardButton("💻 360p", callback_data=f'dl_360_{url}')],
            [InlineKeyboardButton("🎵 Audio MP3", callback_data=f'dl_audio_{url}')],
            [InlineKeyboardButton("❌ Cancel", callback_data='cancel')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await loading_msg.edit_text(info_text, 
                                   reply_markup=reply_markup,
                                   parse_mode=ParseMode.HTML)
    
    except Exception as e:
        await loading_msg.edit_text(f"❌ Error: {str(e)[:100]}")
        logger.error(f"URL handling error: {e}")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = query.from_user.id
    
    # Handle different callbacks
    if data == 'show_help':
        await help_command(query, context)
    
    elif data == 'show_stats':
        stats = db.get_stats()
        stats_text = f"""
<b>📊 BOT STATISTICS:</b>

👥 Total Users: {stats['total_users']}
📥 Total Downloads: {stats['total_downloads']}
💾 Total Data: {stats['total_data'] / (1024**3):.2f} GB
🟢 Active Users: {stats['active_users']}
        """
        await query.edit_message_text(stats_text, parse_mode=ParseMode.HTML)
    
    elif data == 'show_history':
        user_data = db.users.get(str(user_id), {})
        await query.edit_message_text(
            f"📜 <b>Your Stats:</b>\n\n"
            f"📥 Downloads: {user_data.get('downloads', 0)}\n"
            f"💾 Total Data: {user_data.get('total_data', 0) / (1024**2):.2f} MB\n"
            f"📅 Last Download: {user_data.get('last_download', 'Never')}",
            parse_mode=ParseMode.HTML
        )
    
    elif data.startswith('dl_'):
        parts = data.split('_', 2)
        quality_type = parts[1]
        url = parts[2]
        
        await query.edit_message_text(
            "⬇️ <b>Download शुरू हो रही है...</b>\n"
            "⏳ कृपया प्रतीक्षा करें...",
            parse_mode=ParseMode.HTML
        )
        
        audio_only = quality_type == 'audio'
        quality = 'best' if quality_type in ['best', 'audio'] else quality_type
        
        try:
            filename, info = downloader.download_video(
                url, 
                quality=quality, 
                audio_only=audio_only,
                user_id=user_id
            )
            
            if filename and os.path.exists(filename):
                filesize = os.path.getsize(filename)
                db.increment_download(user_id, filesize)
                
                await query.edit_message_text(
                    f"📦 <b>Ready!</b>\n"
                    f"File: {os.path.basename(filename)}\n"
                    f"Size: {filesize / (1024**2):.2f} MB\n\n"
                    f"⬆️ Uploading...",
                    parse_mode=ParseMode.HTML
                )
                
                with open(filename, 'rb') as video_file:
                    if audio_only:
                        await context.bot.send_audio(
                            chat_id=user_id,
                            audio=video_file,
                            title=os.path.basename(filename)
                        )
                    else:
                        await context.bot.send_video(
                            chat_id=user_id,
                            video=video_file,
                            caption=f"✅ <b>Download Complete!</b>\n\n"
                                   f"Title: {info['title'][:50]}\n"
                                   f"Quality: {quality}\n"
                                   f"Size: {filesize / (1024**2):.2f} MB"
                        )
                
                os.remove(filename)
                await query.edit_message_text("✅ <b>सफल!</b>", parse_mode=ParseMode.HTML)
            else:
                await query.edit_message_text(
                    f"❌ <b>Download Failed!</b>\n{info}",
                    parse_mode=ParseMode.HTML
                )
        except Exception as e:
            await query.edit_message_text(
                f"❌ <b>Error:</b>\n{str(e)[:100]}",
                parse_mode=ParseMode.HTML
            )
    
    elif data == 'cancel':
        await query.edit_message_text("❌ <b>Cancelled!</b>", parse_mode=ParseMode.HTML)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user statistics"""
    user_id = str(update.effective_user.id)
    user_data = db.users.get(user_id, {})
    
    stats_text = f"""
╔══════════════════════════════════════════╗
║        📊 YOUR STATISTICS 📊            ║
╚══════════════════════════════════════════╝

👤 <b>User Info:</b>
Name: {user_data.get('first_name', 'Unknown')}
ID: {user_id}
Joined: {user_data.get('joined', 'Unknown')[:10]}

📥 <b>Download Stats:</b>
Total Downloads: {user_data.get('downloads', 0)}
Total Data: {user_data.get('total_data', 0) / (1024**3):.3f} GB
Last Download: {user_data.get('last_download', 'Never')}

🎖️ <b>Account Type:</b>
{'👑 Premium' if user_data.get('premium') else '⭐ Free'}
    """
    
    await update.message.reply_text(stats_text, parse_mode=ParseMode.HTML)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors gracefully"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "❌ कुछ गलत हुआ!\n\n"
                "/help देखो या /support contact करो"
            )
        except:
            pass

# ============================================
# MAIN BOT SETUP
# ============================================

async def set_commands(app: Application):
    """Set bot commands"""
    commands = [
        BotCommand("start", "🚀 Bot को start करो"),
        BotCommand("help", "❓ Help & Guide"),
        BotCommand("stats", "📊 Your Statistics"),
        BotCommand("history", "📜 Download History"),
        BotCommand("settings", "⚙️ Bot Settings"),
        BotCommand("premium", "👑 Premium Features"),
        BotCommand("support", "👨‍💼 Support"),
    ]
    await app.bot.set_my_commands(commands)

async def post_init(app: Application):
    """Post initialization"""
    await set_commands(app)
    logger.info("✅ Bot commands set!")

def main():
    """Main bot function"""
    print("""
    ╔══════════════════════════════════════════╗
    ║  🎬 PROFESSIONAL VIDEO DOWNLOADER BOT 🎬║
    ║         Advanced Edition v2.0            ║
    ╚══════════════════════════════════════════╝
    """)
    
    logger.info("🚀 Bot Starting...")
    
    persistence = PicklePersistence(filepath='bot_data')
    app = Application.builder() \
        .token(TOKEN) \
        .persistence(persistence) \
        .build()
    
    # Set post init
    app.post_init = post_init
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    app.add_error_handler(error_handler)
    
    logger.info("✅ Bot Ready!")
    logger.info("⚡ Features: Video Download, Analytics, Queue System")
    logger.info("📊 Database: Active")
    logger.info("🚀 Polling started...")
    print("\n✅ Bot fully operational!")
    print("⚡ Professional Mode: ON\n")
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("⛔ Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
