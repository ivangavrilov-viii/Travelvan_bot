from bot_requests.user_class import BotUser
from loguru import logger
from typing import Any
import sqlite3


def get_result_high_low_price(input_user: BotUser, input_language: bool) -> Any:
    """Функция получения результата поиска по командам /highprice и /lowprice"""

    hotels_list = input_user.request_hotel_info()
    photo_list, text_list = list(), list()
    user_hotels = ''

    if hotels_list:
        for hotel in hotels_list:
            if input_user.photo_count != 0:
                hotel_photo_list = input_user.get_hotel_photo(hotel['hotel_id'])

                if hotel_photo_list:
                    photo_list.append(hotel_photo_list)

            user_hotels += f"{hotel['name']}\n"

            if input_language:
                text = f"Hotel name: {hotel['name']}\nAddress: {hotel['address']}\n" \
                       f"Distance to centre: {hotel['landmarks']}\n" \
                       f"Price per one: {hotel['price']}\n"
            else:
                text = f"Название отеля: {hotel['name']}\n" \
                       f"Адрес: {hotel['address']}\n" \
                       f"Расстояние до центра: {hotel['landmarks']}\n" \
                       f"Цена за одного человека: {hotel['price']}\n"
            text_list.append(text)

        save_to_database(input_user.user_id, input_user.user_command, input_user.date, user_hotels)
        return photo_list, text_list
    return None


def get_result_bestdeal(input_user: BotUser, input_language: bool) -> Any:
    """Функция получения результата поиска по командам /bestdeal"""

    hotels_list = input_user.request_hotel_info()
    sorted_hotels_list, photo_list, text_list = list(), list(), list()
    user_hotels = ''

    if hotels_list:
        for hotel in hotels_list:
            hotel_distance = float(hotel['landmarks'].split()[0].replace(',', '.'))
            if input_user.max_distance >= hotel_distance >= input_user.min_distance:
                sorted_hotels_list.append(hotel)

        if sorted_hotels_list:
            for hotel in sorted_hotels_list[:input_user.hotels_count]:

                if input_user.photo_count != 0:
                    hotel_photo_list = input_user.get_hotel_photo(hotel['hotel_id'])
                    if hotel_photo_list:
                        photo_list.append(hotel_photo_list)

                user_hotels += f"{hotel['name']}\n"

                if input_language:
                    text = f"Hotel name: {hotel['name']}\nAddress: {hotel['address']}\n" \
                           f"Distance to centre: {hotel['landmarks']}\n"\
                           f"Price per one: {hotel['price']}\n"
                else:
                    text = f"Название отеля: {hotel['name']}\n"\
                           f"Адрес: {hotel['address']}\n"\
                           f"Расстояние до центра: {hotel['landmarks']}\n"\
                           f"Цена за одного человека: {hotel['price']}\n"
                text_list.append(text)

            save_to_database(input_user.user_id, input_user.user_command, input_user.date, user_hotels)

        else:
            if input_language:
                text = "Hotels with these parameters were not found.\nChange your search options and try again."
            else:
                text = "Отели с данными параметрами не найдены.\nИзмените параметры поиска и попробуйте снова."
            text_list.append(text)
        return photo_list, text_list
    return None


def save_to_database(user_id: int, user_command: str, time: str, hotels_list: str) -> None:
    """Функция, сохраняющая результат поиска отелей в базу данных для каждого пользователя"""

    try:
        table = sqlite3.connect('history.db')
        cursor = table.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(user_id INTEGER, 
                            user_command TEXT, date TEXT, hotels_name TEXT);""")
        table.commit()
        cursor = table.cursor()
        cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?);", (user_id, user_command, time, hotels_list))
        table.commit()
        cursor.close()
        logger.info('Info about request is saved in database.')
    except sqlite3.Error as error:
        logger.error(f'Error with database {error}')


def get_history(input_user: BotUser, input_language: bool) -> str:
    """Функция вывода информации об истории запросов каждого пользователя"""

    text = ''
    try:
        table = sqlite3.connect('history.db')
        cursor = table.cursor()
        cursor.execute("""SELECT * FROM users WHERE user_id=?;""", (input_user.user_id,))
        logger.info(f'Info about request user\'s with ID:{input_user.user_id}')
        if input_language:
            for content in cursor.fetchall():
                text += f"User\'s command: {content[1][1:]}\n"\
                        f"Date and time: {content[2]}\n"\
                        f"List of hotels found on request: \n{content[3]}\n"
        else:
            for content in cursor.fetchall():
                text += f"Команда пользователя: {content[1][1:]}\n"\
                        f"Дата и время: {content[2]}\n"\
                        f"Список отелей, найденных по запросу: \n{content[3]}\n"
        return text
    except sqlite3.Error as error:
        logger.error(f'Error with database {error}')
