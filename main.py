import asyncio
import base64
import os

import aiogram.contrib.fsm_storage.memory
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
import pymysql
pymysql.install_as_MySQLdb()

# Установите параметры подключения к базе данных
host = '31.31.196.165'
port = 3306
username = 'u2333338_root'
password = 'Y3S4G9taZvwsYtU2@'
database = 'u2333338_some'

conn = pymysql.connect(host=host, user=username, password=password, db=database)
# Соединение с базой данных


# Создаем объекты бота и диспетчера
bot = Bot(token="6893517321:AAFdChT70-yFPIpBejKo_cpnJUwwRxsaSx4")
dp = Dispatcher(bot, storage=aiogram.contrib.fsm_storage.memory.MemoryStorage())


class DeviceInput(StatesGroup):
    id = State()
    name = State()
    price = State()
    quantity = State()
    size = State()
    power = State()
    hashing = State()
    algorithm = State()
    coin = State()
    image = State()
    manufacturer = State()
    offer_type = State()


class DeviceDelete(StatesGroup):
    id = State()


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton(text="Добавить девайс", callback_data="add_device"),
        types.InlineKeyboardButton(text="Удалить девайс", callback_data="remove_device")
    ]
    keyboard.add(*buttons)
    await message.answer("Выберите действие:", reply_markup=keyboard)


# Обработчик кнопки "Добавить девайс"
@dp.callback_query_handler(text='add_device')
async def add_device(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Привет! Чтобы добавить девайс, введите следующие данные по "
                                                        "очереди.\n\n 1. Введите айди девайса:")
    await DeviceInput.id.set()


@dp.callback_query_handler(text='remove_device')
async def remove_device(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите айди удаляемого девайса:")

    await DeviceDelete.id.set()


@dp.message_handler(state=DeviceDelete.id)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.text

    await message.reply('готово')


@dp.message_handler(state=DeviceInput.id)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.text

    await message.reply('2. Введите имя девайса:')
    await DeviceInput.name.set()


@dp.message_handler(state=DeviceInput.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await message.reply('3. Введите цену:')
    await DeviceInput.price.set()


@dp.message_handler(state=DeviceInput.price)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await message.reply('4. Введите количество:')
    await DeviceInput.quantity.set()


@dp.message_handler(state=DeviceInput.quantity)
async def process_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['quantity'] = message.text

    await message.reply('5. Введите размер:')
    await DeviceInput.size.set()


@dp.message_handler(state=DeviceInput.size)
async def process_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await message.reply('6. Введите мощность:')
    await DeviceInput.power.set()


@dp.message_handler(state=DeviceInput.power)
async def process_power(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['power'] = message.text

    await message.reply('7. Введите алгоритм:')
    await DeviceInput.algorithm.set()


@dp.message_handler(state=DeviceInput.algorithm)
async def process_algorithm(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['algorithm'] = message.text

    await message.reply('8. Введите хэширование:')
    await DeviceInput.hashing.set()


@dp.message_handler(state=DeviceInput.hashing)
async def process_hashing(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['hashing'] = message.text

    await message.reply('9. Введите монету:')

    async with conn.send() as cursor:
        sql = "SELECT id, name from coins"
        cursor.execute(sql)
        coins = cursor.fetchall()
        print(coins)
        # Проверка наличия монет
        if len(coins) == 0:
            await message.reply('Монеты не найдены. Пожалуйста, создайте монеты.')
            return
        # Переход к следующему состоянию
        await message.reply(coins)

    DeviceInput.coin.set()


@dp.message_handler(state=DeviceInput.coin)
async def process_coin(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['coin'] = message.text

    await message.reply('10. Загрузите изображение:')
    await DeviceInput.image.set()


@dp.message_handler(state=DeviceInput.image,
                    content_types=types.ContentTypes.PHOTO)  # Укажите content_types для ограничения типов загружаемого содержимого
async def process_image(message: types.Message, state: FSMContext):
    # Сохраните изображение во временный файл
    photo = message.photo[-1]  # Выберите самое большое изображение из отправленных
    photo_path = f"{photo.file_id}.jpg"  # Задайте путь для сохранения файла
    await photo.download(photo_path)  # Сохраните изображение в файл

    # Прочитайте изображение из файла и преобразуйте его в базовую строку
    with open(photo_path, "rb") as file:
        image_data = file.read()
        base64_data = base64.b64encode(image_data).decode("utf-8")

    # Удалите временный файл
    os.remove(photo_path)

    async with state.proxy() as data:
        data['image'] = base64_data

    await message.reply('11. Введите производителя:')
    await DeviceInput.manufacturer.set()


@dp.message_handler(state=DeviceInput.manufacturer)
async def process_manufacturer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['manufacturer'] = message.text

    await message.reply('12. Введите тип предложения:')
    await DeviceInput.offer_type.set()


@dp.message_handler(state=DeviceInput.offer_type)
async def process_offer_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['offer_type'] = message.text

    # Здесь вы можете продолжить с дополнительными шагами обработки данных

    await message.reply('Ввод данных завершен!')
    print(data['image'])
    await state.finish()


# async def insert_into_database(data):
#     try:
#         conn = await aiomysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)
#         async with conn.cursor() as cursor:
#             sql = "INSERT INTO devices (device_id, quantity, size, power, algorithm, hashing, coin, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
#             await cursor.execute(sql, data)
#             await conn.commit()
#     finally:
#         conn.close()


# Запуск бота
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(dp.start_polling())
    finally:
        loop.run_until_complete(dp.bot.close())
        loop.close()
