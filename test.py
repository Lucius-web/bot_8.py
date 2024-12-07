from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
import asyncio
from aiogram import types
import keyboard as kb


from config import token

bot = Bot(token=token)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Приветствую вас {message.from_user.first_name}!\nЯ ваш бот проводник, если хотите узнать какую либо информацию то она имеется у вас в области клавиатуры и удачи в познании мира программирования!', reply_markup=kb.main)


@dp.message(F.text == 'О нас')
async def about(message: Message):
    await message.answer('Мы создаем экосистему для обучения, работы и творчества IT-специалистов История создания Международная IT-академия Geeks (Гикс) был основан Fullstack-разработчиком Айдаром Бакировым и Android-разработчиком Нургазы Сулаймановым в 2018-ом году в Бишкеке с целью дать возможность каждому человеку, даже без опыта в технологиях, гарантированно освоить IT-профессию. На сегодняшний день более 1200 студентов в возрасте от 12 до 45 лет изучают здесь самые популярные и востребованные IT-профессии. Филиальная сеть образовательного центра представлена в таких городах, как Бишкек, Ош, Ташкент и Кара-Балта.')
    
@dp.message(F.text == 'Направления')
async def direction(message: Message):
    await message.answer('У нас имеются 3 направление по кнопкам ниже', reply_markup=kb.setting)
    
@dp.message(F.text == 'Контакты')
async def contacts(message: Message):
    await message.answer('@geeks_osh\n+996 559 006484\nБексултан Сулайманов')
    
@dp.callback_query(F.data == 'Lining_info')
async def backend_info(query):
    await query.message.answer('''это внутренняя часть сайта и т.д. 
Стоимость: 12000 сом в месяц. 
Обучение: 5 месяц''')
@dp.callback_query(F.data == 'Nike_info')
async def frontend_info(query):
    await query.message.answer('''это внешняя часть сайта и т.д.
    Стоимость: 12000 сом в месяц. 
    Обучение: 5 месяц''')

@dp.callback_query(F.data == 'Sajda_info')
async def ux_ui_info(query):
    await query.message.answer('''это дизайнерская часть сайта и т.д.
    Стоимость: 12000 сом в месяц. 
Обучение: 4 месяц''')

async def main():
    await dp.start_polling(bot)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Вы отключились от бота!")


