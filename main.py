import os
import sqlite3

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)


# =========================
# BOT SETTINGS
# =========================

TOKEN = os.getenv("BOT_TOKEN")
DB_NAME = "gym_bot.db"


# =========================
# WORKOUTS
# =========================

DAY_1_EXERCISES = {
    "ex1": ("Жим штанги лёжа", "4 × 6–10"),
    "ex2": ("Жим гантелей на наклонной скамье", "3 × 8–12"),
    "ex3": ("Разводка гантелей", "3 × 10–15"),
    "ex4": ("Жим гантелей вверх", "3 × 8–12"),
    "ex5": ("Разгибание рук на блоке", "3 × 10–15"),
    "ex6": ("Французский жим", "2 × 10–12"),
}

DAY_2_EXERCISES = {
    "ex1": ("Тяга верхнего блока", "4 × 8–12"),
    "ex2": ("Тяга горизонтального блока", "3 × 8–12"),
    "ex3": ("Тяга гантели одной рукой", "3 × 8–12"),
    "ex4": ("Face Pull", "3 × 12–15"),
    "ex5": ("Подъём штанги на бицепс", "3 × 8–12"),
    "ex6": ("Подъём гантелей на бицепс", "3 × 10–12"),
}

DAY_3_EXERCISES = {
    "ex1": ("Приседания / жим ногами", "4 × 6–10"),
    "ex2": ("Сгибание ног в тренажёре", "3 × 10–15"),
    "ex3": ("Разгибание ног", "3 × 10–15"),
    "ex4": ("Подъём на носки", "4 × 12–20"),
    "ex5": ("Жим гантелей лёжа", "3 × 8–12"),
    "ex6": ("Разведения гантелей в стороны", "3 × 12–15"),
    "ex7": ("Молотки", "2 × 10–12"),
    "ex8": ("Разгибание на блоке", "2 × 10–12"),
}


# =========================
# DATABASE
# =========================

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            user_id INTEGER,
            day INTEGER,
            exercise_id TEXT,
            url TEXT,
            PRIMARY KEY (user_id, day, exercise_id)
        )
    """)

    conn.commit()
    conn.close()


# =========================
# LANGUAGES
# =========================

LANGUAGES = {
    "kk": {
        "choose": "🌐 Тілді таңдаңыз:",
        "home": (
            "🏋️ Менің Gym Bot-ым\n\n"
            "Аптасына 3 рет жаттығамыз 💪\n\n"
            "Күніңді таңда:"
        ),
        "day1": "📅 1-КҮН",
        "day2": "📅 2-КҮН",
        "day3": "📅 3-КҮН",
        "progress": "📊 ПРОГРЕСС",
        "reset": "🔄 АПТАНЫ ҚАЙТА БАСТАУ",
        "back_home": "⬅️ Басты мәзір",
        "back": "⬅️ Артқа",
        "choose_exercise": "Жаттығуды таңда:",
        "video": "▶️ YouTube ВИДЕО",
        "add_video": "➕ ВИДЕО ҚОСУ",
        "change_video": "🔄 ВИДЕОНЫ АУЫСТЫРУ",
        "program": "📋 Бағдарлама",
        "video_saved": "✅ Видео сақталды!",
        "send_video": "YouTube видеосының сілтемесін жібер:",
        "not_youtube": (
            "❌ Бұл YouTube сілтемесі емес сияқты.\n\n"
            "YouTube сілтемесін жібер."
        ),
        "cancel": "❌ Болдырмау",
        "progress_text": (
            "📊 ПРОГРЕСС\n\n"
            "Бұл бөлімді кейін жасаймыз 💪"
        ),
        "reset_text": (
            "🔄 АПТАНЫ ҚАЙТА БАСТАУ\n\n"
            "Бұл функцияны кейін қосамыз."
        ),
    },

    "ru": {
        "choose": "🌐 Выберите язык:",
        "home": (
            "🏋️ Мой Gym Bot\n\n"
            "Тренируемся 3 раза в неделю 💪\n\n"
            "Выберите день:"
        ),
        "day1": "📅 ДЕНЬ 1",
        "day2": "📅 ДЕНЬ 2",
        "day3": "📅 ДЕНЬ 3",
        "progress": "📊 ПРОГРЕСС",
        "reset": "🔄 НАЧАТЬ НЕДЕЛЮ ЗАНОВО",
        "back_home": "⬅️ Главное меню",
        "back": "⬅️ Назад",
        "choose_exercise": "Выберите упражнение:",
        "video": "▶️ YouTube ВИДЕО",
        "add_video": "➕ ДОБАВИТЬ ВИДЕО",
        "change_video": "🔄 ЗАМЕНИТЬ ВИДЕО",
        "program": "📋 Программа",
        "video_saved": "✅ Видео сохранено!",
        "send_video": "Отправьте ссылку на YouTube:",
        "not_youtube": (
            "❌ Похоже, это не ссылка YouTube.\n\n"
            "Отправьте ссылку YouTube."
        ),
        "cancel": "❌ Отмена",
        "progress_text": (
            "📊 ПРОГРЕСС\n\n"
            "Этот раздел сделаем позже 💪"
        ),
        "reset_text": (
            "🔄 НАЧАТЬ НЕДЕЛЮ ЗАНОВО\n\n"
            "Эту функцию добавим позже."
        ),
    },

    "en": {
        "choose": "🌐 Choose your language:",
        "home": (
            "🏋️ My Gym Bot\n\n"
            "We train 3 times a week 💪\n\n"
            "Choose a day:"
        ),
        "day1": "📅 DAY 1",
        "day2": "📅 DAY 2",
        "day3": "📅 DAY 3",
        "progress": "📊 PROGRESS",
        "reset": "🔄 RESET WEEK",
        "back_home": "⬅️ Main menu",
        "back": "⬅️ Back",
        "choose_exercise": "Choose an exercise:",
        "video": "▶️ YouTube VIDEO",
        "add_video": "➕ ADD VIDEO",
        "change_video": "🔄 CHANGE VIDEO",
        "program": "📋 Program",
        "video_saved": "✅ Video saved!",
        "send_video": "Send the YouTube video link:",
        "not_youtube": (
            "❌ This doesn't look like a YouTube link.\n\n"
            "Send a YouTube link."
        ),
        "cancel": "❌ Cancel",
        "progress_text": (
            "📊 PROGRESS\n\n"
            "We'll add this section later 💪"
        ),
        "reset_text": (
            "🔄 RESET WEEK\n\n"
            "We'll add this function later."
        ),
    }
}


# =========================
# LANGUAGE FUNCTIONS
# =========================

def get_lang(context):
    return context.user_data.get("language", "kk")


def t(context, key):
    lang = get_lang(context)
    return LANGUAGES[lang][key]


def language_menu():
    keyboard = [
        [
            InlineKeyboardButton(
                "🇰🇿 Қазақша",
                callback_data="lang_kk"
            ),
            InlineKeyboardButton(
                "🇷🇺 Русский",
                callback_data="lang_ru"
            ),
            InlineKeyboardButton(
                "🇬🇧 English",
                callback_data="lang_en"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================
# MAIN MENU
# =========================

def main_menu(context):

    keyboard = [
        [
            InlineKeyboardButton(
                t(context, "day1"),
                callback_data="day_1"
            )
        ],
        [
            InlineKeyboardButton(
                t(context, "day2"),
                callback_data="day_2"
            )
        ],
        [
            InlineKeyboardButton(
                t(context, "day3"),
                callback_data="day_3"
            )
        ],
        [
            InlineKeyboardButton(
                t(context, "progress"),
                callback_data="progress"
            )
        ],
        [
            InlineKeyboardButton(
                t(context, "reset"),
                callback_data="reset"
            )
        ],
        [
            InlineKeyboardButton(
                "🌐 Тіл / Language",
                callback_data="language"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if "language" not in context.user_data:

        await update.message.reply_text(
            "🌐 Тілді таңдаңыз / "
            "Выберите язык / "
            "Choose your language:",
            reply_markup=language_menu()
        )

        return

    await update.message.reply_text(
        t(context, "home"),
        reply_markup=main_menu(context)
    )


# =========================
# GET EXERCISES
# =========================

def get_exercises(day):

    if day == 1:
        return DAY_1_EXERCISES

    if day == 2:
        return DAY_2_EXERCISES

    return DAY_3_EXERCISES


# =========================
# DAY TITLES
# =========================

DAY_TITLES = {

    "kk": {
        1: "Кеуде + Иық + Трицепс",
        2: "Арқа + Бицепс + Артқы иық",
        3: "Аяқ + Кеуде + Иық + Қол"
    },

    "ru": {
        1: "Грудь + Плечи + Трицепс",
        2: "Спина + Бицепс + Задняя дельта",
        3: "Ноги + Грудь + Плечи + Руки"
    },

    "en": {
        1: "Chest + Shoulders + Triceps",
        2: "Back + Biceps + Rear Delts",
        3: "Legs + Chest + Shoulders + Arms"
    }
}


# =========================
# SHOW DAY
# =========================

async def show_day(query, context, day):

    exercises = get_exercises(day)

    user_id = query.from_user.id

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    keyboard = []

    for exercise_id, exercise in exercises.items():

        cursor.execute("""
            SELECT url
            FROM videos
            WHERE user_id = ?
            AND day = ?
            AND exercise_id = ?
        """, (
            user_id,
            day,
            exercise_id
        ))

        result = cursor.fetchone()

        if result:
            button_text = f"▶️ {exercise[0]}"
        else:
            button_text = f"➕ {exercise[0]}"

        keyboard.append([
            InlineKeyboardButton(
                button_text,
                callback_data=f"exercise_{day}_{exercise_id}"
            )
        ])

    conn.close()

    keyboard.append([
        InlineKeyboardButton(
            t(context, "back_home"),
            callback_data="home"
        )
    ])

    lang = get_lang(context)

    await query.edit_message_text(
        f"📅 {day}-КҮН\n\n"
        f"{DAY_TITLES[lang][day]}\n\n"
        f"{t(context, 'choose_exercise')}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================
# SHOW EXERCISE
# =========================

async def show_exercise(
    query,
    context,
    day,
    exercise_id
):

    exercises = get_exercises(day)

    name, sets_text = exercises[exercise_id]

    user_id = query.from_user.id

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT url
        FROM videos
        WHERE user_id = ?
        AND day = ?
        AND exercise_id = ?
    """, (
        user_id,
        day,
        exercise_id
    ))

    video = cursor.fetchone()

    conn.close()

    keyboard = []

    if video:

        keyboard.append([
            InlineKeyboardButton(
                t(context, "video"),
                url=video[0]
            )
        ])

        keyboard.append([
            InlineKeyboardButton(
                t(context, "change_video"),
                callback_data=f"addvideo_{day}_{exercise_id}"
            )
        ])

    else:

        keyboard.append([
            InlineKeyboardButton(
                t(context, "add_video"),
                callback_data=f"addvideo_{day}_{exercise_id}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            t(context, "back"),
            callback_data=f"day_{day}"
        )
    ])

    await query.edit_message_text(
        f"🏋️ {name}\n\n"
        f"{t(context, 'program')}: {sets_text}\n\n"
        "🎥",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================
# ASK FOR VIDEO
# =========================

async def ask_video(
    query,
    context,
    day,
    exercise_id
):

    exercises = get_exercises(day)

    name, sets_text = exercises[exercise_id]

    context.user_data["adding_video"] = {
        "day": day,
        "exercise_id": exercise_id
    }

    await query.edit_message_text(
        f"🎥 {name}\n\n"
        f"{t(context, 'program')}: {sets_text}\n\n"
        f"{t(context, 'send_video')}\n\n"
        "Мысал / Example:\n"
        "https://www.youtube.com/watch?v=XXXXXXXX",

        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    t(context, "cancel"),
                    callback_data=f"day_{day}"
                )
            ]
        ])
    )


# =========================
# RECEIVE VIDEO LINK
# =========================

async def receive_video_link(update, context):

    if "adding_video" not in context.user_data:
        return

    url = update.message.text.strip()

    if (
        "youtube.com" not in url
        and "youtu.be" not in url
    ):

        await update.message.reply_text(
            t(context, "not_youtube")
        )

        return

    info = context.user_data["adding_video"]

    user_id = update.effective_user.id

    day = info["day"]

    exercise_id = info["exercise_id"]

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO videos
        (user_id, day, exercise_id, url)
        VALUES (?, ?, ?, ?)
    """, (
        user_id,
        day,
        exercise_id,
        url
    ))

    conn.commit()
    conn.close()

    del context.user_data["adding_video"]

    exercises = get_exercises(day)

    name = exercises[exercise_id][0]

    await update.message.reply_text(
        f"{t(context, 'video_saved')}\n\n"
        f"🏋️ {name}"
    )


# =========================
# BUTTON HANDLER
# =========================

async def button_handler(update, context):

    query = update.callback_query

    await query.answer()

    data = query.data

    # LANGUAGE
    if data.startswith("lang_"):

        lang = data.split("_")[1]

        context.user_data["language"] = lang

        await query.edit_message_text(
            t(context, "home"),
            reply_markup=main_menu(context)
        )

        return

    # LANGUAGE MENU
    if data == "language":

        await query.edit_message_text(
            "🌐 Тілді таңдаңыз / "
            "Выберите язык / "
            "Choose your language:",

            reply_markup=language_menu()
        )

        return

    # HOME
    if data == "home":

        await query.edit_message_text(
            t(context, "home"),
            reply_markup=main_menu(context)
        )

        return

    # DAY
    if data.startswith("day_"):

        day = int(
            data.split("_")[1]
        )

        await show_day(
            query,
            context,
            day
        )

        return

    # EXERCISE
    if data.startswith("exercise_"):

        parts = data.split("_")

        day = int(parts[1])

        exercise_id = parts[2]

        await show_exercise(
            query,
            context,
            day,
            exercise_id
        )

        return

    # ADD VIDEO
    if data.startswith("addvideo_"):

        parts = data.split("_")

        day = int(parts[1])

        exercise_id = parts[2]

        await ask_video(
            query,
            context,
            day,
            exercise_id
        )

        return

    # PROGRESS
    if data == "progress":

        await query.edit_message_text(
            t(context, "progress_text"),

            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t(context, "back_home"),
                        callback_data="home"
                    )
                ]
            ])
        )

        return

    # RESET
    if data == "reset":

        await query.edit_message_text(
            t(context, "reset_text"),

            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t(context, "back_home"),
                        callback_data="home"
                    )
                ]
            ])
        )

        return


# =========================
# MAIN
# =========================

def main():

    init_db()

    if not TOKEN:
        print("❌ BOT_TOKEN табылмады!")
        print("❌ PyCharm ішінде BOT_TOKEN орнатылуы керек.")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            receive_video_link
        )
    )

    print("🤖 Gym Bot іске қосылды!")

    app.run_polling()


# =========================
# RUN
# =========================

if __name__ == "__main__":
    main()