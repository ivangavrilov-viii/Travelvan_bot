from telebot.types import Message


def hello(message: Message, input_language: bool) -> str:
    if input_language:
        return f'Hello, {message.chat.first_name}👋\n' \
               f'I\'m bot TravelvanBot (@Travelvan_bot) by "Too Easy Travel"\n' \
               f'I can search hotels for you\n' \
               f'Write /help to get info about me\n'
    return f'Привет, {message.chat.first_name}👋\n' \
           f'Я - бот компании "Too Easy Travel" TravelvanBot (@Travelvan_bot)\n' \
           f'Я занимаюсь поиском подходящих отелей\n' \
           f'Чтобы получить обо мне справку, введите /help\n'


def help_message(input_language: bool) -> str:
    if input_language:
        return f'You can use any methods now:\n' \
               f'/help — help with bot commands\n' \
               f'/language — change language\n' \
               f'/lowprice — search for the cheapest hotels in the city\n' \
               f'/highprice — search for the most expensive hotels in the city\n' \
               f'/bestdeal — search for hotels most suitable for price and location from center\n' \
               f'/history — hotel search history\n'
    return f'Вы можете воспользоваться командами:\n' \
           f'/help — помощь по командам бота\n' \
           f'/language — изменить язык\n' \
           f'/lowprice — поиск самых дешевых отелей города\n' \
           f'/highprice — поиск самых дорогих отелей города\n' \
           f'/bestdeal —  поиск отелей, наиболее подходящих по цене и расположению от центра\n' \
           f'/history — вывод истории поиска отелей\n'


def unknown_command(input_language: bool) -> str:
    if input_language:
        return f'I\'m don\'t know this command...'
    return f'Я не знаю такой команды... '


def city_enter(input_language: bool) -> str:
    if input_language:
        return 'Enter city to search: '
    return 'Введите город для поиска: '


def hotel_incorrect_enter(input_language: bool) -> tuple[str, str]:
    logger_error = 'Incorrect entry of hotels number. Another attempt '
    if input_language:
        message = f'Incorrect input. Try again\nEnter count of hotels: \nMaximum number of hotels - 25'
    else:
        message = f"Некорректный ввод. Попробуйте ещё раз\nВведите число отелей: \nМаксимальное число отелей - 25"
    return logger_error, message


def hotels_count_enter(input_language: bool) -> str:
    if input_language:
        return 'Enter count of hotels: \nMaximum number of hotels - 25'
    return 'Введите число отелей: \nМаксимальное число отелей - 25'


def price_incorrect_enter(input_language: bool) -> tuple[str, str]:
    logger_error = 'Incorrect entry of the price range. Another attempt '
    if input_language:
        message = f'Incorrect input. Try again\n' \
                  f'\nEnter the minimum and maximum price in $, USD:\n(Space-separated enter) '
    else:
        message = f"Некорректный ввод. Попробуйте ещё раз" \
                  f"\nВведите минимальную и максимальную цены в RUB, ₽:\n(Ввод через пробел)"
    return logger_error, message


def price_enter(input_language: bool) -> str:
    if input_language:
        return f'Enter the minimum and maximum price in $, USD:\n(Space-separated enter)'
    return f'Введите минимальную и максимальную цены в RUB, ₽:\n(Ввод через пробел) '


def photo_not_found(input_language: bool) -> str:
    if input_language:
        return 'We couldn\'t find a photo for this hotel ...\nWe apologize'
    return 'Фото для данного отеля найти не получилось...\nПриносим свои извинения'


def photo_count_enter(input_language: bool) -> str:
    if input_language:
        return 'Enter count of photo: \nMaximum number of photo - 5'
    return 'Введите число фото: \nМаксимальное число фото - 5'


def photo_incorrect_enter(input_language: bool) -> tuple[str, str]:
    logger_error = 'Incorrect entry of the photo range. Another attempt '
    if input_language:
        message = f'Incorrect input. Try again\n' \
                  f'Enter count of photo for each hotel: \nMaximum number of photo - 5'
    else:
        message = f"Некорректный ввод. Попробуйте ещё раз\n" \
                  f"Введите число фото для каждого отеля: \nМаксимальное число фото - 5"
    return logger_error, message


def photo_refusal_message(input_language: bool) -> tuple[str, str]:
    logger_error = 'The user refused to display the photo'
    if input_language:
        message = 'You have given up the photo\nSearching hotels, wait a while...'
    else:
        message = 'Вы отказались от фото\nПоиск отелей, подождите некоторое время...'
    return logger_error, message


def searching_location(input_language: bool) -> str:
    if input_language:
        return 'Searching location, wait a while...'
    return 'Поиск города, подождите некоторое время...'


def searching_hotels(input_language: bool) -> str:
    if input_language:
        return 'Searching hotels, wait a while...'
    return 'Поиск отелей, подождите некоторое время...'


def distance_enter(input_language: bool) -> str:
    if input_language:
        return 'Enter the minimum and maximum distance to centre in miles: \n(Space-separated enter) '
    else:
        return 'Введите минимальное и максимальное расстояния до центра (в километрах): \n(Ввод через пробел)'


def distance_incorrect_enter(input_language: bool) -> tuple[str, str]:
    logger_error = 'Incorrect entry of the price range. Another attempt '
    if input_language:
        message = f'Incorrect input. Try again\n' \
                  f'Enter the minimum and maximum distance in miles:\n(Space-separated enter) '
    else:
        message = f"Некорректный ввод. Попробуйте ещё раз\n" \
                  f"Введите минимальное и максимальное расстояния в километрах:\n(Ввод через пробел) "
    return logger_error, message


def problem_on_server(input_language: bool) -> str:
    if input_language:
        return 'Not found. Server has few problems. Try again later...'
    return 'Не найдено. На данный момент проблемы на сервере. Попробуйте позже...'
