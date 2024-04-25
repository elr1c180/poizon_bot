from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.start import start_kb
from keyboards.final import final
from keyboards.calc import calc_order
from get_cny import get_cny
from keyboards.admin import text_admin
from keyboards.recalc import recalc
from keyboards.main import main_menu
from keyboards.order_type import order_type_calc
from aiogram.types import CallbackQuery
from fsm import calc_quiz, order_quiz

from aiogram.fsm.context import FSMContext

from calc_order_func import calc_order_func

from main import *

router = Router()  # [1]

@router.message(Command("start"))  # [2]
async def cmd_start(message: Message):
    await message.answer(
        f"<b>{message.from_user.first_name}</b>, добро пожаловать в бот группы Кунг-фу деливери!\nНаша группа поможет Вам выкупить товары с <b>китайских</b> площадок <b>POIZON</b> и <b>TAOBAO</b>.\n\nКратчайшие сроки доставки до Владивостока 7-10 дней с момента покупки, за исключением праздничных дней",
        parse_mode='html',
        reply_markup=start_kb()
    )

@router.callback_query(F.data == 'main_menu')  # [2]
async def cmd_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        f"<b>{callback.from_user.first_name}</b>, добро пожаловать в бот группы Кунг-фу деливери!\nНаша группа поможет Вам выкупить товары с <b>китайских</b> площадок <b>POIZON</b> и <b>TAOBAO</b>.\n\nКратчайшие сроки доставки до Владивостока 7-10 дней с момента покупки, за исключением праздничных дней",
        parse_mode='html',
        reply_markup=start_kb()
    )

    await state.clear()

@router.callback_query(F.data == 'order')
async def new_order(callback: CallbackQuery, state: FSMContext):
    await state.set_state(order_quiz.Order.item_type)
    await callback.message.answer(
        "Выберете категорию товара:",
        reply_markup=order_type_calc()
    )
@router.callback_query(order_quiz.Order.item_type)
async def new_order(callback: CallbackQuery, state: FSMContext):
    await state.update_data(item_type=callback.data)
    await state.set_state(order_quiz.Order.link)
    await callback.message.answer(
        "Отправьте, пожалуйста, ссылку на товар"
    )

@router.message(order_quiz.Order.link)
async def order_link(message: Message, state: FSMContext):
    await state.update_data(link=message.text)
    await state.set_state(order_quiz.Order.photo)

    await message.answer("Отправьте, пожалуйста, фотографию товара")

@router.message(order_quiz.Order.photo)
async def order_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await state.update_data(photo=file_id)
    await state.set_state(order_quiz.Order.size)

    await message.answer("Отправьте, пожалуйста, ваш размер")

@router.message(order_quiz.Order.size)
async def order_size(message: Message, state: FSMContext):
    await state.update_data(size=message.text)
    await state.set_state(order_quiz.Order.color)

    await message.answer("Отправьте, пожалуйста, <b>цвет/модель/аромат</b> товара", parse_mode='html')

@router.message(order_quiz.Order.color)
async def order_color(message: Message, state: FSMContext):
    await state.update_data(color=message.text)
    await state.set_state(order_quiz.Order.price)

    await message.answer("Отправьте, пожалуйста, цену на товар. <b>В юанях</b>", parse_mode='html')

@router.message(order_quiz.Order.price)
async def order_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(order_quiz.Order.promo)

    await message.answer("Отправьте, пожалуйста, промокод.\n\n<b>Если его нет, то отправитьте прочерк(-)</b>", parse_mode='html')

@router.message(order_quiz.Order.promo)
async def order_promo(message: Message, state: FSMContext):
    await state.update_data(promo=message.text)
    await state.set_state(order_quiz.Order.phone)

    await message.answer("Отправьте, пожалуйста, ваш номер телефона/почту")

@router.message(order_quiz.Order.phone)
async def final_order(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.update_data(name=message.from_user.first_name)
    await state.update_data(username=message.from_user.username)
    
    data = await state.get_data()
    item_type = data["item_type"]
    print(item_type)
    link = data["link"]
    photo = data["photo"]
    size = data["size"]
    color = data["color"]
    price = data["price"]
    promo = data["promo"]
    price = calc_order_func(int(price), item_type, promo)
    phone = data["phone"]

    if item_type == 'summer':
        item_type = 'Куртки🥼/Кроссовки👟'
    
    if item_type == 'winter':
        item_type = 'Зимняя обувь🥾/Верхняя одежда👗'
    
    if item_type == 'shirt':
        item_type = 'Футболки👕/Рубашки👔/Шорты🩳'

    if item_type == 'jeans':
        item_type = 'Штаны👖/Толстовки🦺/Летняя обувь👟'
    
    if item_type == 'parf':
        item_type = 'Парфюм👑/Аксессуары💍'
    
    if item_type == 'bag':
        item_type = 'Рюкзаки🎒/Сумки👜'
    
    if item_type == 'socks':
        item_type = 'Носки🧦/Кепки🧢/Нижнее белье🩲'

    await message.answer_photo(photo, caption=f"<b>Ваш заказ сформирован!</b>\nПеред финалом оформления заказа с вами свяжется нас менеджер, чтобы уточнить некоторые детали\n<b>Категория: {item_type}</b>\n<b>Ссылка на товар: {link}</b>\n<b>Размер товара: {size}</b>\n<b>Цвет товара: {color}</b>\n<b>Стоимость: {round(price['total'],2)}</b>\n<b>Стоимость без промокода: {round(price['total_without_promo'],2)}</b>\n<b>Промокод: {promo}</b>\n<b>Контактные данные: {phone}, {message.from_user.first_name}  {message.from_user.last_name},  @{message.from_user.username}</b>\n\n---\n\nПросим проверить данные, если все верно, нажмите кнопку:", 
                                               parse_mode='html',
                                               reply_markup=final())

@router.callback_query(F.data == "final_order")
async def send_message(callback: CallbackQuery, state: FSMContext):
    await state.update_data()
    data = await state.get_data()
    item_type = data["item_type"]
    link = data["link"]
    photo = data["photo"]
    size = data["size"]
    color = data["color"]
    price = data["price"]
    promo = data["promo"]
    price_cny = data["price"]
    price = calc_order_func(int(price), item_type, promo)
    phone = data["phone"]
    name = data["name"]
    username = data["username"]

    if item_type == 'summer':
        item_type = 'Куртки🥼/Кроссовки👟'
    
    if item_type == 'winter':
        item_type = 'Зимняя обувь🥾/Верхняя одежда👗'
    
    if item_type == 'shirt':
        item_type = 'Футболки👕/Рубашки👔/Шорты🩳'

    if item_type == 'jeans':
        item_type = 'Штаны👖/Толстовки🦺/Летняя обувь👟'
    
    if item_type == 'parf':
        item_type = 'Парфюм👑/Аксессуары💍'
    
    if item_type == 'bag':
        item_type = 'Рюкзаки🎒/Сумки👜'
    
    if item_type == 'socks':
        item_type = 'Носки🧦/Кепки🧢/Нижнее белье🩲'

    await callback.bot.send_photo('-1002127645159',photo, caption=f"<b>Новый заказ!</b>\nПредварительные детали заказа\n\n<b>Ссылка на товар: {link}</b>\n<b>Размер товара: {size}</b>\n<b>Цвет товара: {color}</b>\n<b>Категория: {item_type}</b>\n<b>Стоимость в Юанях: {price_cny}</b>\n<b>Стоимость: {round(price['total'],2)}</b>\n<b>Стоимость без промокода: {round(price['total_without_promo'],2)}</b>\n<b>Промокод: {promo}</b>\n<b>Контактные данные: {phone}, {name}  @{username}</b>\n", 
                                parse_mode='html',)
    
    await callback.message.answer("Отлично! Оплачивайте товар 💸 по реквизитам ниже и ожидайте ответ менеджера.\n\n<code>2202 2080 8468 3904</code>\n\nРучко Максим Евгеньевич. Сбербанк", parse_mode='html')

    await state.clear()    

@router.callback_query(F.data == 'current_rates')
async def current_rate(callback: CallbackQuery):
    try:
        rate = get_cny()['rub_rate_plus']
    except Exception as e:
        await callback.message.answer(
            'На данный момент биржа для сбора курса недоступна, просьба обратиться к Админу',
            reply_markup=main_menu()
        )
        
    await callback.message.answer(
        f"Текущий курс по ЦБ РФ - <b>{rate} РУБ.</b>\n\nКурс рассчитан с учетом конвертации ₽ в ¥ и комиссии за перевод за границу.",
        parse_mode='html',
        reply_markup=main_menu()
    )

@router.callback_query(F.data == "calc")
async def calc(callback: CallbackQuery, state: FSMContext):
    await state.set_state(calc_quiz.CalcForm.item_type)
    await callback.message.answer(
        "В калькуляторе вы можете сделать расчет стоимости товаров с доставкой до склада во Владивостоке, стоимость включает:\n- Доставка по Китаю\n- Доставка Китай - Владивосток\n- Комиссия нашего сервиса.\n\n<b>Выберете категорию товара:</b>",
        parse_mode="html",
        reply_markup=calc_order()
    )
@router.callback_query(calc_quiz.CalcForm.item_type)
async def calc_price(callback: CallbackQuery, state: FSMContext):
    await state.update_data({'item_type':callback.data})
    data = await state.get_data()
    data = data['item_type']
    if data != 'not_found' and data != 'reply_to_admin':
        await state.set_state(calc_quiz.CalcForm.price)
        await callback.message.answer("Напишите цену в Юанях на берюзовом фоне")
    else:
        await callback.message.answer(
            '<b>Друзья, в связи с тем, что некоторые категории товаров имеют слишком разнообразный выбор, просчитать их точную стоимость не является возможным</b>,так как одним из самых главных факторов при расчетах является <b>доставка</b>\n\nДоставка при перевозках из Китая в Россию высчитывается исключительно через объемный вес и килограммы.\n\nЕсли Вашей категории в списке для расчета нет, то напишите, пожалуйста, нашему менеджеру и он с удовольствием поможет рассчитать Ваш заказ 😊',
            parse_mode='html',
            reply_markup=text_admin()
        )
        await state.clear()
@router.message(calc_quiz.CalcForm.price)
async def calc_promo(message: Message, state: FSMContext):
    await state.update_data({'price': message.text})
    await state.set_state(calc_quiz.CalcForm.promo)
    await message.answer(
        "Введите промокод, если он у вас есть <b>Если его нет, то поставьте прочерк(-)</b>",
        parse_mode='html'
        )

@router.message(calc_quiz.CalcForm.promo)
async def total(message: Message, state: FSMContext):
    await state.update_data({"promo":message.text})
    price =  await state.get_data()
    print(price)
    item_type = await state.get_data()
    promo = await state.get_data()

    price, item_type, promo = price["price"], item_type["item_type"], promo["promo"]

    res = calc_order_func(int(price), item_type, promo)

    await message.answer(
        f"Итоговая стоимость вашего заказа:\n\nБез учёта промокода:<b>{int(res['total_without_promo'])} РУБ</b>\nС учётом промокода:<b>{int(res['total'])} РУБ</b> + стоимость доставки по РФ СДЭК (рассчитывается отдельно)",
        parse_mode='html',
        reply_markup=recalc()
    )
    await state.clear()
    