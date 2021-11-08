from telebot.types import Message, CallbackQuery
from bot_requests.user_class import BotUser
from decouple import config
from loguru import logger
from typing import Dict
import bot_messages
import set_params
import get_info
import telebot


bot = telebot.TeleBot(config('BOT_TOKEN'))
users_dict: Dict[int, BotUser] = dict()


@bot.message_handler(content_types=['text'])
def start(message: Message) -> None:
    """Функция вызова и обработки основных команд бота"""

    global users_dict
    if message.text == '/start':
        if message.chat.id not in users_dict:
            users_dict[message.chat.id] = BotUser(message.chat.id)
        bot.send_message(message.chat.id, text='Выберете язык / Select language ',
                         reply_markup=set_params.language_keyboard(False))

    elif message.text == '/language':
        bot.send_message(message.chat.id, text='Выберете язык / Select language ',
                         reply_markup=set_params.language_keyboard(True))

    elif message.text in ['/hello-world', 'Привет']:
        bot.send_message(message.chat.id, bot_messages.hello(message, users_dict[message.chat.id].language))

    elif message.text == '/help':
        bot.send_message(message.chat.id, bot_messages.help_message(users_dict[message.chat.id].language))

    elif message.text in ['/lowprice', '/highprice', '/bestdeal']:
        users_dict[message.chat.id].user_command = message.text
        bot.send_message(message.chat.id, bot_messages.city_enter(users_dict[message.chat.id].language))
        bot.register_next_step_handler(message, select_city)

    elif message.text == '/history':
        bot.send_message(message.chat.id,
                         get_info.get_history(users_dict[message.chat.id], users_dict[message.chat.id].language))
        logger.info('User\'s history on display.')

    else:
        bot.send_message(message.chat.id, bot_messages.unknown_command(users_dict[message.chat.id].language))


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call: CallbackQuery) -> None:
    """Функция обработки ответов от клавиатуры"""

    user_id = call.message.chat.id
    if call.data == "ru":
        users_dict[user_id].language = False
        bot.send_message(user_id, bot_messages.hello(call.message, users_dict[user_id].language))

    elif call.data == 'en':
        users_dict[user_id].language = True
        bot.send_message(user_id, bot_messages.hello(call.message, users_dict[user_id].language))

    elif call.data == 'change_en':
        users_dict[user_id].language = True
        bot.send_message(user_id, f'Language changed\nLucky search 😉')
        bot.send_message(user_id, bot_messages.help_message(users_dict[user_id].language))

    elif call.data == 'change_ru':
        users_dict[user_id].language = False
        bot.send_message(user_id, f'Язык изменен\nУдачного поиска 😉')
        bot.send_message(user_id, bot_messages.help_message(users_dict[user_id].language))

    elif call.data == 'back':
        bot.send_message(user_id, bot_messages.help_message(users_dict[user_id].language))

    elif call.data == 'photo_true':
        bot.send_message(user_id, bot_messages.photo_count_enter(users_dict[user_id].language))
        bot.register_next_step_handler(call.message, photo_count)

    elif call.data == 'photo_false':
        users_dict[user_id].photo_count = 0
        logger.info(bot_messages.photo_refusal_message(users_dict[user_id].language)[0])
        bot.send_message(user_id, bot_messages.photo_refusal_message(users_dict[user_id].language)[1])
        search_result(call.message)
    else:
        users_dict[user_id].destination_id = call.data
        logger.info(f'\"Destination_id\" is set. {users_dict[user_id].destination_id}')
        if users_dict[user_id].user_command == '/bestdeal':
            bot.send_message(user_id, bot_messages.price_enter(users_dict[user_id].language))
            bot.register_next_step_handler(call.message, price_range)
        else:
            bot.send_message(user_id,  bot_messages.hotels_count_enter(users_dict[user_id].language))
            bot.register_next_step_handler(call.message, hotels_count)


def select_city(message: Message) -> None:
    """Функция получения location_id от API и выбора искомого города с помощью клавиатуры"""

    user_id = message.chat.id
    bot.send_message(user_id, bot_messages.searching_location(users_dict[user_id].language))
    users_dict[user_id].user_query = message.text
    users_dict[user_id].set_locale(users_dict[user_id].language)
    location_id_list = users_dict[user_id].request_location_id()

    if location_id_list:
        bot.send_message(user_id, text=str(set_params.location_id_keyboard(location_id_list,
                                                                           users_dict[user_id].language)[0]),
                         reply_markup=set_params.location_id_keyboard(location_id_list,
                                                                      users_dict[user_id].language)[1])
    else:
        bot.send_message(user_id, bot_messages.problem_on_server(users_dict[user_id].language))
        bot.send_message(user_id, bot_messages.help_message(users_dict[user_id].language))


def price_range(message: Message) -> None:
    """Функция установки минимальной и максимальной цен"""

    user_id = message.chat.id
    price_list = message.text.split(' ')
    error = False
    if len(price_list) == 1:
        if price_list[0].isdigit() and int(price_list[0]) > 0:
            users_dict[user_id].min_price, users_dict[user_id].max_price = 0, int(price_list[0])
            logger.info(f'Minimum and maximum prices are set {users_dict[user_id].min_price}, '
                        f'{users_dict[user_id].max_price} {users_dict[user_id].currency}')
            bot.send_message(user_id, bot_messages.distance_enter(users_dict[user_id].language))
            bot.register_next_step_handler(message, distance_range)
        else:
            error = True
    elif len(price_list) == 2:
        if price_list[0].isdigit() and price_list[1].isdigit():
            if int(price_list[0]) > int(price_list[1]):
                users_dict[user_id].min_price, users_dict[user_id].max_price = \
                    int(price_list[1]), int(price_list[0])
            else:
                users_dict[user_id].min_price, users_dict[user_id].max_price = \
                    int(price_list[0]), int(price_list[1])
            logger.info(f'Minimum and maximum prices are set {users_dict[user_id].min_price},'
                        f' {users_dict[user_id].max_price} {users_dict[user_id].currency}')
            bot.send_message(user_id, bot_messages.distance_enter(users_dict[user_id].language))
            bot.register_next_step_handler(message, distance_range)
        else:
            error = True
    else:
        error = True
    if error:
        logger.error(bot_messages.price_incorrect_enter(users_dict[user_id].language)[0])
        bot.send_message(user_id, bot_messages.price_incorrect_enter(users_dict[user_id].language)[1])
        bot.register_next_step_handler(message, price_range)


def distance_range(message: Message) -> None:
    """Функция установки минимального и максимального расстояний от центра города"""

    user_id = message.chat.id
    distance_list = message.text.split(' ')
    error = False
    if len(distance_list) == 1:
        if distance_list[0].isdigit() and int(distance_list[0]) > 0:
            users_dict[user_id].min_distance, users_dict[user_id].max_distance = 0, int(distance_list[0])

            if users_dict[user_id].language:
                logger.info(f'Minimum and maximum distances are set {users_dict[user_id].min_distance}, '
                            f'{users_dict[user_id].max_distance} miles')
            else:
                logger.info(f'Minimum and maximum distances are set {users_dict[user_id].min_distance},'
                            f'{users_dict[user_id].max_distance} kilometres')
            bot.send_message(user_id, bot_messages.hotels_count_enter(users_dict[user_id].language))
            bot.register_next_step_handler(message, hotels_count)
        else:
            error = True
    elif len(distance_list) == 2:
        if distance_list[0].isdigit() and distance_list[1].isdigit():
            if int(distance_list[0]) > int(distance_list[1]):
                users_dict[user_id].min_distance, users_dict[user_id].max_distance = \
                    int(distance_list[1]), int(distance_list[0])
            else:
                users_dict[user_id].min_distance, users_dict[user_id].max_distance = \
                    int(distance_list[0]), int(distance_list[1])

            if users_dict[user_id].language:
                logger.info(f'Minimum and maximum distances are set {users_dict[user_id].min_distance}, '
                            f'{users_dict[user_id].max_distance} miles')
            else:
                logger.info(f'Minimum and maximum distances are set {users_dict[user_id].min_distance},'
                            f'{users_dict[user_id].max_distance} kilometres')
            bot.send_message(user_id, bot_messages.hotels_count_enter(users_dict[user_id].language))
            bot.register_next_step_handler(message, hotels_count)
        else:
            error = True
    else:
        error = True
    if error:
        logger.error(bot_messages.distance_incorrect_enter(users_dict[user_id].language)[0])
        bot.send_message(user_id, bot_messages.distance_incorrect_enter(users_dict[user_id].language)[1])
        bot.register_next_step_handler(message, distance_range)


def hotels_count(message) -> None:
    """Функция установки количества выводимых отелей"""

    if message.text.isdigit() and 26 > int(message.text) > 0:
        users_dict[message.chat.id].hotels_count = int(message.text)
        logger.info(f'User\'s page size {users_dict[message.chat.id].hotels_count} hotel(-s)')
        bot.send_message(message.chat.id, text=set_params.show_photo_keyboard(users_dict[message.chat.id].language)[0],
                         reply_markup=set_params.show_photo_keyboard(users_dict[message.chat.id].language)[1])
    else:
        logger.error(bot_messages.hotel_incorrect_enter(users_dict[message.chat.id].language)[0])
        bot.send_message(message.chat.id, bot_messages.hotel_incorrect_enter(users_dict[message.chat.id].language)[1])
        bot.register_next_step_handler(message, hotels_count)


def photo_count(message: Message) -> None:
    """Функция установки количества фотографии для каждого отеля"""

    if message.text.isdigit() and 6 > int(message.text) >= 0:
        users_dict[message.chat.id].photo_count = int(message.text)
        bot.send_message(message.chat.id, bot_messages.searching_hotels(users_dict[message.chat.id].language))
        search_result(message)
    else:
        logger.error(bot_messages.photo_incorrect_enter(users_dict[message.chat.id].language)[0])
        bot.send_message(message.chat.id, bot_messages.photo_incorrect_enter(users_dict[message.chat.id].language)[1])
        bot.register_next_step_handler(message, photo_count)


def search_result(message: Message):
    """Функция получения и вывода результатов поиска информации об отелях и фотографий"""

    user_id = message.chat.id
    try:
        if users_dict[user_id].user_command == '/bestdeal':
            [photo, output_message] = get_info.get_result_bestdeal(users_dict[user_id], users_dict[user_id].language)
            if photo and output_message:
                for i in range(len(output_message)):
                    if photo[i]:
                        bot.send_media_group(user_id, photo[i])
                    else:
                        bot.send_message(user_id, bot_messages.photo_not_found(users_dict[user_id].language))
                    bot.send_message(user_id, str(output_message[i]))
            elif output_message:
                for out_mes in output_message:
                    bot.send_message(user_id, out_mes)
            logger.info('Success. Info about hotels for user on display')

        elif users_dict[user_id].user_command in ['/highprice', '/lowprice']:
            [photo, output_message] = get_info.get_result_high_low_price(users_dict[user_id],
                                                                         users_dict[user_id].language)
            if photo and output_message:
                for i in range(len(output_message)):
                    if photo[i]:
                        bot.send_media_group(user_id, photo[i])
                    else:
                        bot.send_message(user_id, bot_messages.photo_not_found(users_dict[user_id].language))
                    bot.send_message(user_id, str(output_message[i]))
            elif output_message:
                for out_mes in output_message:
                    bot.send_message(user_id, out_mes)
            logger.info('Success. Info about hotels for user on display')
    except Exception as error:
        logger.error(f'Bot is crushed... {error}')
        if users_dict[user_id].language:
            bot.send_message(user_id, 'Not found. Server has few problems. Try again later...')
        else:
            bot.send_message(user_id, 'Не найдено. На данный момент проблемы на сервере. Попробуйте позже...')


if __name__ == '__main__':
    logger.add('logger.log', level='DEBUG', format='{time} {level} {message}', encoding='utf-8')
    bot.polling(none_stop=True, interval=0)
