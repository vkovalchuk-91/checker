from django.core.cache import cache
from loguru import logger
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from apps.common.constants import WAGON_TYPES, SEAT_TYPES
from apps.tbot_base.bot import tbot as bot


def send_tickets(tg_id, checker_id, direction_info, tickets_matches):
    tg_id_str = str(tg_id)

    menu_dict = {'keyboard': InlineKeyboardMarkup()}
    for ticket in tickets_matches:
        date_str = ticket['departure_date']
        train_number_str = ticket['train_number']
        wagon_types_list = ticket['wagon_types']

        if date_str not in menu_dict:
            button = InlineKeyboardButton(
                text=date_str,
                callback_data=f"{tg_id_str}_{checker_id}_{'trains'}_{date_str}")
            menu_dict['keyboard'].add(button)
            menu_dict[date_str] = {}
            menu_dict[date_str]['keyboard'] = InlineKeyboardMarkup()

        if train_number_str not in menu_dict[date_str]:
            button = InlineKeyboardButton(
                text=train_number_str,
                callback_data=f"{tg_id_str}_{checker_id}_{'wagon-types'}_{date_str}~{train_number_str.replace(' ', '')}")
            menu_dict[date_str]['keyboard'].add(button)

            menu_dict[date_str][train_number_str] = {}
            menu_dict[date_str][train_number_str]['keyboard'] = InlineKeyboardMarkup()

        for wagon_type in wagon_types_list:
            wagon_type_str = wagon_type['wagon_type']
            min_price_str = wagon_type['min_price']
            available_seats_str = wagon_type['available_seats']
            seats_list = wagon_type['seats']

            if wagon_type_str not in menu_dict[date_str][train_number_str]:
                wagon_type_index = WAGON_TYPES.index(wagon_type_str)
                button = InlineKeyboardButton(
                    text=f"{wagon_type_str}, від {min_price_str} грн, місць - {available_seats_str}",
                    callback_data=f"{tg_id_str}_{checker_id}_{'seat-types'}_{date_str}~{train_number_str.replace(' ', '')}~{wagon_type_index}")
                menu_dict[date_str][train_number_str]['keyboard'].add(button)

                menu_dict[date_str][train_number_str][wagon_type_str] = {}
                menu_dict[date_str][train_number_str][wagon_type_str]['keyboard'] = InlineKeyboardMarkup()

                menu_dict[date_str][train_number_str][wagon_type_str][
                    'text'] = f"<b>Місця доступні у вагонах типу '{wagon_type_str}' для потягу {train_number_str} на {date_str}:</b>\n\n"

                for seat in seats_list:
                    seat_type_str = seat['seat_type']
                    seat_type_name_str = None
                    for seat_type_item in SEAT_TYPES:
                        if seat_type_item['seat_type'] == seat_type_str:
                            seat_type_name_str = seat_type_item['seat_type_name']
                    available_seats = seat['available_seats']
                    menu_dict[date_str][train_number_str][wagon_type_str][
                        'text'] += f"{seat_type_name_str} - {available_seats}\n"

    text = f"<b>Знайдено дати на які доступні квитки за напрямком {direction_info}:</b>"
    bot.send_message(tg_id_str, text, reply_markup=menu_dict['keyboard'])
    return menu_dict


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    parts = call.data.split("_")
    tg_id = parts[0]
    checker_id = parts[1]
    menu_key = parts[2]
    path_parts = parts[3].split("~")
    date = path_parts[0]

    menu_dict = cache.get(checker_id)

    try:
        if menu_key == 'trains':
            text = f"<b>Оберіть потяг з тих що доступні на {date}</b>"
            keyboard = menu_dict[date]['keyboard']
            bot.send_message(tg_id, text, reply_markup=keyboard)
        elif menu_key == 'wagon-types':
            train_number = path_parts[1]
            text = f"<b>Оберіть тип вагону для потягу {train_number} на {date}</b>"
            keyboard = menu_dict[date][train_number]['keyboard']
            bot.send_message(tg_id, text, reply_markup=keyboard)
        elif menu_key == 'seat-types':
            train_number = path_parts[1]
            wagon_type_index = path_parts[2]
            wagon_type = WAGON_TYPES[int(wagon_type_index)]
            text = menu_dict[date][train_number][wagon_type]['text']
            bot.send_message(tg_id, text)
    except TypeError as e:
        text = f"Дані застаріли, дочекайтеся нових оновлень!"
        bot.send_message(tg_id, text)
