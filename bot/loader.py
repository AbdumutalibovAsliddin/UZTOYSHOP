from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
import threading
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
try:
    from bot.data import config
except:
    from data import config


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
#MESSAGE SELLER
async def send_message_to_seller(chat_id: int, text: str,order_id:int):
    keyboard = InlineKeyboardMarkup(row_width=2)
    accept_button = InlineKeyboardButton("Qabul Qilish✅", callback_data=f"accept_order={order_id}")
    cancel_button = InlineKeyboardButton("Bekor Qilish❌", callback_data=f"cancel_order={order_id}")
    
    # Tugmalarni qo'shish
    btn = keyboard.add(accept_button, cancel_button)
    await bot.send_message(chat_id=chat_id, text=text,reply_markup=btn)

def notify_seller(chat_id: int, text: str,order_id:int):
    global loop  # Global o'zgaruvchini ishlatish

    if not loop.is_running():
        threading.Thread(target=loop.run_forever).start()

    asyncio.run_coroutine_threadsafe(send_message_to_seller(chat_id, text,order_id), loop)