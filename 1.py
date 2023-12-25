# from aiogram import Bot, Dispatcher, types
# from aiogram.contrib.middlewares.logging import LoggingMiddleware
# from aiogram.utils import executor
#
# API_TOKEN = "6866448291:AAGNY-57pLY586PNoUphIQXh5GSkiqVqdGo"
#
# bot = Bot(API_TOKEN)
# dp = Dispatcher(bot)
# dp.middleware.setup(LoggingMiddleware())
#
#
# async def send_info_to_admin(chat_id):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     products =
#     for product in products:
#         food_name = product['food_name']
#         count = product['count']
#         amount = product['amount']
#
#         button_text = f"Food: {food_name}"
#         keyboard.add(types.KeyboardButton(text=button_text))
#
#     await bot.send_message(chat_id=chat_id, text="New order information:", reply_markup=keyboard)
#
#
# # Add a handler for the /start command to trigger the function
# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     chat_id = message.chat.id  # Get the chat ID from the received message
#     products_list = [
#         {'food_name': 'Food 1', 'count': 5, 'amount': 20},
#         {'food_name': 'Food 2', 'count': 3, 'amount': 15},
#         # Add more products as needed
#     ]
#     await send_info_to_admin(chat_id, products_list)
#
#
# @dp.message_handler(lambda message: message.text.startswith('Food: '))
# async def handle_food_button(message: types.Message):
#     # Extract the food name from the button text
#     food_name = message.text.replace('Food: ', '')
#
#     # Here, perform the action related to the specific food item based on its name
#     # Retrieve corresponding information or perform a specific task related to this food item
#
#     # Example: Send a message with the details of the selected food item
#     await bot.send_message(message.chat.id, f"Details for {food_name}: ...")  # Replace ... with relevant details
#
#
# # Start the bot
# executor.start_polling(dp, skip_updates=True)
