
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import logging
import asyncio
import aioschedule as schedule
from config import token
from datetime import datetime
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import sqlite3

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher()

conn = sqlite3.connect('schedule.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS schedule (
    user_id INTEGER PRIMARY KEY,
    time TEXT NOT NULL
)
""")
conn.commit()

async def send_reminder():
    now = datetime.now().strftime('%H:%M')
    cursor.execute('SELECT user_id FROM schedule WHERE time = ?', (now,))
    users = cursor.fetchall()
    
    for user in users:
        await bot.send_message(user[0], "Пора выполнить задачу!")

async def scheduler():
    schedule.every().minute.do(send_reminder)
    while True:
        await asyncio.sleep(1)
        await schedule.run_pending()

@dp.message(Command('start'))
async def start(message: types.Message):
    user_id = message.from_user.id
    cursor.execute('INSERT OR IGNORE INTO schedule (user_id, time) VALUES (?, ?)', (user_id, '19:10'))
    conn.commit()
    await message.answer(
        "Привет! Я помогу тебе планировать задачи. Используй /set_schedule <время>, чтобы установить время для уведомлений."
    )

@dp.message(Command('set_schedule'))
async def set_schedule(message: types.Message):
    try:
        time_str = message.text.split()[1]
        datetime.strptime(time_str, '%H:%M')
        user_id = message.from_user.id
        cursor.execute('INSERT OR REPLACE INTO schedule (user_id, time) VALUES (?, ?)', (user_id, time_str))
        conn.commit()
        await message.answer(f"Уведомление будет отправлено в {time_str}.")
    except (IndexError, ValueError):
        await message.answer("Неверный формат. Используйте /set_schedule <время> в формате HH:MM.")

@dp.message(Command('view_schedule'))
async def view_schedule(message: types.Message):
    user_id = message.from_user.id
    cursor.execute('SELECT time FROM schedule WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    if result:
        await message.answer(f"Ваше текущее расписание: {result[0]}")
    else:
        await message.answer("У вас нет установленного расписания.")

@dp.message(Command('delete_schedule'))
async def delete_schedule(message: types.Message):
    try:
        user_id = message.from_user.id
        cursor.execute('DELETE FROM schedule WHERE user_id = ?', (user_id,))
        conn.commit()
        await message.answer("Ваше расписание удалено.")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

@dp.message(Command('update_schedule'))
async def update_schedule(message: types.Message):
    try:
        old_time, new_time = message.text.split()[1:3]
        datetime.strptime(new_time, '%H:%M')
        user_id = message.from_user.id
        cursor.execute(
            'UPDATE schedule SET time = ? WHERE user_id = ? AND time = ?',
            (new_time, user_id, old_time)
        )
        conn.commit()
        await message.answer(f"Уведомление изменено с {old_time} на {new_time}.")
    except (IndexError, ValueError):
        await message.answer("Неверный формат. Используйте /update_schedule <старое_время> <новое_время>.")

async def main():
    asyncio.create_task(scheduler())
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main()) 