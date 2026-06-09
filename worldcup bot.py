#!/usr/bin/env python3
"""
🏆 World Cup 2026 Telegram Bot
Shows all 48 teams and their group stage schedules with match times and stadiums.

Usage:
  1. pip install python-telegram-bot
  2. Set your bot token: BOT_TOKEN = "YOUR_TOKEN_HERE"
  3. python worldcup_bot.py
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)

# ─────────────────────────────────────────────
# CONFIG — replace with your BotFather token
# ─────────────────────────────────────────────
import os
BOT_TOKEN = os.environ.get("BOT_TOKEN")



logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ─────────────────────────────────────────────
# DATA — Group Stage schedules (all times ET)
# ─────────────────────────────────────────────
GROUPS = {
    "A": ["🇲🇽 Mexico", "🇿🇦 South Africa", "🇰🇷 South Korea", "🇨🇿 Czechia"],
    "B": ["🇨🇦 Canada", "🇧🇦 Bosnia & Herzegovina", "🇶🇦 Qatar", "🇨🇭 Switzerland"],
    "C": ["🇧🇷 Brazil", "🇲🇦 Morocco", "🇭🇹 Haiti", "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland"],
    "D": ["🇺🇸 USA", "🇵🇾 Paraguay", "🇦🇺 Australia", "🇹🇷 Türkiye"],
    "E": ["🇩🇪 Germany", "🇨🇼 Curaçao", "🇨🇮 Ivory Coast", "🇪🇨 Ecuador"],
    "F": ["🇳🇱 Netherlands", "🇯🇵 Japan", "🇸🇪 Sweden", "🇹🇳 Tunisia"],
    "G": ["🇧🇪 Belgium", "🇪🇬 Egypt", "🇮🇷 Iran", "🇳🇿 New Zealand"],
    "H": ["🇪🇸 Spain", "🇨🇻 Cape Verde", "🇸🇦 Saudi Arabia", "🇺🇾 Uruguay"],
    "I": ["🇫🇷 France", "🇸🇳 Senegal", "🇮🇶 Iraq", "🇳🇴 Norway"],
    "J": ["🇦🇷 Argentina", "🇩🇿 Algeria", "🇦🇹 Austria", "🇯🇴 Jordan"],
    "K": ["🇵🇹 Portugal", "🇨🇩 DR Congo", "🇺🇿 Uzbekistan", "🇨🇴 Colombia"],
    "L": ["🏴󠁧󠁢󠁥󠁮󠁧󠁿 England", "🇭🇷 Croatia", "🇬🇭 Ghana", "🇵🇦 Panama"],
}

# Each match: (date, time_ET, home, away, stadium, city)
MATCHES = [
    # GROUP A
    ("Thu Jun 11", "3:00 PM ET",  "Mexico",       "South Africa", "Estadio Azteca",          "Mexico City, Mexico"),
    ("Thu Jun 11", "10:00 PM ET", "South Korea",  "Czechia",      "Estadio Akron",            "Zapopan, Mexico"),
    ("Thu Jun 18", "12:00 PM ET", "Czechia",      "South Africa", "Mercedes-Benz Stadium",    "Atlanta, USA"),
    ("Thu Jun 18", "9:00 PM ET",  "Mexico",       "South Korea",  "Estadio Akron",            "Zapopan, Mexico"),
    ("Wed Jun 24", "9:00 PM ET",  "Czechia",      "Mexico",       "Estadio Azteca",           "Mexico City, Mexico"),
    ("Wed Jun 24", "9:00 PM ET",  "South Africa", "South Korea",  "Estadio BBVA",             "Monterrey, Mexico"),
    # GROUP B
    ("Fri Jun 12", "3:00 PM ET",  "Canada",       "Bosnia & Herzegovina", "BMO Field",        "Toronto, Canada"),
    ("Sat Jun 13", "3:00 PM ET",  "Qatar",        "Switzerland",  "Levi's Stadium",           "Santa Clara, USA"),
    ("Thu Jun 18", "3:00 PM ET",  "Switzerland",  "Bosnia & Herzegovina", "SoFi Stadium",     "Inglewood, USA"),
    ("Thu Jun 18", "6:00 PM ET",  "Canada",       "Qatar",        "BC Place",                 "Vancouver, Canada"),
    ("Wed Jun 24", "3:00 PM ET",  "Switzerland",  "Canada",       "BC Place",                 "Vancouver, Canada"),
    ("Wed Jun 24", "3:00 PM ET",  "Bosnia & Herzegovina", "Qatar", "Lumen Field",             "Seattle, USA"),
    # GROUP C
    ("Sat Jun 13", "6:00 PM ET",  "Brazil",       "Morocco",      "MetLife Stadium",          "East Rutherford, USA"),
    ("Sat Jun 13", "9:00 PM ET",  "Haiti",        "Scotland",     "Gillette Stadium",         "Foxborough, USA"),
    ("Fri Jun 19", "6:00 PM ET",  "Scotland",     "Morocco",      "Gillette Stadium",         "Foxborough, USA"),
    ("Fri Jun 19", "8:30 PM ET",  "Brazil",       "Haiti",        "Lincoln Financial Field",  "Philadelphia, USA"),
    ("Wed Jun 24", "6:00 PM ET",  "Scotland",     "Brazil",       "Hard Rock Stadium",        "Miami Gardens, USA"),
    ("Wed Jun 24", "6:00 PM ET",  "Morocco",      "Haiti",        "Mercedes-Benz Stadium",    "Atlanta, USA"),
    # GROUP D
    ("Sun Jun 14", "12:00 PM ET", "Australia",    "Türkiye",      "BC Place",                 "Vancouver, Canada"),
    ("Fri Jun 12", "9:00 PM ET",  "USA",          "Paraguay",     "SoFi Stadium",             "Inglewood, USA"),
    ("Fri Jun 19", "3:00 PM ET",  "USA",          "Australia",    "Lumen Field",              "Seattle, USA"),
    ("Fri Jun 19", "11:00 PM ET", "Türkiye",      "Paraguay",     "Levi's Stadium",           "Santa Clara, USA"),
    ("Thu Jun 25", "10:00 PM ET", "Türkiye",      "USA",          "SoFi Stadium",             "Inglewood, USA"),
    ("Thu Jun 25", "10:00 PM ET", "Paraguay",     "Australia",    "Levi's Stadium",           "Santa Clara, USA"),
    # GROUP E
    ("Sun Jun 14", "1:00 PM ET",  "Germany",      "Curaçao",      "NRG Stadium",              "Houston, USA"),
    ("Sun Jun 14", "7:00 PM ET",  "Ivory Coast",  "Ecuador",      "Lincoln Financial Field",  "Philadelphia, USA"),
    ("Sat Jun 20", "1:00 PM ET",  "Netherlands",  "Sweden",       "NRG Stadium",              "Houston, USA"),
    ("Sat Jun 20", "4:00 PM ET",  "Germany",      "Ivory Coast",  "BMO Field",                "Toronto, Canada"),
    ("Sat Jun 20", "8:00 PM ET",  "Ecuador",      "Curaçao",      "Arrowhead Stadium",        "Kansas City, USA"),
    ("Thu Jun 25", "4:00 PM ET",  "Curaçao",      "Ivory Coast",  "Lincoln Financial Field",  "Philadelphia, USA"),
    ("Thu Jun 25", "4:00 PM ET",  "Ecuador",      "Germany",      "MetLife Stadium",          "East Rutherford, USA"),
    # GROUP F
    ("Sun Jun 14", "4:00 PM ET",  "Netherlands",  "Japan",        "AT&T Stadium",             "Arlington, USA"),
    ("Sun Jun 14", "10:00 PM ET", "Sweden",       "Tunisia",      "Estadio BBVA",             "Monterrey, Mexico"),
    ("Sat Jun 20", "1:00 PM ET",  "Netherlands",  "Sweden",       "NRG Stadium",              "Houston, USA"),
    ("Sun Jun 21", "12:00 AM ET", "Tunisia",      "Japan",        "Estadio BBVA",             "Monterrey, Mexico"),
    ("Thu Jun 25", "7:00 PM ET",  "Japan",        "Sweden",       "AT&T Stadium",             "Arlington, USA"),
    ("Thu Jun 25", "7:00 PM ET",  "Tunisia",      "Netherlands",  "Arrowhead Stadium",        "Kansas City, USA"),
    # GROUP G
    ("Mon Jun 15", "3:00 PM ET",  "Belgium",      "Egypt",        "Lumen Field",              "Seattle, USA"),
    ("Mon Jun 15", "9:00 PM ET",  "Iran",         "New Zealand",  "SoFi Stadium",             "Inglewood, USA"),
    ("Sun Jun 21", "3:00 PM ET",  "Belgium",      "Iran",         "SoFi Stadium",             "Inglewood, USA"),
    ("Sun Jun 21", "9:00 PM ET",  "New Zealand",  "Egypt",        "BC Place",                 "Vancouver, Canada"),
    ("Fri Jun 26", "11:00 PM ET", "Egypt",        "Iran",         "Lumen Field",              "Seattle, USA"),
    ("Fri Jun 26", "11:00 PM ET", "New Zealand",  "Belgium",      "BC Place",                 "Vancouver, Canada"),
    # GROUP H
    ("Mon Jun 15", "12:00 PM ET", "Spain",        "Cape Verde",   "Mercedes-Benz Stadium",    "Atlanta, USA"),
    ("Mon Jun 15", "6:00 PM ET",  "Saudi Arabia", "Uruguay",      "Hard Rock Stadium",        "Miami Gardens, USA"),
    ("Sun Jun 21", "12:00 PM ET", "Spain",        "Saudi Arabia", "Mercedes-Benz Stadium",    "Atlanta, USA"),
    ("Sun Jun 21", "6:00 PM ET",  "Uruguay",      "Cape Verde",   "Hard Rock Stadium",        "Miami Gardens, USA"),
    ("Fri Jun 26", "8:00 PM ET",  "Cape Verde",   "Saudi Arabia", "NRG Stadium",              "Houston, USA"),
    ("Fri Jun 26", "8:00 PM ET",  "Uruguay",      "Spain",        "Estadio Akron",            "Zapopan, Mexico"),
    # GROUP I
    ("Tue Jun 16", "3:00 PM ET",  "France",       "Senegal",      "MetLife Stadium",          "East Rutherford, USA"),
    ("Tue Jun 16", "6:00 PM ET",  "Iraq",         "Norway",       "Gillette Stadium",         "Foxborough, USA"),
    ("Mon Jun 22", "5:00 PM ET",  "France",       "Iraq",         "Lincoln Financial Field",  "Philadelphia, USA"),
    ("Mon Jun 22", "8:00 PM ET",  "Norway",       "Senegal",      "MetLife Stadium",          "East Rutherford, USA"),
    ("Fri Jun 26", "3:00 PM ET",  "Norway",       "France",       "Gillette Stadium",         "Foxborough, USA"),
    ("Fri Jun 26", "3:00 PM ET",  "Senegal",      "Iraq",         "BMO Field",                "Toronto, Canada"),
    # GROUP J
    ("Tue Jun 16", "9:00 PM ET",  "Argentina",    "Algeria",      "Arrowhead Stadium",        "Kansas City, USA"),
    ("Wed Jun 17", "12:00 AM ET", "Austria",      "Jordan",       "Levi's Stadium",           "Santa Clara, USA"),
    ("Mon Jun 22", "1:00 PM ET",  "Argentina",    "Austria",      "AT&T Stadium",             "Arlington, USA"),
    ("Mon Jun 22", "11:00 PM ET", "Jordan",       "Algeria",      "Levi's Stadium",           "Santa Clara, USA"),
    ("Sat Jun 27", "10:00 PM ET", "Algeria",      "Austria",      "Arrowhead Stadium",        "Kansas City, USA"),
    ("Sat Jun 27", "10:00 PM ET", "Jordan",       "Argentina",    "AT&T Stadium",             "Arlington, USA"),
    # GROUP K
    ("Wed Jun 17", "1:00 PM ET",  "Portugal",     "DR Congo",     "NRG Stadium",              "Houston, USA"),
    ("Wed Jun 17", "10:00 PM ET", "Uzbekistan",   "Colombia",     "Estadio Azteca",           "Mexico City, Mexico"),
    ("Tue Jun 23", "1:00 PM ET",  "Portugal",     "Uzbekistan",   "NRG Stadium",              "Houston, USA"),
    ("Tue Jun 23", "10:00 PM ET", "Colombia",     "DR Congo",     "Estadio Akron",            "Zapopan, Mexico"),
    ("Sat Jun 27", "7:30 PM ET",  "Colombia",     "Portugal",     "Hard Rock Stadium",        "Miami Gardens, USA"),
    ("Sat Jun 27", "7:30 PM ET",  "DR Congo",     "Uzbekistan",   "Mercedes-Benz Stadium",    "Atlanta, USA"),
    # GROUP L
    ("Wed Jun 17", "4:00 PM ET",  "England",      "Croatia",      "AT&T Stadium",             "Arlington, USA"),
    ("Wed Jun 17", "7:00 PM ET",  "Ghana",        "Panama",       "BMO Field",                "Toronto, Canada"),
    ("Tue Jun 23", "4:00 PM ET",  "England",      "Ghana",        "Gillette Stadium",         "Foxborough, USA"),
    ("Tue Jun 23", "7:00 PM ET",  "Panama",       "Croatia",      "BMO Field",                "Toronto, Canada"),
    ("Sat Jun 27", "5:00 PM ET",  "Panama",       "England",      "MetLife Stadium",          "East Rutherford, USA"),
    ("Sat Jun 27", "5:00 PM ET",  "Croatia",      "Ghana",        "Lincoln Financial Field",  "Philadelphia, USA"),
]

# ─────────────────────────────────────────────
# Helper: find which group a team belongs to
# ─────────────────────────────────────────────
def find_group(team_raw: str) -> str | None:
    """Return group letter for a team name (ignoring flag emoji)."""
    name = team_raw.strip().split(" ", 1)[-1]  # strip emoji
    for grp, members in GROUPS.items():
        for m in members:
            if name.lower() in m.lower():
                return grp
    return None


def get_team_matches(team_raw: str) -> list:
    """Return all group stage matches for a given team."""
    name = team_raw.strip().split(" ", 1)[-1].lower()
    results = []
    for m in MATCHES:
        date, time, home, away, stadium, city = m
        if name in home.lower() or name in away.lower():
            results.append(m)
    # deduplicate (some matches appear twice in data for diff groups)
    seen = set()
    unique = []
    for m in results:
        key = (m[0], m[2], m[3])
        if key not in seen:
            seen.add(key)
            unique.append(m)
    return sorted(unique, key=lambda x: x[0])


# ─────────────────────────────────────────────
# BOT HANDLERS
# ─────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send group selection keyboard."""
    keyboard = []
    row = []
    for grp in sorted(GROUPS.keys()):
        row.append(InlineKeyboardButton(f"Group {grp}", callback_data=f"grp_{grp}"))
        if len(row) == 4:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    await update.message.reply_text(
        "🏆 *FIFA World Cup 2026*\n\nیه گروه انتخاب کن تا تیم‌هاشو ببینی:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # ── Group selected → show teams ──
    if data.startswith("grp_"):
        grp = data[4:]
        teams = GROUPS.get(grp, [])
        keyboard = [
            [InlineKeyboardButton(t, callback_data=f"team_{t}")]
            for t in teams
        ]
        keyboard.append([InlineKeyboardButton("🔙 بازگشت به گروه‌ها", callback_data="back_groups")])
        await query.edit_message_text(
            f"⚽ *گروه {grp}* — یه تیم انتخاب کن:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ── Team selected → show matches ──
    elif data.startswith("team_"):
        team_raw = data[5:]
        matches = get_team_matches(team_raw)
        grp = find_group(team_raw)
        name_clean = team_raw.split(" ", 1)[-1] if " " in team_raw else team_raw

        if not matches:
            text = f"❌ بازی‌ای برای {team_raw} پیدا نشد."
        else:
            lines = [f"📋 *بازی‌های {team_raw}* — گروه {grp}\n"]
            for i, (date, time, home, away, stadium, city) in enumerate(matches, 1):
                vs = f"{home} vs {away}"
                lines.append(
                    f"*بازی {i}*\n"
                    f"📅 {date}  ⏰ {time}\n"
                    f"⚔️ {vs}\n"
                    f"🏟 {stadium}\n"
                    f"📍 {city}\n"
                )
            text = "\n".join(lines)

        keyboard = [
            [InlineKeyboardButton(f"🔙 بازگشت به گروه {grp}", callback_data=f"grp_{grp}")],
            [InlineKeyboardButton("🏠 منوی اصلی", callback_data="back_groups")],
        ]
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ── Back to group list ──
    elif data == "back_groups":
        keyboard = []
        row = []
        for grp in sorted(GROUPS.keys()):
            row.append(InlineKeyboardButton(f"Group {grp}", callback_data=f"grp_{grp}"))
            if len(row) == 4:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        await query.edit_message_text(
            "🏆 *FIFA World Cup 2026*\n\nیه گروه انتخاب کن:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    print("✅ Bot is running... Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
