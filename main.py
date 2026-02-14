import asyncio
import sqlite3
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

# ================== SOZLAMALAR ==================

TOKEN = "6308074416:AAGKDEZ5ZEHXlVnHdunaupQl_cu-2Zad0Hs"
ADMIN_ID = 6579807924  # <-- O'zingni telegram ID yoz

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ================== DATABASE ==================

def connect_db():
    return sqlite3.connect("users.db")

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            username TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_user(user_id, username):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (user_id, username) VALUES (?, ?)",
            (user_id, username)
        )
        conn.commit()
    except:
        pass
    conn.close()

def get_users_count():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_all_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

# ================== KEYBOARD ==================

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📷 Rasm")],
        [KeyboardButton(text="ℹ️ Ma'lumot")]
    ],
    resize_keyboard=True
)

# ================== HANDLERS ==================

@dp.message(Command("start"))
async def start_handler(message: Message):
    add_user(message.from_user.id, message.from_user.username)
    await message.answer(
        "Botga xush kelibsiz 🚀",
        reply_markup=keyboard
    )

@dp.message(Command("users"))
async def users_handler(message: Message):
    if message.from_user.id == ADMIN_ID:
        count = get_users_count()
        await message.answer(f"Foydalanuvchilar soni: {count}")
    else:
        await message.answer("Siz admin emassiz ❌")

@dp.message(Command("broadcast"))
async def broadcast_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Siz admin emassiz ❌")
        return

    text = message.text.replace("/broadcast ", "")

    if text == "/broadcast":
        await message.answer("Foydalanish: /broadcast xabaringiz")
        return

    users = get_all_users()

    success = 0
    failed = 0

    for user in users:
        try:
            await bot.send_message(user[0], text)
            success += 1
        except:
            failed += 1

    await message.answer(
        f"Broadcast tugadi ✅\n\nYuborildi: {success}\nXato: {failed}"
    )

@dp.message()
async def menu_handler(message: Message):
    if message.text == "📷 Rasm":
        await message.answer_photo(
            photo="https://picsum.photos/500",
            caption="Tasodifiy rasm 📷"
        )
    elif message.text == "ℹ️ Ma'lumot":
        await message.answer(" Bu telegram bot")
    else:
        await message.answer("Tugmalardan foydalaning.")

# ================== MAIN ==================

async def main():
    create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
