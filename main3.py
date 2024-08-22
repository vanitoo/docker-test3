from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
import asyncio

API_TOKEN = '6931242232:AAFR4mUpA-cPqrsF4Wzxntpo9ZLmeYhRKoE'
GROUP_ID = 'ayavmoskve'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Определение состояний
class Quiz(StatesGroup):
    waiting_for_goal = State()
    waiting_for_problem = State()


# Клавиатура с кнопками
def subscribe_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    subscribe_button = InlineKeyboardButton(text="Подписаться на группу", url=f"https://t.me/{GROUP_ID}")
    check_button = InlineKeyboardButton(text="Проверить подписку", callback_data="check_subscription")
    keyboard.add(subscribe_button, check_button)
    return keyboard


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! Я рад, что ты заинтересовался нашим курсом по личностному росту. Чтобы получить доступ к первому уроку, подпишись на наш Telegram-канал.",
        reply_markup=subscribe_keyboard())


# Обработчик нажатия на кнопку "Проверить"
@dp.callback_query_handler(lambda c: c.data == 'check_subscription')
async def process_callback_button(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    try:
        member = await bot.get_chat_member(chat_id='@'+GROUP_ID, user_id=user_id)

        if member.status in ['member', 'administrator', 'creator']:
            await bot.answer_callback_query(callback_query.id, "Вы успешно подписаны на группу!")
            await bot.send_message(callback_query.from_user.id,
                                   "Спасибо за подписку! Давайте начнем с небольшого опроса, чтобы лучше понять ваши цели.")
            await bot.send_message(callback_query.from_user.id,
                                   "Какая ваша главная цель на данный момент? (Например, улучшить карьеру, повысить мотивацию, найти баланс между работой и жизнью)")
            await Quiz.waiting_for_goal.set()
        else:
            await bot.answer_callback_query(callback_query.id, "Вы еще не подписались на группу.")
    except Exception as e:
        await bot.answer_callback_query(callback_query.id, f"Ошибка: {str(e)}")


# Опрос пользователя - цель
@dp.message_handler(state=Quiz.waiting_for_goal)
async def process_goal(message: types.Message, state: FSMContext):
    user_goal = message.text
    await state.update_data(goal=user_goal)

    await message.answer(
        "Спасибо! Теперь расскажите, какую главную проблему вы хотите решить с помощью коучинга? (Например, низкая самооценка, прокрастинация, нехватка времени и т.д.)")
    await Quiz.waiting_for_problem.set()


# Опрос пользователя - проблема
@dp.message_handler(state=Quiz.waiting_for_problem)
async def process_problem(message: types.Message, state: FSMContext):
    user_problem = message.text
    user_data = await state.get_data()

    user_goal = user_data.get('goal')

    await message.answer(f"Отлично! Ваша цель - {user_goal}, а проблема, которую вы хотите решить - {user_problem}.")
    await message.answer(
        "Чтобы помочь вам, вот бесплатный видеоурок, который поможет вам начать решать вашу проблему. [Ссылка на видео]")

    # Предложение участия в вебинаре или консультации
    await message.answer(
        "Хотите пойти дальше? Присоединяйтесь к нашему вебинару, где мы глубже разберем вашу проблему и предложим работающие решения. Зарегистрируйтесь по ссылке!")

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
