#!/usr/bin/env python3
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatMember
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = "@iFootBad"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

GROUPS = {
    "A": ["🇲🇽 مکزیک", "🇿🇦 آفریقای جنوبی", "🇰🇷 کره جنوبی", "🇨🇿 چک"],
    "B": ["🇨🇦 کانادا", "🇧🇦 بوسنی و هرزگوین", "🇶🇦 قطر", "🇨🇭 سوئیس"],
    "C": ["🇧🇷 برزیل", "🇲🇦 مراکش", "🇭🇹 هائیتی", "🏴󠁧󠁢󠁳󠁣󠁴󠁿 اسکاتلند"],
    "D": ["🇺🇸 آمریکا", "🇵🇾 پاراگوئه", "🇦🇺 استرالیا", "🇹🇷 ترکیه"],
    "E": ["🇩🇪 آلمان", "🇨🇼 کوراسائو", "🇨🇮 ساحل عاج", "🇪🇨 اکوادور"],
    "F": ["🇳🇱 هلند", "🇯🇵 ژاپن", "🇸🇪 سوئد", "🇹🇳 تونس"],
    "G": ["🇧🇪 بلژیک", "🇪🇬 مصر", "🇮🇷 ایران", "🇳🇿 نیوزیلند"],
    "H": ["🇪🇸 اسپانیا", "🇨🇻 کیپ ورد", "🇸🇦 عربستان سعودی", "🇺🇾 اروگوئه"],
    "I": ["🇫🇷 فرانسه", "🇸🇳 سنگال", "🇮🇶 عراق", "🇳🇴 نروژ"],
    "J": ["🇦🇷 آرژانتین", "🇩🇿 الجزایر", "🇦🇹 اتریش", "🇯🇴 اردن"],
    "K": ["🇵🇹 پرتغال", "🇨🇩 کنگو", "🇺🇿 ازبکستان", "🇨🇴 کلمبیا"],
    "L": ["🏴󠁧󠁢󠁥󠁮󠁧󠁿 انگلیس", "🇭🇷 کرواسی", "🇬🇭 غنا", "🇵🇦 پاناما"],
}

FA_TO_EN = {
    "مکزیک": "Mexico", "آفریقای جنوبی": "South Africa", "کره جنوبی": "South Korea", "چک": "Czechia",
    "کانادا": "Canada", "بوسنی و هرزگوین": "Bosnia", "قطر": "Qatar", "سوئیس": "Switzerland",
    "برزیل": "Brazil", "مراکش": "Morocco", "هائیتی": "Haiti", "اسکاتلند": "Scotland",
    "آمریکا": "USA", "پاراگوئه": "Paraguay", "استرالیا": "Australia", "ترکیه": "Turkiye",
    "آلمان": "Germany", "کوراسائو": "Curacao", "ساحل عاج": "Ivory Coast", "اکوادور": "Ecuador",
    "هلند": "Netherlands", "ژاپن": "Japan", "سوئد": "Sweden", "تونس": "Tunisia",
    "بلژیک": "Belgium", "مصر": "Egypt", "ایران": "Iran", "نیوزیلند": "New Zealand",
    "اسپانیا": "Spain", "کیپ ورد": "Cape Verde", "عربستان سعودی": "Saudi Arabia", "اروگوئه": "Uruguay",
    "فرانسه": "France", "سنگال": "Senegal", "عراق": "Iraq", "نروژ": "Norway",
    "آرژانتین": "Argentina", "الجزایر": "Algeria", "اتریش": "Austria", "اردن": "Jordan",
    "پرتغال": "Portugal", "کنگو": "DR Congo", "ازبکستان": "Uzbekistan", "کلمبیا": "Colombia",
    "انگلیس": "England", "کرواسی": "Croatia", "غنا": "Ghana", "پاناما": "Panama",
}

EN_TO_FA = {v: k for k, v in FA_TO_EN.items()}

def et_to_iran(time_et: str) -> str:
    try:
        from datetime import datetime, timedelta
        t = datetime.strptime(time_et, "%I:%M %p")
        iran_t = t + timedelta(hours=7, minutes=30)
        result = iran_t.strftime("%H:%M")
        if iran_t.day != t.day:
            return result + " (روز بعد)"
        return result
    except:
        return time_et

# date, time_ET, home_EN, away_EN, stadium_FA, city_FA
MATCHES = [
    ("پنج‌شنبه ۲۱ خرداد", "3:00 PM", "Mexico", "South Africa", "استادیوم آزتکا", "مکزیکوسیتی"),
    ("پنج‌شنبه ۲۱ خرداد", "10:00 PM", "South Korea", "Czechia", "استادیوم آکرون", "گوادالاخارا"),
    ("جمعه ۲۲ خرداد", "3:00 PM", "Canada", "Bosnia", "BMO فیلد", "تورنتو"),
    ("جمعه ۲۲ خرداد", "9:00 PM", "USA", "Paraguay", "سوفای استادیوم", "اینگلووود"),
    ("شنبه ۲۳ خرداد", "3:00 PM", "Qatar", "Switzerland", "لوی‌ استادیوم", "سانتاکلارا"),
    ("شنبه ۲۳ خرداد", "6:00 PM", "Brazil", "Morocco", "مت‌لایف استادیوم", "نیوجرسی"),
    ("شنبه ۲۳ خرداد", "9:00 PM", "Haiti", "Scotland", "گیلت استادیوم", "فاکسبورو"),
    ("یکشنبه ۲۴ خرداد", "12:00 PM", "Australia", "Turkiye", "BC پلیس", "ونکوور"),
    ("یکشنبه ۲۴ خرداد", "1:00 PM", "Germany", "Curacao", "NRG استادیوم", "هیوستون"),
    ("یکشنبه ۲۴ خرداد", "4:00 PM", "Netherlands", "Japan", "AT&T استادیوم", "آرلینگتون"),
    ("یکشنبه ۲۴ خرداد", "7:00 PM", "Ivory Coast", "Ecuador", "لینکلن فاینانشیال فیلد", "فیلادلفیا"),
    ("یکشنبه ۲۴ خرداد", "10:00 PM", "Sweden", "Tunisia", "استادیوم BBVA", "مونتری"),
    ("دوشنبه ۲۵ خرداد", "12:00 PM", "Spain", "Cape Verde", "مرسدس-بنز استادیوم", "آتلانتا"),
    ("دوشنبه ۲۵ خرداد", "3:00 PM", "Belgium", "Egypt", "لومن فیلد", "سیاتل"),
    ("دوشنبه ۲۵ خرداد", "6:00 PM", "Saudi Arabia", "Uruguay", "هارد راک استادیوم", "مایامی"),
    ("دوشنبه ۲۵ خرداد", "9:00 PM", "Iran", "New Zealand", "سوفای استادیوم", "اینگلووود"),
    ("سه‌شنبه ۲۶ خرداد", "3:00 PM", "France", "Senegal", "مت‌لایف استادیوم", "نیوجرسی"),
    ("سه‌شنبه ۲۶ خرداد", "6:00 PM", "Iraq", "Norway", "گیلت استادیوم", "فاکسبورو"),
    ("سه‌شنبه ۲۶ خرداد", "9:00 PM", "Argentina", "Algeria", "اروهد استادیوم", "کانزاس سیتی"),
    ("چهارشنبه ۲۷ خرداد", "12:00 AM", "Austria", "Jordan", "لوی‌ استادیوم", "سانتاکلارا"),
    ("چهارشنبه ۲۷ خرداد", "1:00 PM", "Portugal", "DR Congo", "NRG استادیوم", "هیوستون"),
    ("چهارشنبه ۲۷ خرداد", "4:00 PM", "England", "Croatia", "AT&T استادیوم", "آرلینگتون"),
    ("چهارشنبه ۲۷ خرداد", "7:00 PM", "Ghana", "Panama", "BMO فیلد", "تورنتو"),
    ("چهارشنبه ۲۷ خرداد", "10:00 PM", "Uzbekistan", "Colombia", "استادیوم آزتکا", "مکزیکوسیتی"),
    ("پنج‌شنبه ۲۸ خرداد", "12:00 PM", "Czechia", "South Africa", "مرسدس-بنز استادیوم", "آتلانتا"),
    ("پنج‌شنبه ۲۸ خرداد", "3:00 PM", "Switzerland", "Bosnia", "سوفای استادیوم", "اینگلووود"),
    ("پنج‌شنبه ۲۸ خرداد", "6:00 PM", "Canada", "Qatar", "BC پلیس", "ونکوور"),
    ("پنج‌شنبه ۲۸ خرداد", "9:00 PM", "Mexico", "South Korea", "استادیوم آکرون", "گوادالاخارا"),
    ("جمعه ۲۹ خرداد", "3:00 PM", "USA", "Australia", "لومن فیلد", "سیاتل"),
    ("جمعه ۲۹ خرداد", "6:00 PM", "Scotland", "Morocco", "گیلت استادیوم", "فاکسبورو"),
    ("جمعه ۲۹ خرداد", "8:30 PM", "Brazil", "Haiti", "لینکلن فاینانشیال فیلد", "فیلادلفیا"),
    ("جمعه ۲۹ خرداد", "11:00 PM", "Turkiye", "Paraguay", "لوی‌ استادیوم", "سانتاکلارا"),
    ("شنبه ۳۰ خرداد", "1:00 PM", "Netherlands", "Sweden", "NRG استادیوم", "هیوستون"),
    ("شنبه ۳۰ خرداد", "4:00 PM", "Germany", "Ivory Coast", "BMO فیلد", "تورنتو"),
    ("شنبه ۳۰ خرداد", "8:00 PM", "Ecuador", "Curacao", "اروهد استادیوم", "کانزاس سیتی"),
    ("یکشنبه ۳۱ خرداد", "12:00 AM", "Tunisia", "Japan", "استادیوم BBVA", "مونتری"),
    ("یکشنبه ۳۱ خرداد", "12:00 PM", "Spain", "Saudi Arabia", "مرسدس-بنز استادیوم", "آتلانتا"),
    ("یکشنبه ۳۱ خرداد", "3:00 PM", "Belgium", "Iran", "سوفای استادیوم", "اینگلووود"),
    ("یکشنبه ۳۱ خرداد", "6:00 PM", "Uruguay", "Cape Verde", "هارد راک استادیوم", "مایامی"),
    ("یکشنبه ۳۱ خرداد", "9:00 PM", "New Zealand", "Egypt", "BC پلیس", "ونکوور"),
    ("دوشنبه ۱ تیر", "1:00 PM", "Argentina", "Austria", "AT&T استادیوم", "آرلینگتون"),
    ("دوشنبه ۱ تیر", "5:00 PM", "France", "Iraq", "لینکلن فاینانشیال فیلد", "فیلادلفیا"),
    ("دوشنبه ۱ تیر", "8:00 PM", "Norway", "Senegal", "مت‌لایف استادیوم", "نیوجرسی"),
    ("دوشنبه ۱ تیر", "11:00 PM", "Jordan", "Algeria", "لوی‌ استادیوم", "سانتاکلارا"),
    ("سه‌شنبه ۲ تیر", "1:00 PM", "Portugal", "Uzbekistan", "NRG استادیوم", "هیوستون"),
    ("سه‌شنبه ۲ تیر", "4:00 PM", "England", "Ghana", "گیلت استادیوم", "فاکسبورو"),
    ("سه‌شنبه ۲ تیر", "7:00 PM", "Panama", "Croatia", "BMO فیلد", "تورنتو"),
    ("سه‌شنبه ۲ تیر", "10:00 PM", "Colombia", "DR Congo", "استادیوم آکرون", "گوادالاخارا"),
    ("چهارشنبه ۳ تیر", "3:00 PM", "Switzerland", "Canada", "BC پلیس", "ونکوور"),
    ("چهارشنبه ۳ تیر", "3:00 PM", "Bosnia", "Qatar", "لومن فیلد", "سیاتل"),
    ("چهارشنبه ۳ تیر", "6:00 PM", "Scotland", "Brazil", "هارد راک استادیوم", "مایامی"),
    ("چهارشنبه ۳ تیر", "6:00 PM", "Morocco", "Haiti", "مرسدس-بنز استادیوم", "آتلانتا"),
    ("چهارشنبه ۳ تیر", "9:00 PM", "Czechia", "Mexico", "استادیوم آزتکا", "مکزیکوسیتی"),
    ("چهارشنبه ۳ تیر", "9:00 PM", "South Africa", "South Korea", "استادیوم BBVA", "مونتری"),
    ("پنج‌شنبه ۴ تیر", "4:00 PM", "Curacao", "Ivory Coast", "لینکلن فاینانشیال فیلد", "فیلادلفیا"),
    ("پنج‌شنبه ۴ تیر", "4:00 PM", "Ecuador", "Germany", "مت‌لایف استادیوم", "نیوجرسی"),
    ("پنج‌شنبه ۴ تیر", "7:00 PM", "Japan", "Sweden", "AT&T استادیوم", "آرلینگتون"),
    ("پنج‌شنبه ۴ تیر", "7:00 PM", "Tunisia", "Netherlands", "اروهد استادیوم", "کانزاس سیتی"),
    ("پنج‌شنبه ۴ تیر", "10:00 PM", "Turkiye", "USA", "سوفای استادیوم", "اینگلووود"),
    ("پنج‌شنبه ۴ تیر", "10:00 PM", "Paraguay", "Australia", "لوی‌ استادیوم", "سانتاکلارا"),
    ("جمعه ۵ تیر", "3:00 PM", "Norway", "France", "گیلت استادیوم", "فاکسبورو"),
    ("جمعه ۵ تیر", "3:00 PM", "Senegal", "Iraq", "BMO فیلد", "تورنتو"),
    ("جمعه ۵ تیر", "8:00 PM", "Cape Verde", "Saudi Arabia", "NRG استادیوم", "هیوستون"),
    ("جمعه ۵ تیر", "8:00 PM", "Uruguay", "Spain", "استادیوم آکرون", "گوادالاخارا"),
    ("جمعه ۵ تیر", "11:00 PM", "Egypt", "Iran", "لومن فیلد", "سیاتل"),
    ("جمعه ۵ تیر", "11:00 PM", "New Zealand", "Belgium", "BC پلیس", "ونکوور"),
    ("شنبه ۶ تیر", "5:00 PM", "Panama", "England", "مت‌لایف استادیوم", "نیوجرسی"),
    ("شنبه ۶ تیر", "5:00 PM", "Croatia", "Ghana", "لینکلن فاینانشیال فیلد", "فیلادلفیا"),
    ("شنبه ۶ تیر", "7:30 PM", "Colombia", "Portugal", "هارد راک استادیوم", "مایامی"),
    ("شنبه ۶ تیر", "7:30 PM", "DR Congo", "Uzbekistan", "مرسدس-بنز استادیوم", "آتلانتا"),
    ("شنبه ۶ تیر", "10:00 PM", "Algeria", "Austria", "اروهد استادیوم", "کانزاس سیتی"),
    ("شنبه ۶ تیر", "10:00 PM", "Jordan", "Argentina", "AT&T استادیوم", "آرلینگتون"),
]


def find_group(team_fa: str) -> str | None:
    name = team_fa.split(" ", 1)[-1]
    for grp, members in GROUPS.items():
        for m in members:
            m_name = m.split(" ", 1)[-1]
            if name == m_name:
                return grp
    return None


def get_team_matches(team_fa: str) -> list:
    name_fa = team_fa.split(" ", 1)[-1]
    name_en = FA_TO_EN.get(name_fa, "")
    results = []
    seen = set()
    for m in MATCHES:
        date, time_et, home, away, stadium, city = m
        if name_en.lower() in home.lower() or name_en.lower() in away.lower():
            key = (date, home, away)
            if key not in seen:
                seen.add(key)
                results.append(m)
    return results


async def check_membership(user_id: int, context) -> bool:
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in [ChatMember.MEMBER, ChatMember.ADMINISTRATOR, ChatMember.OWNER]
    except:
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await check_membership(user_id, context):
        keyboard = [[
            InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{CHANNEL_ID.lstrip('@')}"),
            InlineKeyboardButton("✅ عضو شدم", callback_data="check_join"),
        ]]
        await update.message.reply_text(
            f"⛔️ برای استفاده از بات باید عضو کانال ما باشی:\n\n{CHANNEL_ID}\n\nبعد از عضویت روی «✅ عضو شدم» بزن.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    await show_groups(update, context, is_message=True)


async def show_groups(update, context, is_message=False):
    keyboard = []
    row = []
    for grp in sorted(GROUPS.keys()):
        row.append(InlineKeyboardButton(f"گروه {grp}", callback_data=f"grp_{grp}"))
        if len(row) == 4:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    text = "🏆 *جام جهانی ۲۰۲۶*\n\nیه گروه انتخاب کن:"
    markup = InlineKeyboardMarkup(keyboard)
    if is_message:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=markup)
    else:
        await update.callback_query.edit_message_text(text, parse_mode="Markdown", reply_markup=markup)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = update.effective_user.id

    if data == "check_join":
        if await check_membership(user_id, context):
            await show_groups(update, context)
        else:
            await query.answer("❌ هنوز عضو نشدی!", show_alert=True)
        return

    if not await check_membership(user_id, context):
        keyboard = [[
            InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{CHANNEL_ID.lstrip('@')}"),
            InlineKeyboardButton("✅ عضو شدم", callback_data="check_join"),
        ]]
        await query.edit_message_text(
            f"⛔️ باید عضو کانال باشی:\n{CHANNEL_ID}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    if data.startswith("grp_"):
        grp = data[4:]
        teams = GROUPS.get(grp, [])
        keyboard = [[InlineKeyboardButton(t, callback_data=f"team_{t}")] for t in teams]
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="back_groups")])
        await query.edit_message_text(
            f"⚽ *گروه {grp}* — یه تیم انتخاب کن:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("team_"):
        team_raw = data[5:]
        matches = get_team_matches(team_raw)
        grp = find_group(team_raw)
        if not matches:
            text = "❌ بازی‌ای پیدا نشد."
        else:
            lines = [f"📋 *بازی‌های {team_raw}* — گروه {grp}\n"]
            for i, (date, time_et, home, away, stadium, city) in enumerate(matches, 1):
                home_fa = EN_TO_FA.get(home, home)
                away_fa = EN_TO_FA.get(away, away)
                iran_time = et_to_iran(time_et)
                lines.append(
                    f"*بازی {i}*\n"
                    f"📅 {date}\n"
                    f"⏰ ساعت ایران: {iran_time}\n"
                    f"⚔️ {home_fa} vs {away_fa}\n"
                    f"🏟 {stadium} — {city}\n"
                )
            text = "\n".join(lines)
        keyboard = [
            [InlineKeyboardButton(f"🔙 گروه {grp}", callback_data=f"grp_{grp}")],
            [InlineKeyboardButton("🏠 منوی اصلی", callback_data="back_groups")],
        ]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "back_groups":
        await show_groups(update, context)


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
