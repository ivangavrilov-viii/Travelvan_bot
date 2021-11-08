from telebot import types


def language_keyboard(changed_lang: bool) -> types.InlineKeyboardMarkup:
    """Функция для создания клавиатуры на установление/изменение языка"""

    keyboard = types.InlineKeyboardMarkup()
    if changed_lang:
        keyboard.add(types.InlineKeyboardButton(text='Russian', callback_data='change_ru'))
        keyboard.add(types.InlineKeyboardButton(text='English', callback_data='change_en'))
    else:
        keyboard.add(types.InlineKeyboardButton(text='Russian', callback_data='ru'))
        keyboard.add(types.InlineKeyboardButton(text='English', callback_data='en'))
    return keyboard


def show_photo_keyboard(input_language: bool) -> tuple[str, types.InlineKeyboardMarkup]:
    """Функция для создания клавиатуры на вывод фотографий"""

    keyboard = types.InlineKeyboardMarkup()
    if input_language:
        keyboard.add(types.InlineKeyboardButton(text='Yes', callback_data='photo_true'))
        keyboard.add(types.InlineKeyboardButton(text='No', callback_data='photo_false'))
        text = 'Show photos of hotels?'
    else:
        keyboard.add(types.InlineKeyboardButton(text='Да', callback_data='photo_true'))
        keyboard.add(types.InlineKeyboardButton(text='Нет', callback_data='photo_false'))
        text = 'Показать фото отелей ?'
    return text, keyboard


def location_id_keyboard(input_location_list: list, input_language: bool) -> tuple[str, types.InlineKeyboardMarkup]:
    """Функция для создания клавиатуры на вывод списка предложенных городов по запросу"""

    keyboard = types.InlineKeyboardMarkup()
    for location_data in input_location_list:
        keyboard.add(types.InlineKeyboardButton(text=location_data[1], callback_data=location_data[0]))

    if input_language:
        keyboard.add(types.InlineKeyboardButton(text='< Back', callback_data='back'))
        text = 'Select city: '
    else:
        keyboard.add(types.InlineKeyboardButton(text='< Назад', callback_data='back'))
        text = 'Выберете город: '
    return text, keyboard
