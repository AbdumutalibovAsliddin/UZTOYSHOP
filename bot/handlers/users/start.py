import logging
from aiogram import types
from data.config import CHANNELS,WEB_URL
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton,ReplyKeyboardRemove
from loader import bot, dp
from utils.misc import subscription
from states.address import Address
from states.confirm import Accept, Cancel
from aiogram.dispatcher import FSMContext
from datetime import datetime,date
from keyboards.default.buttons import menu
import requests


def send_date_to_django(order_id, order_date):
    url = f'http://{WEB_URL}/cart/save_order_date/' 
    data = {
        'order_id': order_id,
        'order_date': order_date, 
    }

    # POST so'rovini yuborish
    response = requests.post(url, json=data)

    if response.status_code == 200:
        return "Sana muvaffaqiyatli saqlandi!"
    else:
        return "Xatolik yuz berdi!"
def send_location_request(address_code,longitude, latitude):
    # URL ni belgilaymiz
    url = f'http://{WEB_URL}/cart/update_address/{address_code}'  # O'zingizning API URL manzilingiz bilan almashtiring
    print(url)
    # Parametrlarni tayyorlaymiz
    params = {
        'longitude': longitude,
        'latitude': latitude
    }

    try:
        # GET so'rovini yuboramiz
        response = requests.get(url, params=params)

        # So'rov natijalarini tekshiramiz
        if response.status_code == 200:
            return True  # JSON formatida javobni chiqaramiz
        else:
            print(response.status_code)
            return False  # Xato haqida ma'lumot
    except requests.exceptions.RequestException as e:
        print("So'rovda xato:", e)
def send_reason(order_id, reason):
    url = f'http://{WEB_URL}/cart/order/cancel/' 
    data = {
        'order_id': order_id,
        'reason': reason, 
    }

    # POST so'rovini yuborish
    response = requests.post(url, json=data)

    if response.status_code == 200:
        return "Sana muvaffaqiyatli saqlandi!"
    else:
        return "Xatolik yuz berdi!"
@dp.message_handler(commands=['start'])
async def show_channels(message: types.Message, state: FSMContext):
    args = message.get_args()
    if args:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button_location = types.KeyboardButton(text="Joylashuvni jo'natish ✈️", request_location=True)
        button_cancel = types.KeyboardButton(text="Bekor qilish ❌")
        keyboard.add(button_location)
        keyboard.add(button_cancel)
        await message.reply("""📍 Hozirgi joylashuvingizni jo‘natish uchun pastdagi Jo‘natish tugmasini bosing.
📽 Agar boshqa joyni tanlamoqchi bo‘lsangiz, videoni ko‘rib chiqing va oson o‘rganing! ✨📦

📌✅🎬""",reply_markup=keyboard)
        await Address.address_code.set()
        await state.update_data(address_code=message.text)
        await Address.location.set()
    else:
        user = message.from_user.id
        final_status = True
        btn = InlineKeyboardMarkup(row_width=1)
        for channel in CHANNELS:
            status = await subscription.check(user_id=user,
                                            channel=channel)
            final_status *= status
            channel = await bot.get_chat(channel)
            if status:
                invite_link = await channel.export_invite_link()
                btn.add(InlineKeyboardButton(text=f"✅ {channel.title}", url=invite_link))
            if not status:
                invite_link = await channel.export_invite_link()
                btn.add(InlineKeyboardButton(text=f"❌ {channel.title}", url=invite_link))
        btn.add(InlineKeyboardButton(text="Obunani tekshirish", callback_data="check_subs"))
        if final_status:
            keyboard = InlineKeyboardMarkup()
            web_button = InlineKeyboardButton(text="Xaridni boshlash 🛍", web_app={"url":f"https://{WEB_URL}"})
            keyboard.add(web_button)
            text = f"""🎉 Xush kelibsiz, {message.from_user.full_name}!
Uz Toys Shop do'konimizga tashrif buyurganingiz uchun tashakkur!
Eng zo'r o'yinchoqlar va sovg'alar sizni kutmoqda!
📍 Manzil: Andijon shahar, Jaxon bozori

✨ Yangi mahsulotlar va chegirmalar uchun kuzatib boring!
🚚 Yetkazib berish narxi:

Andijon shahar uchun — bepul 🆓!

Boshqa joylarga zakaz berganingizdan keyin aloqaga chiqib, narxni aytib beramiz.


Agar yordam kerak bo'lsa, aloqa uchun @UzToysShop_Manager bilan bog'lanishingiz mumkin.

Sizni kutib qolamiz! 🚀

 Mahsulotlarni ko'rish uchun pastdagi tugmani bosing 👇🏼"""
            await message.answer(text,reply_markup=keyboard)
            await message.answer("Menu 🏠", reply_markup=menu)
        if not final_status:
            await message.answer("Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling!", disable_web_page_preview=True, reply_markup=btn)
@dp.message_handler(content_types=types.ContentTypes.LOCATION,state=Address.location)
async def location_handler(message: types.Message, state: FSMContext):
    latitude = message.location.latitude
    longitude = message.location.longitude
    data = await state.get_data()
    print(latitude,longitude,data.get('address_code'))
    error = send_location_request(data.get('address_code').replace("/start ", ""),longitude,latitude)
    if error:
        await message.reply(f"""📍 Manzil muvaffaqiyatli saqlandi!
💡 Sizning manzilingiz: <a href="https://www.google.com/maps/search/{latitude}+{longitude}">Manzilni Ko'rish</a>
✨ Endi quyidagilarni amalga oshirishingiz mumkin:
1️⃣ Web sahifaga qaytish: ✅ Tugmani bosing va ishni davom ettiring.
2️⃣ Web ilovani ochish: 📱 Web ilovaga o‘tib, barcha qulayliklardan foydalaning.

🔗 Web sahifaga qaytib barcha xizmatlardan foydalanishni davom ettirishni unutmang!
🚀 Web ilova orqali qulay va tez ishlash imkoniyatlarini kashf eting! 😊""",reply_markup=ReplyKeyboardRemove())
        await message.answer("Menu 🏠", reply_markup=menu)
    else:
        await message.reply(f"Nimadur xato ketdi ❌",reply_markup=ReplyKeyboardRemove())
    # State'ni tugatish
    await state.finish()
@dp.message_handler(lambda message: message.text == "Bekor qilish ❌",content_types=types.ContentTypes.TEXT,state=Address.location)
async def send_support_info(message: types.Message, state: FSMContext):
    await message.answer("Lokatsiya bekor qilindi", reply_markup=menu)
    await state.finish()
@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    await call.answer()
    result = str()
    btn = InlineKeyboardMarkup()
    final_status = True
    for channel in CHANNELS:
        status = await subscription.check(user_id=call.from_user.id,
                                          channel=channel)
        final_status *=status
        channel = await bot.get_chat(channel)
        if not status:
            invite_link = await channel.export_invite_link()
            btn.add(InlineKeyboardButton(text=f"❌ {channel.title}", url=invite_link))

    btn.add(InlineKeyboardButton(text="Obunani tekshirish", callback_data="check_subs"))
    if final_status:
        keyboard = InlineKeyboardMarkup()
        web_button = InlineKeyboardButton(text="Xaridni boshlash 🛍", web_app={"url":f"https://{WEB_URL}"})
        keyboard.add(web_button)
        text = f"""🎉 Xush kelibsiz, {call.from_user.full_name}!
Uz Toys Shop do'konimizga tashrif buyurganingiz uchun tashakkur!
Eng zo'r o'yinchoqlar va sovg'alar sizni kutmoqda!
📍 Manzil: Andijon shahar, Jaxon bozori

✨ Yangi mahsulotlar va chegirmalar uchun kuzatib boring!
🚚 Yetkazib berish narxi:

Andijon shahar uchun — bepul 🆓!

Boshqa joylarga zakaz berganingizdan keyin aloqaga chiqib, narxni aytib beramiz.


Agar yordam kerak bo'lsa, aloqa uchun @UzToysShop_Manager bilan bog'lanishingiz mumkin.

Sizni kutib qolamiz! 🚀

 Mahsulotlarni ko'rish uchun pastdagi tugmani bosing 👇🏼"""
        await call.message.answer(text,reply_markup=keyboard)
        await call.answer("Menu 🏠", reply_markup=menu)
    if not final_status:
        await call.answer(cache_time=60)
        await call.message.answer("Siz quyidagi kanal(lar)ga obuna bo'lmagansiz!",reply_markup=btn)
        await call.message.delete()
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('accept_order='))
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    order_id = int(callback_query.data.split('=')[1])
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id
    )
    await Accept.order_id.set()
    await state.update_data(order_id=order_id)
    await Accept.date.set()
    await bot.send_message(chat_id=callback_query.from_user.id,text="Buyurtma Yetkazish sanasini yuboring\nMisol: YYYY-OO-KK 2024-06-13",reply_markup=ReplyKeyboardRemove())
    await bot.answer_callback_query(callback_query.id)
@dp.message_handler(state=Accept.date)
async def process_date(message: types.Message, state: FSMContext):
    date_text = message.text  # Foydalanuvchidan kiritilgan matn

    try:
        # Faqat sana formatini tekshirish (masalan, '2024-11-07')
        date_obj = datetime.strptime(date_text, '%Y-%m-%d').date()
        await state.update_data(date=date_obj)  # Sana saqlash
        user_data = await state.get_data()
        order_id = user_data.get('order_id')
        
        # Foydalanuvchiga xabar yuborish
        today = date.today()
        print(date_obj,today)
        if date_obj < today:
            await message.answer("Kiritilgan sana hozirgi kundan kichkina!\nQayta kiriting")
            await Accept.date.set()
        else:
            send_date_to_django(order_id, date_obj.strftime('%Y-%m-%d'))
            await message.answer(f"Yetkazib berish sanasi belgilandi: {date_obj.strftime('%Y-%m-%d')}")
            await state.finish()
    except ValueError:
        await message.answer("Iltimos, sanani to'g'ri formatda kiriting (YYYY-OO-KK).")
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('cancel_order='))
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    order_id = int(callback_query.data.split('=')[1])
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id
    )
    await Cancel.order_id.set()
    await state.update_data(order_id=order_id)
    await Cancel.reason.set()
    await bot.send_message(chat_id=callback_query.from_user.id,text="Bekor qilish uchun sababni yozing",reply_markup=ReplyKeyboardRemove())
    await bot.answer_callback_query(callback_query.id)
@dp.message_handler(state=Cancel.reason)
async def process_date(message: types.Message, state: FSMContext):
    reason = message.text 
    print(reason)
    await state.update_data(reason=reason)  # Sana saqlash
    user_data = await state.get_data()
    order_id = user_data.get('order_id')
    send_reason(order_id,user_data.get('reason'))
    await state.finish()
    await message.answer("Buyurma bekor qilindi")
@dp.message_handler(lambda message: message.text == "📲 Kontaktlar")
async def send_support_info(message: types.Message):
    text = """Hurmatli foydalanuvchi!
Quyidagi kanallar orqali biz bilan bog‘lanishingiz mumkin:

📞 Telefon: +998907594797
📱 Telegram: Uz Toys Menejer (@UzToysShop_Manager)
📍 Manzil: Andijon shahar, Jaxon bozori

"Savollaringiz bo‘lsa, biz har doim yordam berishga tayyormiz!"""
    await message.reply(text)
@dp.message_handler(lambda message: message.text == "🌍 Do‘kon manzili")
async def send_support_info(message: types.Message):
    text = """🗺️ Manzilimiz: Andijon shahar, Jaxon bozori
✨ "Jaxon bozorida bizga tashrif buyuring va farqni his eting!""""
    latitude = 40.82451  # Kenglik (latitude)
    longitude = 72.355654  # Uzunlik (longitude)
    await bot.send_location(chat_id=message.chat.id, latitude=latitude, longitude=longitude)
    await message.reply(text)
@dp.message_handler(lambda message: message.text == "Xaridni boshlash 🛍")
async def send_support_info(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    web_button = InlineKeyboardButton(text="Xaridni boshlash 🛍", web_app={"url":f"https://{WEB_URL}"})
    keyboard.add(web_button)
    text = f"""🎉 Xush kelibsiz, {message.from_user.full_name}!
Uz Toys Shop do'konimizga tashrif buyurganingiz uchun tashakkur!
Eng zo'r o'yinchoqlar va sovg'alar sizni kutmoqda!
📍 Manzil: Andijon shahar, Jaxon bozori

✨ Yangi mahsulotlar va chegirmalar uchun kuzatib boring!
🚚 Yetkazib berish narxi:

Andijon shahar uchun — bepul 🆓!

Boshqa joylarga zakaz berganingizdan keyin aloqaga chiqib, narxni aytib beramiz.


Agar yordam kerak bo'lsa, aloqa uchun @UzToysShop_Manager bilan bog'lanishingiz mumkin.

Sizni kutib qolamiz! 🚀

Mahsulotlarni ko'rish uchun pastdagi tugmani bosing 👇🏼"""
    await message.answer(text,reply_markup=keyboard)