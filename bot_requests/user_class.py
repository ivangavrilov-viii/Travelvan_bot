from typing import List, Dict, Union, Optional
from telebot.types import InputMediaPhoto
from decouple import config
from loguru import logger
import datetime
import requests
import re


class BotUser:
    """ Класс: Пользователь Телеграм-бота. """
    headers = {'x-rapidapi-host': config('API_HOST'), 'x-rapidapi-key': config('API_KEY')}

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        self.language = None
        self.user_query = None
        self.user_command = None
        self.destination_id = None
        self.hotels_count = None
        self.locale = None
        self.currency = None
        self.photo_count = None
        self.min_price = None
        self.max_price = None
        self.min_distance = None
        self.max_distance = None
        self.date = None

    def set_locale(self, user_language: bool) -> None:
        """Метод класса, устанавливающий язык и валюту для вывода найденной информации"""

        if user_language:
            self.locale = 'eu_US'
            self.currency = 'USD'
        else:
            self.locale = 'ru_RU'
            self.currency = 'RUB'
        logger.info('Locale and currency are set.')

    def kind_of_sort(self) -> str:
        """Метод класса, определяющий метод сортировки и вывода предложенных отелей согласно команде от пользователя"""

        if self.user_command == '/lowprice':
            return 'PRICE'
        elif self.user_command == '/highprice':
            return 'PRICE_HIGHEST_FIRST'
        elif self.user_command == '/bestdeal':
            return 'DISTANCE_FROM_LANDMARK'
        logger.info('Kind of sort is set.')

    def request_location_id(self) -> Optional[list[list[str]]]:
        """Метод класса, определяющий ID всех городов, которые были найдены по запросу пользователя. """

        location_url = 'https://hotels4.p.rapidapi.com/locations/search'
        query_str = {'query': self.user_query, 'locale': self.locale}

        try:
            response = requests.get(url=location_url, headers=self.headers, params=query_str, timeout=30).json()
            id_location_list = [[i_city['destinationId'], re.sub(r'<.*>', self.user_query.capitalize(),
                                                                 i_city['caption'])]
                                for i_city in response['suggestions'][0]['entities'] if i_city['type'] == 'CITY']
            if len(id_location_list) > 0:
                logger.info('Cities list received')
                return id_location_list
            else:
                logger.info('Cities list is NULL.')
                return None
        except Exception as exc:
            logger.exception(f'Failed to search for a list of cities: {exc}')
            return None

    def request_hotel_info(self) -> Optional[List[Dict[str, Union[int, str]]]]:
        """Метод класса, получающий информацию от сервера о каждом из числа искомых отелей ."""

        properties_url = 'https://hotels4.p.rapidapi.com/properties/list'
        check_in = datetime.datetime.now().strftime(f'%Y-%m-%d')
        self.date = datetime.datetime.now().strftime(f'%d-%m-%Y %H:%M:%S')
        check_out = datetime.datetime.now().replace(day=datetime.datetime.now().day + 1).strftime(f'%Y-%m-%d')

        query_str = {"destinationId": self.destination_id, "pageNumber": "1", "pageSize": self.hotels_count,
                     "checkIn": check_in, "checkOut": check_out, "adults1": "1", "sortOrder": self.kind_of_sort(),
                     "locale": self.locale, "currency": self.currency}

        if self.user_command == '/bestdeal':
            query_str["priceMin"] = self.min_price
            query_str["priceMax"] = self.max_price
            query_str["pageSize"] = 25


        try:
            response = requests.request("GET", properties_url, headers=self.headers, params=query_str, timeout=120)
            hotels_list = list()

            for i_dict in response.json()["data"]["body"]["searchResults"]['results']:
                hotel_info = dict()
                hotel_info['address'] = f"{i_dict['address']['streetAddress']}, {i_dict['address']['locality']}"
                hotel_info['hotel_id'] = i_dict['id']
                hotel_info['name'] = i_dict['name']
                hotel_info['landmarks'] = i_dict['landmarks'][0]['distance']
                hotel_info['price'] = i_dict['ratePlan']['price']['current']
                hotels_list.append(hotel_info)
            if hotels_list:
                logger.info('Hotel list received')
                return hotels_list
            else:
                logger.info('Hotel list is NULL')
                return None
        except Exception as exc:
            logger.exception(f'Failed to search for a list of hotels: {exc}')
            return None

    def get_hotel_photo(self, hotel_id) -> Optional[List[InputMediaPhoto]]:
        """Метод класса, получающий информацию о фото каждого отеля по номеру его ID и возвращающий все фото списком"""

        photo_url = 'https://hotels4.p.rapidapi.com/properties/get-hotel-photos'
        query_str = {'id': str(hotel_id)}

        try:
            response = requests.request("GET", photo_url, headers=self.headers, params=query_str, timeout=60).json()
            photo_list = [InputMediaPhoto(elem['baseUrl'].replace('{size}', 'z'))
                          for elem in response['hotelImages'] if 'hotelImages' in response]
            if len(photo_list) >= self.photo_count:
                logger.info(f'Photo list received. Photo count is {self.photo_count}')
                return photo_list[:self.photo_count]
            elif len(photo_list) == 0:
                logger.info('Photo list is NULL')
                return None
            else:
                logger.info(f'Photo list received. Photo count is {len(photo_list)}')
                return photo_list
        except Exception as exc:
            logger.exception(f'Failed to search for a list of hotels: {exc}')
            return None
