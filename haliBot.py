import os
import random
import asyncio
import requests
import google.generativeai as genai
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
from dotenv import load_dotenv

# === LOAD ENVIRONMENT VARIABLES ===
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_KEY_HERE").strip()

BOT_NAME = "HaliTech"
CHANNEL_ID = "@Hali-Tech"

# === CONFIGURE GEMINI ===
genai.configure(api_key=GEMINI_API_KEY)
MODEL_NAME = "models/gemini-2.5-flash"
model = genai.GenerativeModel(MODEL_NAME)

# === DAILY CONTENT ===
TECH_FACTS = [
    "💡 HTML stands for HyperText Markup Language — it’s not a programming language!",
    "⚙️ CSS Flexbox makes responsive layouts so much easier.",
    "🐍 Python is named after the comedy group ‘Monty Python’, not the snake!",
    "🧠 The first website ever created is still online: http://info.cern.ch/",
    "💾 Git was created by Linus Torvalds, the same person who made Linux."
]

ENCOURAGEMENTS = [
    "🚀 Keep learning — small progress daily leads to big success!",
    "💪 Every expert was once a beginner. Keep coding!",
    "🔥 Debugging is where real developers are born!",
    "🌱 Don’t compare, just grow — your time will come!",
    "🎯 One more line of code could change your future!"
]

MEMES = [
    "😂 When your code works on the first try... `print('Miracle!')`",
    "💻 Developer’s diet: caffeine, bugs, and hope.",
    "🧠 StackOverflow is the real university.",
    "😅 Me: I’ll fix that later. Bug: *becomes feature*",
    "📟 404: Motivation not found."
]

# === COMMAND HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Web Dev 🌐", callback_data='webdev'),
            InlineKeyboardButton("Python 🐍", callback_data='python'),
            InlineKeyboardButton("Tech News 📰", callback_data='news')
        ],
        [
            InlineKeyboardButton("Ethical Hacking 💀", callback_data='hacking'),
            InlineKeyboardButton("Cybersecurity 🛡️", callback_data='cyber'),
            InlineKeyboardButton("AI & ML 🤖", callback_data='aiml')
        ],
        [
            InlineKeyboardButton("Networking 🌐", callback_data='networking'),
            InlineKeyboardButton("Cloud ☁️", callback_data='cloud'),
            InlineKeyboardButton("DevOps ⚙️", callback_data='devops')
        ],
        [
            InlineKeyboardButton("Data Science 📊", callback_data='datasci'),
            InlineKeyboardButton("Ask Hali ❓", callback_data='hali')
        ]
    ]
    await update.message.reply_text(
        f"👋 Welcome to {BOT_NAME}!\n\nExplore different tech fields below — I’ll share top learning resources for each:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Commands List:\n"
        "/start - Welcome message\n"
        "/help - Show this help\n"
        "/webdev - Web Dev Resources\n"
        "/python - Python Resources\n"
        "/hali <question> - Ask Hali\n"
        "/channel - About Hali-Tech"
    )

async def webdev(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 Web Development Resources:\n"
        "• MDN: https://developer.mozilla.org\n"
        "• FreeCodeCamp: https://freecodecamp.org\n"
        "• CSS Tricks: https://css-tricks.com"
    )

async def python_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🐍 Python Learning:\n"
        "• Docs: https://docs.python.org/3/\n"
        "• Real Python: https://realpython.com"
    )

async def channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📢 Hali-Tech Channel — Tech tips, memes, and motivation!\n"
        "📢 You can ask everything to HALI — by writing: /hali <then your answer here>!\n"
        "🌐 Author: Eng. Ahmed Hassen <ahmedhassenmohamed11@gmail.com>"
    )

# === INLINE BUTTON CALLBACKS ===
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    topics = {
        "webdev": "🌐 **Web Development Resources**:\n• [MDN Docs](https://developer.mozilla.org)\n• [FreeCodeCamp](https://freecodecamp.org)\n• [CSS Tricks](https://css-tricks.com)",
        "python": "🐍 **Python Learning**:\n• [Docs](https://docs.python.org/3/)\n• [Real Python](https://realpython.com)\n• [Python Tutor](https://pythontutor.com)",
        "news": "📰 **Tech News Sources**:\n• [TechCrunch](https://techcrunch.com)\n• [The Verge](https://theverge.com)\n• [Wired](https://wired.com)",
        "hacking": "💀 **Ethical Hacking Resources**:\n• [TryHackMe](https://tryhackme.com)\n• [Hack The Box](https://hackthebox.com)\n• [PortSwigger Academy](https://portswigger.net/web-security)\n• [OverTheWire](https://overthewire.org)\n• [Hacker101](https://www.hacker101.com)",
        "cyber": "🛡️ **Cybersecurity Resources**:\n• [Cybrary](https://www.cybrary.it)\n• [CISA](https://www.cisa.gov)\n• [MITRE ATT&CK](https://attack.mitre.org)\n• [Security Blue Team](https://securityblue.team)\n• [r/cybersecurity](https://www.reddit.com/r/cybersecurity)",
        "aiml": "🤖 **AI & Machine Learning**:\n• [Kaggle](https://www.kaggle.com)\n• [Google AI](https://ai.google)\n• [Hugging Face](https://huggingface.co)\n• [Coursera AI](https://www.coursera.org/browse/data-science/machine-learning)",
        "networking": "🌐 **Networking Resources**:\n• [Cisco Networking Academy](https://www.netacad.com)\n• [NetworkLessons](https://networklessons.com)\n• [CompTIA Network+](https://www.comptia.org)\n• [r/networking](https://www.reddit.com/r/networking)",
        "cloud": "☁️ **Cloud Computing Resources**:\n• [AWS Training](https://aws.amazon.com/training)\n• [Microsoft Learn Azure](https://learn.microsoft.com/en-us/training/azure)\n• [Google Cloud Skills Boost](https://cloudskillsboost.google)\n• [Cloud Guru](https://acloudguru.com)",
        "devops": "⚙️ **DevOps Resources**:\n• [Docker Docs](https://docs.docker.com)\n• [Kubernetes](https://kubernetes.io)\n• [Jenkins](https://www.jenkins.io)\n• [GitHub Actions](https://github.com/features/actions)\n• [DevOps Roadmap](https://roadmap.sh/devops)",
        "datasci": "📊 **Data Science Resources**:\n• [Kaggle](https://www.kaggle.com)\n• [DataCamp](https://www.datacamp.com)\n• [Analytics Vidhya](https://www.analyticsvidhya.com)\n• [r/datascience](https://www.reddit.com/r/datascience)"
    }

    if data in topics:
        await query.edit_message_text(topics[data], parse_mode="Markdown", disable_web_page_preview=True)
    elif data == 'hali':
        await query.edit_message_text("Type /hali <your question> to chat with Hali AI.")
    else:
        await query.edit_message_text("Unknown option.")

# === AI HANDLER (Gemini API) ===
async def ai_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = " ".join(context.args)
    if not question:
        await update.message.reply_text("🧠 Example: /hali What is quantum computing?")
        return

    await update.message.reply_text("🤖 Hali is Thinking... please be patient.")
    try:
        response = model.generate_content(question)
        if hasattr(response, "text") and response.text:
            answer = response.text.strip()
        else:
            answer = "⚠️ Sorry, Hali didn’t return a response."
    except Exception as e:
        print("an error to reach Hali server", e)
        answer = "⚠️ Sorry, I couldn’t get a response from Hali right now."

    await update.message.reply_text(answer)

# === AUTO-ASSIST & SPAM FILTER ===
async def tech_assist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if "react" in text:
        await update.message.reply_text("⚛️ React is a JS library for UI. Need setup help?")
    elif "django" in text:
        await update.message.reply_text("Django docs: https://docs.djangoproject.com/")
    elif "python" in text:
        await python_info(update, context)
    elif any(w in text for w in ["web", "html", "css"]):
        await webdev(update, context)
    else:
        await update.message.reply_text("🤔 Interesting! Use /hali <question> for a smart answer.")

async def filter_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if "http" in text or "t.me/" in text or text.count("!") > 5:
        try:
            await update.message.delete()
            print("🚫 Spam removed.")
        except:
            pass

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(f"👋 Welcome, {member.first_name}! Glad to have you in Hali-Tech 💻")

# === AUTO POST DAILY ===
async def post_daily(context: ContextTypes.DEFAULT_TYPE):
    fact = random.choice(TECH_FACTS)
    encouragement = random.choice(ENCOURAGEMENTS)
    meme = random.choice(MEMES)
    message = f"{fact}\n\n{encouragement}\n\n{meme}"
    try:
        await context.bot.send_message(chat_id=CHANNEL_ID, text=message)
        print("✅ Auto-post sent to channel.")
    except Exception as e:
        print("⚠️ Failed to send scheduled post:", e)

# === SETUP BOT ===
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("webdev", webdev))
app.add_handler(CommandHandler("python", python_info))
app.add_handler(CommandHandler("channel", channel))
app.add_handler(CommandHandler("hali", ai_answer))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tech_assist))
app.add_handler(MessageHandler(filters.TEXT, filter_spam))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
app.add_handler(CallbackQueryHandler(button))

# === SCHEDULER ===
scheduler = AsyncIOScheduler()
scheduler.add_job(lambda: asyncio.create_task(post_daily(app)), 'cron', hour=9, minute=0)
scheduler.add_job(lambda: asyncio.create_task(post_daily(app)), 'cron', hour=18, minute=0)

# === MAIN LOOP ===
async def main():
    scheduler.start()
    print("🤖 Hali-Tech bot running with scheduler...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    try:
        await asyncio.Event().wait()  # Keeps bot alive
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
