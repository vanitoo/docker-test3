from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.exceptions import ChatNotFound, BadRequest

# Ваш токен и группа
API_TOKEN = '6931242232:AAFR4mUpA-cPqrsF4Wzxntpo9ZLmeYhRKoE'
GROUP_ID = 'ayavmoskve'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


# Клавиатура с кнопками
def subscribe_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    subscribe_button = InlineKeyboardButton(text="Подписаться на группу", url=f"https://t.me/{GROUP_ID}")
    check_button = InlineKeyboardButton(text="Проверить", callback_data="check_subscription")
    keyboard.add(subscribe_button, check_button)
    return keyboard


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Для продолжения, пожалуйста, подпишитесь на нашу группу и нажмите 'Проверить'.",
                         reply_markup=subscribe_keyboard())


# Обработчик нажатия на кнопку "Проверить"
@dp.callback_query_handler(lambda c: c.data == 'check_subscription')
async def process_callback_button(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    try:
        # Проверка, является ли пользователь подписчиком группы
        member = await bot.get_chat_member(chat_id='@'+GROUP_ID, user_id=user_id)

        if member.status in ['member', 'administrator', 'creator']:
            await bot.answer_callback_query(callback_query.id, "Вы успешно подписаны на группу!")
            await bot.send_message(callback_query.from_user.id, "Спасибо за подписку! Продолжаем...")
            # Здесь можно продолжить выполнение других действий
        else:
            await bot.answer_callback_query(callback_query.id, "Вы еще не подписались на группу.")
    except ChatNotFound:
        await bot.answer_callback_query(callback_query.id, "Не удалось найти группу. Проверьте правильность GROUP_ID.")
    except BadRequest:
        await bot.answer_callback_query(callback_query.id, "Ошибка при проверке подписки. Попробуйте позже.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
