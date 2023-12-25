import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, order_info
from aiogram.utils import executor
from sqlalchemy import create_engine, Column, String, Integer, LargeBinary, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from button import main_rp

API_TOKEN = "6866448291:AAGNY-57pLY586PNoUphIQXh5GSkiqVqdGo"
from aiogram.dispatcher.filters.state import StatesGroup, State

bot = Bot(API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

storage = MemoryStorage()
dp.storage = storage
DATABASE_URL = 'sqlite:///food.db'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    food_name = Column(String)
    # Other columns for order details


class FoodItem(Base):
    __tablename__ = 'food_item'

    id = Column(Integer, primary_key=True)
    food_picture = Column(LargeBinary)
    food_name = Column(String)
    count = Column(Integer)
    amount = Column(Integer)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class Form(StatesGroup):
    food_name = State()
    fullname = State()
    count = State()
    phone_number = State()
    address = State()


class Forms(StatesGroup):
    food_picture = State()
    food_name = State()
    count = State()
    amount = State()


class Food(StatesGroup):
    food_name = State()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def order_keyboard():
    # Creating an order keyboard
    ikm = InlineKeyboardMarkup()
    ikm.add(InlineKeyboardButton('Order Food', callback_data='order_start'))
    return ikm


keyboard = types.InlineKeyboardMarkup()
keyboard.add(types.InlineKeyboardButton('Yes', callback_data='confirm_order'),
             types.InlineKeyboardButton('No', callback_data='cancel_order'))


def order_keyboart():
    # Creating an order keyboard
    ikm = InlineKeyboardMarkup()
    ikm.add(InlineKeyboardButton("delete", callback_data='delete'))
    return ikm


def food_delete():
    # Creating an order keyboard
    ikm = InlineKeyboardMarkup()
    ikm.add(InlineKeyboardButton("delete", callback_data='delete_id'))
    return ikm


# async def bekor_qilish():
#     # Creating an order keyboard
#     ikm = InlineKeyboardMarkup()
#     ikm.add(InlineKeyboardButton('Order Food', callback_data='order_start'))
#     ikm.add(InlineKeyboardButton('Cancel Order', callback_data='cancel_order'))
#     return ikm


async def fetch_and_send_info(message: types.Message):
    # Fetch data from the database
    db = Session()
    food_items = db.query(FoodItem).all()
    db.close()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Create KeyboardButtons for each food item in the database
    for food_item in food_items:
        button_text = f"Food: {food_item.food_name}"
        keyboard.add(types.KeyboardButton(text=button_text))

    # Send the keyboard with food information to the user
    await bot.send_message(chat_id=message.chat.id, text="Available Foods:", reply_markup=keyboard)


async def hamma_ovqatlar(message: types.Message):
    # Fetch data from the database
    db = Session()
    food_items = db.query(FoodItem).all()
    db.close()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Create KeyboardButtons for each food item in the database
    for food_item in food_items:
        button_text = f"Food: {food_item.food_name}"
        keyboard.add(types.KeyboardButton(text=button_text))

    # Send the keyboard with food information to the user
    await bot.send_message(chat_id=message.chat.id, text="Available Foods:", reply_markup=keyboard)


@dp.message_handler(
    lambda message: any(food_item.food_name in message.text for food_item in Session().query(FoodItem).all()))
async def show_food_details(message: types.Message):
    db = Session()
    selected_food_name = next(
        (food_item.food_name for food_item in db.query(FoodItem).all() if food_item.food_name in message.text), None)
    if message.from_user.id != 1372665869 and message.from_user.id != 1327286056 and message.from_user.id != 5772722670:
        if selected_food_name:
            try:
                # Fetch details of the selected food item from the database
                selected_food_item = db.query(FoodItem).filter(FoodItem.food_name == selected_food_name).first()

                # Prepare and send details to the user
                photo = selected_food_item.food_picture
                details_text = f"Food Name: {selected_food_item.food_name}\nCount: {selected_food_item.count}\nAmount: {selected_food_item.amount}"
                await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=details_text,
                                     reply_markup=order_keyboard(), )
            finally:
                db.close()
    else:
        if selected_food_name:
            try:
                # Fetch details of the selected food item from the database
                selected_food_item = db.query(FoodItem).filter(FoodItem.food_name == selected_food_name).first()

                # Prepare and send details to the user
                photo = selected_food_item.food_picture
                details_text = f"Food id : {selected_food_item.id} Food Name: {selected_food_item.food_name}\nCount: {selected_food_item.count}\nAmount: {selected_food_item.amount}"
                await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=details_text,
                                     reply_markup=food_delete())
            finally:
                db.close()


@dp.message_handler(commands=['start'])
async def start_order(message: types.Message):
    if message.from_user.id == 1327286056 or message.from_user.id == 5772722670:
        await message.answer("hello admin", reply_markup=main_rp)
    else:
        await fetch_and_send_info(message)


@dp.callback_query_handler(lambda query: query.data == 'order_start', state="*")
async def process_order(query: types.CallbackQuery):
    await query.answer()
    await bot.send_message(query.from_user.id, "Please enter the food name:")
    await Form.food_name.set()


@dp.message_handler(state=Form.food_name)
async def process_food_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        food_name = message.text

        # Query the database to check if the food_name exists
        db = SessionLocal()
        db_food = db.query(FoodItem).filter(FoodItem.food_name == food_name).first()
        db.close()
        if db_food:
            data['food_name'] = str((food_name))
            await Form.next()
            await message.answer("Please enter your full name:")
        else:
            await message.answer("This food item is unavailable. Please choose another:")


@dp.message_handler(state=Form.fullname)
async def process_fullname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fullname'] = message.text
    await Form.next()
    await message.answer("Please enter the count:")


@dp.message_handler(state=Form.count)
async def process_count(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        count = int(message.text)

        # Fetch the selected food item from the database
        selected_food_name = data.get('food_name')  # Assuming 'food_name' is stored in the state
        db = Session()
        selected_food_item = db.query(FoodItem).filter(FoodItem.food_name == selected_food_name).first()
        db.close()

        if selected_food_item:
            # Check if the entered count is less than or equal to the available quantity
            if count <= selected_food_item.count:
                data['count'] = count
                await Form.next()
                await message.answer("Please enter your phone number:")
            else:
                await message.answer("The entered count exceeds the available quantity. Please enter a valid count.")
        else:
            await message.answer("Failed to fetch food item information. Please try again.")

        # You might want to handle error cases or empty responses for the food item query accordingly


@dp.message_handler(state=Form.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text
    await Form.next()
    await message.answer("Finally, enter your address:")


@dp.message_handler(state=Form.address)
async def process_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text

        # Compile order information
        order_info = (
            f"Food Name: {data['food_name']}\n"
            f"Full Name: {data['fullname']}\n"
            f"Count: {data['count']}\n"
            f"Phone Number: {data['phone_number']}\n"
            f"Address: {data['address']}"
        )

        # await message.answer(order_info, reply_markup=keyboard)

        # Send order information to admin (replace ADMIN_TELEGRAM_ID with the actual ID)
        admin_id = '5772722670'
        await bot.send_message(admin_id, f"New Order:\n\n{order_info}", reply_markup=order_keyboart()
                               )

        await message.answer("Your order has been placed! Thank you.")

        # Reset state
        await state.finish()


@dp.message_handler(lambda message: message.text == "Ovqat qo'shish")
async def start_food_registration(message: types.Message):
    await message.answer("Please send the food picture.")
    await Forms.food_picture.set()


@dp.message_handler(content_types=types.ContentType.PHOTO, state=Forms.food_picture)
async def process_food_picture(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    async with state.proxy() as data:
        data['food_picture'] = photo_id

    await Forms.next()
    await message.answer("Please enter the food name:")


@dp.message_handler(state=Forms.food_name)
async def process_food_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['food_name'] = message.text

    await Forms.next()
    await message.answer("Please enter the count:")


@dp.message_handler(state=Forms.count)
async def process_count(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['count'] = message.text

    await Forms.next()
    await message.answer("Please enter the amount:")


@dp.message_handler(state=Forms.amount)
async def process_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text

        # Download the image file
        file_id = data['food_picture']
        file = await bot.get_file(file_id)
        downloaded_file = await bot.download_file(file.file_path)

        db = Session()
        food = FoodItem(
            food_picture=downloaded_file.read(),  # Save the image data as binary
            food_name=data['food_name'],
            count=data['count'],
            amount=data['amount']
        )
        db.add(food)
        db.commit()

        # Update the count in the database
        # selected_food_name = data.get('food_name')
        # selected_food_item = db.query(FoodItem).filter(FoodItem.food_name == selected_food_name).first()
        # if selected_food_item:
        #     selected_food_item.count -= int(data['count'])
        #     db.commit()
        # db.close()

        await state.finish()
        await message.answer(
            f"Food item '{data['food_name']}' with count {data['count']} and amount {data['amount']} has been added to the database."
        )
        await message.answer("Your order has been placed! Thank you.")


session = Session()


@dp.message_handler(lambda message: message.text == "Ovqatlarni ko'rish")
async def start_food_registration(message: types.Message):
    db = Session()
    food_items = db.query(FoodItem).all()
    db.close()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Create KeyboardButtons for each food item in the database
    for food_item in food_items:
        button_text = f"Food: {food_item.food_name}"
        keyboard.add(types.KeyboardButton(text=button_text))

    # Send the keyboard with food information to the user
    await bot.send_message(chat_id=message.chat.id, text="Available Foods:", reply_markup=keyboard)


@dp.callback_query_handler(lambda query: query.data.startswith('delete'))
async def delete_food_button_callback(query: types.CallbackQuery):
    food_id = query.data.split('id')

    try:
        existing_food = session.query(FoodItem).filter(FoodItem.id == food_id).first()
        if existing_food:
            session.delete(existing_food)
            session.commit()
            await bot.answer_callback_query(query.id, text=f"Food ID '{food_id}' has been deleted.")
            await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
        else:
            await bot.answer_callback_query(query.id, text=f"Food ID '{food_id}' not found.")
    except Exception as e:
        print(f"Exception occurred: {e}")
        await bot.answer_callback_query(query.id, text=f"Error deleting food ID '{food_id}'. Please try again.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
