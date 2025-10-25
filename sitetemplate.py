from flask import Flask, render_template, url_for, request, session, redirect, jsonify
import json
import os
from collections import defaultdict

# Ініціалізація Flask
app = Flask(__name__)
# 🔴 КЛЮЧОВЕ: Секретний ключ для управління сесіями (ОБОВ'ЯЗКОВО!)
app.secret_key = 'your_super_secret_key_here_for_secure_sessions' 

# =========================================================================
# 🔴 ПОВНИЙ КАТАЛОГ ПРОДУКТІВ (ШЛЯХИ БЕЗ ПРЕФІКСУ 'images/')
# =========================================================================

PRODUCTS = {
    # ------------------ Секція 1: Пральні засоби (laundry) ------------------
    1: {"name": "Безфосфатний гель для прання білих та світлих речей White, 1л", "price": 117.00, "desc": "Новинка! Екологічний гель для ідеальної білизни.", "img": "laundry_white_1l.png", "category": "laundry", "tag": "Новинка", "is_highlight": True}, 
    2: {"name": "Безфосфатний гель для прання кольорових речей Color, 1л", "price": 117.00, "desc": "Новинка! Захист кольору та м'якість тканин.", "img": "laundry_color_1l.png", "category": "laundry", "tag": "Новинка", "is_highlight": True}, 
    3: {"name": "Безфосфатний гель для прання чорних та темних речей Black, 1л", "price": 117.00, "desc": "Новинка! Зберігає насиченість чорного та темних кольорів.", "img": "laundry_black_1l.png", "category": "laundry", "tag": "Акція", "is_highlight": True, "price_old": 150.00},
    4: {"name": "Безфосфатний гель для прання білих та світлих речей White, 2л", "price": 199.00, "desc": "Економічна упаковка для білої білизни.", "img": "laundry_white_2l.png", "category": "laundry", "tag": "Хіт", "is_highlight": False},
    5: {"name": "Гель для прання білих та світлих речей White, 5л", "price": 450.00, "desc": "Великий об'єм. Професійний догляд.", "img": "laundry_white_5l.png", "category": "laundry", "tag": None, "is_highlight": False},
    6: {"name": "Безфосфатний гель для прання кольорових речей Color, 2л", "price": 199.00, "desc": "Економічна упаковка для кольорової білизни.", "img": "laundry_color_2l.png", "category": "laundry", "tag": None, "is_highlight": False},
    7: {"name": "Гель для прання кольорових речей Color, 5л", "price": 450.00, "desc": "Великий об'єм. Професійний догляд.", "img": "laundry_color_5l.png", "category": "laundry", "tag": None, "is_highlight": False},
    8: {"name": "Засіб для прання чорних та темних речей Black, 2л", "price": 199.00, "desc": "Економічна упаковка для темної білизни.", "img": "laundry_black_2l.png", "category": "laundry", "tag": None, "is_highlight": False},
    9: {"name": "Гель для прання чорних та темних речей Black, 5л", "price": 450.00, "desc": "Великий об'єм. Професійний догляд.", "img": "laundry_black_5l.png", "category": "laundry", "tag": None, "is_highlight": False},
    10: {"name": "Гель для прання універсальний з ензимами, 5л", "price": 465.00, "desc": "Посилена формула з біоактивними ензимами.", "img": "laundry_universal_enzymes_5l.png", "category": "laundry", "tag": "Premium", "is_highlight": False},
    11: {"name": "Засіб для прання Universal, 5л", "price": 395.00, "desc": "Універсальне рішення для всієї родини.", "img": "laundry_universal_5l.png", "category": "laundry", "tag": None, "is_highlight": False},
    12: {"name": "Пральний порошок Baby, 5кг (без ароматизаторів)", "price": 350.00, "desc": "Гіпоалергенний, без запаху, для чутливої шкіри.", "img": "laundry_baby_5kg.png", "category": "laundry", "tag": "Еко", "is_highlight": False},
    13: {"name": "Пральний порошок Baby, 1кг (без ароматизаторів)", "price": 85.00, "desc": "Гіпоалергенний, без запаху, для чутливої шкіри.", "img": "laundry_baby_1kg.png", "category": "laundry", "tag": "Еко", "is_highlight": False},
    14: {"name": "Пральний порошок Парфум, 1кг", "price": 95.00, "desc": "З насиченим парфумованим ароматом.", "img": "laundry_parfum_1kg.png", "category": "laundry", "tag": None, "is_highlight": False},
    15: {"name": "Пральний порошок універсальний Парфум, 5кг", "price": 395.00, "desc": "З насиченим парфумованим ароматом.", "img": "laundry_parfum_5kg.png", "category": "laundry", "tag": "Акція", "is_highlight": False, "price_old": 450.00},
    16: {"name": "Кондиціонер для прання Fresh Elegance, 1л", "price": 80.00, "desc": "Аромат ранкової свіжості та легкість прасування.", "img": "conditioner_fresh_1l.png", "category": "laundry", "tag": None, "is_highlight": False},
    17: {"name": "Кондиціонер для прання Velvet Air, 1л", "price": 80.00, "desc": "Неймовірна м'якість та ніжний аромат.", "img": "conditioner_velvet_1l.png", "category": "laundry", "tag": None, "is_highlight": False},
    18: {"name": "Кондиціонер для прання Island Paradise, 1л", "price": 80.00, "desc": "Екзотичний аромат тропічного острова.", "img": "conditioner_island_1l.png", "category": "laundry", "tag": None, "is_highlight": False},
    19: {"name": "Кондиціонери для прання Euphoria of love, 1л", "price": 90.00, "desc": "Насичений чуттєвий аромат.", "img": "conditioner_euphoria_1l.png", "category": "laundry", "tag": None, "is_highlight": False},
    20: {"name": "Кондиціонер для прання Euphoria of love, 2л", "price": 150.00, "desc": "Насичений чуттєвий аромат.", "img": "conditioner_euphoria_2l.png", "category": "laundry", "tag": None, "is_highlight": False},
    21: {"name": "Кондиціонер для прання Euphoria of love, 5л", "price": 320.00, "desc": "Насичений чуттєвий аромат. Вигідний об'єм.", "img": "conditioner_euphoria_5l.png", "category": "laundry", "tag": None, "is_highlight": False},
    22: {"name": "Ополіскувач для прання Flower mystery, 1л", "price": 90.00, "desc": "Таємничий квітковий букет.", "img": "conditioner_flower_1l.png", "category": "laundry", "tag": None, "is_highlight": False},
    23: {"name": "Ополіскувач для прання Flower mystery, 2л", "price": 150.00, "desc": "Таємничий квітковий букет.", "img": "conditioner_flower_2l.png", "category": "laundry", "tag": None, "is_highlight": False},
    24: {"name": "Ополіскувач для прання Flower mystery, 5л", "price": 320.00, "desc": "Таємничий квітковий букет. Вигідний об'єм.", "img": "conditioner_flower_5l.png", "category": "laundry", "tag": None, "is_highlight": False},
    25: {"name": "Кондиціонер для прання Spring melody, 1л", "price": 90.00, "desc": "Ніжний аромат весняної свіжості.", "img": "conditioner_spring_1l.png", "category": "laundry", "tag": None, "is_highlight": False},
    26: {"name": "Кондиціонер для прання Spring melody, 2л", "price": 150.00, "desc": "Ніжний аромат весняної свіжості.", "img": "conditioner_spring_2l.png", "category": "laundry", "tag": None, "is_highlight": False},
    27: {"name": "Кондиціонер для прання Spring melody, 5л", "price": 320.00, "desc": "Ніжний аромат весняної свіжості. Вигідний об'єм.", "img": "conditioner_spring_5l.png", "category": "laundry", "tag": None, "is_highlight": False},
    28: {"name": "Кондиціонер для прання Magic Dream, 2л", "price": 150.00, "desc": "Чарівний, заспокійливий аромат.", "img": "conditioner_magic_2l.png", "category": "laundry", "tag": None, "is_highlight": False},
    29: {"name": "Кондиціонер для прання Wild and Fresh, 2л", "price": 150.00, "desc": "Свіжий та дикий аромат.", "img": "conditioner_wild_2l.png", "category": "laundry", "tag": None, "is_highlight": False},
    30: {"name": "Кондиціонер для прання Wild and Fresh, 5л", "price": 320.00, "desc": "Свіжий та дикий аромат. Вигідний об'єм.", "img": "conditioner_wild_5l.png", "category": "laundry", "tag": "Хіт", "is_highlight": False},
    31: {"name": "Кисневий відбілювач", "price": 120.00, "desc": "Потужний засіб для виведення плям та відбілювання.", "img": "oxy_bleach.png", "category": "laundry", "tag": None, "is_highlight": False},
    32: {"name": "Кисневий порошок 'Універсальний', 1кг", "price": 180.00, "desc": "Для чищення, прання та відбілювання.", "img": "oxy_powder_1kg.png", "category": "laundry", "tag": "Акція", "is_highlight": False, "price_old": 200.00},
    33: {"name": "Кисневий порошок 'Універсальний', 5кг", "price": 850.00, "desc": "Для чищення, прання та відбілювання. Мега-об'єм.", "img": "oxy_powder_5kg.png", "category": "laundry", "tag": None, "is_highlight": False},
    34: {"name": "Кисневий відбілювач, 5кг", "price": 550.00, "desc": "Ефективне відбілювання та видалення плям.", "img": "oxy_bleach_5kg.png", "category": "laundry", "tag": "Хіт", "is_highlight": False},
    35: {"name": "Набір еко-засобів для прання", "price": 499.00, "desc": "Гель, кондиціонер та кисневий порошок.", "img": "laundry_set_eco.png", "category": "laundry", "tag": "Набір", "is_highlight": False},
    36: {"name": "Набір безфосфатних кондиціонерів для прання, 3шт.", "price": 230.00, "desc": "Fresh Elegance, Velvet Air, Island Paradise.", "img": "conditioner_set_3.png", "category": "laundry", "tag": "Набір", "is_highlight": False},

    # ------------------ Секція 2: Для ванної та сантехніки (bath) ------------------
    37: {"name": "Засіб для зняття нальоту та іржі, 500 мл", "price": 95.00, "desc": "Ефективно видаляє вапняний наліт та іржу.", "img": "bath_limescale_500.png", "category": "bath", "tag": None, "is_highlight": False},
    38: {"name": "Засіб для миття сантехнічного обладнання, 500 мл", "price": 85.00, "desc": "Для щоденного догляду за ванною та раковиною.", "img": "bath_sanitary_500.png", "category": "bath", "tag": "Новинка", "is_highlight": False},
    39: {"name": "Очисник душових кабін та акрилу, 5л", "price": 390.00, "desc": "Професійний засіб, не пошкоджує акрил.", "img": "bath_shower_5l.png", "category": "bath", "tag": "Хіт", "is_highlight": True},
    40: {"name": "Очисник кранів та змішувачів, 5л", "price": 380.00, "desc": "Надає блиску та захищає від нальоту.", "img": "bath_taps_5l.png", "category": "bath", "tag": None, "is_highlight": False},
    41: {"name": "Засіб для миття унітазів, 1л", "price": 120.00, "desc": "Густий гель для максимальної чистоти.", "img": "bath_toilet_1l.png", "category": "bath", "tag": None, "is_highlight": False},
    42: {"name": "Засіб для миття унітазів, 5л", "price": 490.00, "desc": "Густий гель для максимальної чистоти. Вигідний об'єм.", "img": "bath_toilet_5l.png", "category": "bath", "tag": None, "is_highlight": False},
    43: {"name": "Засіб для миття унітазів з активним хлором, 1л", "price": 130.00, "desc": "Дезінфекція та ідеальна білизна.", "img": "bath_toilet_chlorine_1l.png", "category": "bath", "tag": "Акція", "is_highlight": False},
    44: {"name": "Соляна кислота (13%) від складних вапняних відкладень, 1л", "price": 180.00, "desc": "Для професійного видалення застарілого каменю.", "img": "bath_hcl_1l.png", "category": "bath", "tag": "Premium", "is_highlight": False},

    # ------------------ Секція 3: Для кухні, жировідведення та посуду (kitchen) ------------------
    45: {"name": "Засіб для видалення жиру, 500 мл", "price": 89.00, "desc": "Миттєво розчиняє жир на плитах та витяжках.", "img": "kitchen_fat_500.png", "category": "kitchen", "tag": "Хіт", "is_highlight": True},
    46: {"name": "Засіб для видалення жиру, 5л", "price": 410.00, "desc": "Миттєво розчиняє жир на плитах та витяжках. Вигідний об'єм.", "img": "kitchen_fat_5l.png", "category": "kitchen", "tag": None, "is_highlight": False},
    47: {"name": "Засіб для видалення пригарів (концентрат), 1л", "price": 150.00, "desc": "Легко видаляє запечені залишки та нагар.", "img": "kitchen_burnt_1l.png", "category": "kitchen", "tag": None, "is_highlight": False},
    48: {"name": "Засіб для видалення пригарів (концентрат), 5л", "price": 650.00, "desc": "Легко видаляє запечені залишки та нагар. Вигідний об'єм.", "img": "kitchen_burnt_5l.png", "category": "kitchen", "tag": None, "is_highlight": False},
    49: {"name": "Засіб для ручного миття посуду Алоє, 500мл", "price": 60.00, "desc": "М'яка формула з екстрактом Алоє Вера.", "img": "kitchen_dish_aloe_500.png", "category": "kitchen", "tag": None, "is_highlight": False},
    50: {"name": "Засіб для ручного миття посуду Алоє, 5л", "price": 250.00, "desc": "М'яка формула з екстрактом Алоє Вера. Вигідний об'єм.", "img": "kitchen_dish_aloe_5l.png", "category": "kitchen", "tag": None, "is_highlight": False},
    51: {"name": "Засіб для ручного миття посуду Лайм, 500мл", "price": 60.00, "desc": "Свіжий аромат Лайму, чудово піниться.", "img": "kitchen_dish_lime_500.png", "category": "kitchen", "tag": None, "is_highlight": False},
    52: {"name": "Засіб для ручного миття посуду Лайм, 5л", "price": 250.00, "desc": "Свіжий аромат Лайму, чудово піниться. Вигідний об'єм.", "img": "kitchen_dish_lime_5l.png", "category": "kitchen", "tag": None, "is_highlight": False},
    53: {"name": "Засіб для миття посуду Кавун-Диня, 2л", "price": 120.00, "desc": "Літній аромат, ефективне видалення жиру.", "img": "kitchen_dish_melon_2l.png", "category": "kitchen", "tag": None, "is_highlight": False},

    # ------------------ Секція 4: Для підлоги, скла та меблів (floor_furniture) ------------------
    54: {"name": "Засіб для чищення скла, 500 мл", "price": 75.00, "desc": "Без розводів. Ідеально для вікон та дзеркал.", "img": "floor_glass_500.png", "category": "floor_furniture", "tag": None, "is_highlight": False},
    55: {"name": "Засіб для чищення скла, 5л", "price": 320.00, "desc": "Без розводів. Ідеально для вікон та дзеркал. Вигідний об'єм.", "img": "floor_glass_5l.png", "category": "floor_furniture", "tag": "Хіт", "is_highlight": False},
    56: {"name": "Універсальний миючий засіб, 500 мл", "price": 85.00, "desc": "Для всіх типів поверхонь у домі.", "img": "floor_universal_500.png", "category": "floor_furniture", "tag": "Новинка", "is_highlight": False},
    57: {"name": "Засіб для миття підлоги (концентрат), 1л", "price": 110.00, "desc": "Концентрат для всіх типів підлогових покриттів.", "img": "floor_concentrate_1l.png", "category": "floor_furniture", "tag": None, "is_highlight": False},
    58: {"name": "Засіб для миття підлоги (концентрат), 5л", "price": 450.00, "desc": "Концентрат для всіх типів підлогових покриттів. Вигідний об'єм.", "img": "floor_concentrate_5l.png", "category": "floor_furniture", "tag": "Акція", "is_highlight": False},
    59: {"name": "Поліроль для меблів, 500мл", "price": 99.00, "desc": "Надає блиску та захищає від пилу.", "img": "floor_polish_500.png", "category": "floor_furniture", "tag": None, "is_highlight": False},
    60: {"name": "Поліроль для меблів, 5л", "price": 480.00, "desc": "Надає блиску та захищає від пилу. Вигідний об'єм.", "img": "floor_polish_5l.png", "category": "floor_furniture", "tag": None, "is_highlight": False},
    61: {"name": "Поліроль для шкіри та шкіряних поверхонь, 500мл", "price": 140.00, "desc": "Відновлює колір та м'якість шкіри.", "img": "floor_leather_500.png", "category": "floor_furniture", "tag": "Premium", "is_highlight": False},
    62: {"name": "Поліроль для шкіри та шкіряних поверхонь, 5л", "price": 650.00, "desc": "Відновлює колір та м'якість шкіри. Професійний об'єм.", "img": "floor_leather_5l.png", "category": "floor_furniture", "tag": None, "is_highlight": False},

    # ------------------ Секція 5: Спеціалізовані засоби, Набори та Аксесуари (special_sets) ------------------
    63: {"name": "Очисник стоків та каналізаційних труб, 1л", "price": 130.00, "desc": "Миттєво усуває засмічення.", "img": "special_drain_1l.png", "category": "special_sets", "tag": None, "is_highlight": False},
    64: {"name": "Засіб для видалення плісняви, 500мл", "price": 95.00, "desc": "Ефективна боротьба з грибком та пліснявою.", "img": "special_mold_500.png", "category": "special_sets", "tag": None, "is_highlight": False},
    65: {"name": "Засіб для видалення плісняви, 5л", "price": 450.00, "desc": "Ефективна боротьба з грибком та пліснявою. Вигідний об'єм.", "img": "special_mold_5l.png", "category": "special_sets", "tag": None, "is_highlight": False},
    66: {"name": "Засіб для очищення плям Lynks (одяг, килими, мякі меблі), 500мл", "price": 105.00, "desc": "Швидко видаляє плями з тканин та м'яких меблів.", "img": "special_stain_500.png", "category": "special_sets", "tag": "Новинка", "is_highlight": False},
    67: {"name": "Очисник килимового покриття та текстильних поверхонь, 5л", "price": 490.00, "desc": "Професійний концентрат для хімчистки.", "img": "special_carpet_5l.png", "category": "special_sets", "tag": None, "is_highlight": False},
    68: {"name": "Освіжувач повітря 'ранкова свіжість'", "price": 70.00, "desc": "Нейтралізує неприємні запахи.", "img": "special_air_fresh_morning.png", "category": "special_sets", "tag": None, "is_highlight": False},
    69: {"name": "Освіжувач повітря 'ранковий бриз'", "price": 70.00, "desc": "Нейтралізує неприємні запахи.", "img": "special_air_fresh_breeze.png", "category": "special_sets", "tag": None, "is_highlight": False},
    70: {"name": "Засіб для видалення бетону та миття після будівельних робіт, 1л", "price": 190.00, "desc": "Для очищення від цементу та вапна.", "img": "special_concrete_1l.png", "category": "special_sets", "tag": "Premium", "is_highlight": False},
    71: {"name": "Засіб для видалення бетону та миття після будівельних робіт, 5л", "price": 850.00, "desc": "Для очищення від цементу та вапна. Професійний об'єм.", "img": "special_concrete_5l.png", "category": "special_sets", "tag": None, "is_highlight": False},
    72: {"name": "Антисептик для рук та шкіри Sterilio A, 250 мл", "price": 75.00, "desc": "Дезінфекція та захист.", "img": "special_antiseptic_250.png", "category": "special_sets", "tag": None, "is_highlight": False},
    73: {"name": "Засіб для дезінфекції рук та поверхонь. Антисептик з дозатором Sterilio A, 1л", "price": 190.00, "desc": "Зручний дозатор, для регулярного використання.", "img": "special_antiseptic_1l.png", "category": "special_sets", "tag": None, "is_highlight": False},
    74: {"name": "Засіб для дезінфекції, антисептик Sterilio A, 5л", "price": 850.00, "desc": "Для дезінфекції великих площ. Вигідний об'єм.", "img": "special_antiseptic_5l.png", "category": "special_sets", "tag": None, "is_highlight": False},
    75: {"name": "Розпилювач курковий тригер (для засобів Lynks)", "price": 25.00, "desc": "Якісний розпилювач для пляшок 0,5-1л.", "img": "special_trigger.png", "category": "special_sets", "tag": None, "is_highlight": False},
    76: {"name": "Набір для прибирання за супер-ціною (7 засобів)", "price": 799.00, "desc": "Повний комплект для ідеальної чистоти.", "img": "set_general.png", "category": "special_sets", "tag": "Набір", "is_highlight": False},
    77: {"name": "Набір ТОП-3 засоба для кухні + ПОДАРУНОК", "price": 299.00, "desc": "Жироудалитель, засіб для посуду та пригарів.", "img": "set_kitchen_top3.png", "category": "special_sets", "tag": "Набір", "is_highlight": False},
    78: {"name": "Набір 'Чиста кухня'", "price": 450.00, "desc": "Розширений комплект для підтримки чистоти на кухні.", "img": "set_kitchen_clean.png", "category": "special_sets", "tag": "Набір", "is_highlight": False},

    # ------------------ Секція 6: Рідке мило та Гелі для душу Lynks (body_care) ------------------
    79: {"name": "Рідке мило 'Конвалія', 500мл", "price": 60.00, "desc": "Ніжний аромат конвалії та догляд за шкірою.", "img": "body_soap_lily_500.png", "category": "body_care", "tag": "Новинка", "is_highlight": False},
    80: {"name": "Рідке мило 'Парфум', 500 мл", "price": 65.00, "desc": "Насичений парфумований аромат.", "img": "body_soap_parfum_500.png", "category": "body_care", "tag": "Хіт", "is_highlight": False},
    81: {"name": "Рідке мило та гель для душу 'Парфум', 2л", "price": 140.00, "desc": "Великий об'єм для економії.", "img": "body_soap_parfum_2l.png", "category": "body_care", "tag": None, "is_highlight": False},
    82: {"name": "Рідке мило та гель для душу 'Парфум', 5л", "price": 280.00, "desc": "Для професійного використання та великої родини.", "img": "body_soap_parfum_5l.png", "category": "body_care", "tag": None, "is_highlight": False},
    83: {"name": "Рідке мило та гель для душу 'Грейпфрут з мандарином', 2л", "price": 130.00, "desc": "Цитрусова свіжість та бадьорість.", "img": "body_soap_citrus_2l.png", "category": "body_care", "tag": None, "is_highlight": False},
    84: {"name": "Рідке мило та гель для душу 'Грейпфрут з мандарином', 5л", "price": 260.00, "desc": "Цитрусова свіжість та бадьорість. Вигідний об'єм.", "img": "body_soap_citrus_5l.png", "category": "body_care", "tag": None, "is_highlight": False},
    85: {"name": "Рідке мило та гель для душу 'Гранат', 2л", "price": 130.00, "desc": "Солодкий та насичений аромат.", "img": "body_soap_pomegranate_2l.png", "category": "body_care", "tag": None, "is_highlight": False},
    86: {"name": "Рідке мило та гель для душу 'М'ята', 2л", "price": 130.00, "desc": "Освіжаючий ефект з ароматом м'яти.", "img": "body_soap_mint_2l.png", "category": "body_care", "tag": None, "is_highlight": False},
    87: {"name": "Рідке мило та гель для душу 'Конвалія', 2л", "price": 130.00, "desc": "Ніжний та заспокійливий аромат.", "img": "body_soap_lily_2l.png", "category": "body_care", "tag": None, "is_highlight": False},
    88: {"name": "Рідке мило та гель для душу 'Конвалія', 5л", "price": 260.00, "desc": "Для професійного використання та великої родини.", "img": "body_soap_lily_5l.png", "category": "body_care", "tag": None, "is_highlight": False},
    
    # ... (Інші категорії) ...
    
    101: {"name": "Крем для рук 'Весна'", "price": 85.00, "desc": "Живильний крем для сухої шкіри.", "img": "vesna_cream.jpg", "category": "vesna", "tag": None, "is_highlight": False},
    201: {"name": "Омивач скла 0°С літній EXOL, 5л", "price": 150.00, "desc": "Ефективно видаляє бруд, не залишаючи розводів.", "img": "auto_washer_0c_5l.png", "category": "auto_care", "tag": "Акція", "is_highlight": False},
    202: {"name": "Омивач скла -12°С EXOL, 5л", "price": 250.00, "desc": "Морозостійкий омивач.", "img": "auto_washer_12c_5l.png", "category": "auto_care", "tag": None, "is_highlight": False},
    203: {"name": "Омивач скла -18°С EXOL, 5л", "price": 250.00, "desc": "Морозостійкий омивач.", "img": "auto_washer_18c_5l.png", "category": "auto_care", "tag": None, "is_highlight": False},
    204: {"name": "Омивач скла -80°С EXOL, 1 л", "price": 250.00, "desc": "Концентрат.", "img": "auto_washer_80c_1l.png", "category": "auto_care", "tag": "Premium", "is_highlight": False},
    205: {"name": "Антифриз G12 червоний 'Premium Rot -35' EXOL, 1л", "price": 250.00, "desc": "Для двигунів.", "img": "auto_antifreeze_g12_1l.png", "category": "auto_care", "tag": None, "is_highlight": False},
    206: {"name": "Антифриз G11 блакитний 'Premium Blau -35' EXOL, 1л", "price": 250.00, "desc": "Для двигунів.", "img": "auto_antifreeze_g11_1l.png", "category": "auto_care", "tag": None, "is_highlight": False},
    207: {"name": "Очисник двигуна EXOL, 500 мл", "price": 250.00, "desc": "Для двигунів.", "img": "auto_engine_cleaner_500.png", "category": "auto_care", "tag": None, "is_highlight": False},
    208: {"name": "Автошампунь (конц. 1:200) EXOL, 500 мл", "price": 250.00, "desc": "Для миття.", "img": "auto_shampoo_500.png", "category": "auto_care", "tag": None, "is_highlight": False},
    209: {"name": "Автошампунь з воском (конц. 1:200) EXOL, 500 мл", "price": 250.00, "desc": "Для миття та блиску.", "img": "auto_shampoo_wax_500.png", "category": "auto_care", "tag": None, "is_highlight": False},
    210: {"name": "Засіб для видалення залишків комах EXOL, 500 мл", "price": 250.00, "desc": "Для авто.", "img": "auto_bugs_remover_500.png", "category": "auto_care", "tag": None, "is_highlight": False},
    211: {"name": "Засіб для миття віконного скла EXOL, 500 мл", "price": 250.00, "desc": "Для авто.", "img": "auto_glass_cleaner_500.png", "category": "auto_care", "tag": None, "is_highlight": False},
    212: {"name": "Засіб для хімчистки салону EXOL, 500 мл", "price": 250.00, "desc": "Для салону.", "img": "auto_interior_cleaner_500.png", "category": "auto_care", "tag": None, "is_highlight": False},
    213: {"name": "Поліроль панелей приладів та пластику EXOL, 500 мл", "price": 250.00, "desc": "Для салону.", "img": "auto_dashboard_polish_500.png", "category": "auto_care", "tag": None, "is_highlight": False},
    214: {"name": "Поліроль для шин. Відновлення чорного кольору EXOL, 500 мл", "price": 250.00, "desc": "Для шин.", "img": "auto_tire_polish_500.png", "category": "auto_care", "tag": None, "is_highlight": False},
    215: {"name": "Розморожувач скла та замків EXOL, 500 мл", "price": 250.00, "desc": "Для авто.", "img": "auto_deicer_500.png", "category": "auto_care", "tag": None, "is_highlight": False},
    216: {"name": "Поліроль EXOL, 1л", "price": 250.00, "desc": "Для кузова.", "img": "auto_polish_1l.png", "category": "auto_care", "tag": None, "is_highlight": False},
    217: {"name": "Поліроль EXOL, 5л", "price": 250.00, "desc": "Для кузова.", "img": "auto_polish_5l.png", "category": "auto_care", "tag": None, "is_highlight": False},
    218: {"name": "Активна піна 'Premium' EXOL (1:20), 1л", "price": 250.00, "desc": "Для мийки.", "img": "auto_foam_premium_1l.png", "category": "auto_care", "tag": None, "is_highlight": False},
    219: {"name": "Активна піна 'Premium PLUS' EXOL (1:30) концентрат, 1 л", "price": 250.00, "desc": "Для мийки.", "img": "auto_foam_plus_1l.png", "category": "auto_care", "tag": None, "is_highlight": False},
    220: {"name": "Активна піна 'Premium PINK' EXOL (1:30) концентрат, 1 л", "price": 250.00, "desc": "Для мийки.", "img": "auto_foam_pink_1l.png", "category": "auto_care", "tag": None, "is_highlight": False},
    221: {"name": "Активна піна 'Premium PINK' EXOL (1:30) концентрат, 20 л", "price": 250.00, "desc": "Для мийки.", "img": "auto_foam_pink_20l.png", "category": "auto_care", "tag": None, "is_highlight": False},
    222: {"name": "Активна піна 'Premium' EXOL (1:20), 20 л", "price": 250.00, "desc": "Для мийки.", "img": "auto_foam_premium_20l.png", "category": "auto_care", "tag": None, "is_highlight": False},
    223: {"name": "Активна піна 'Premium PLUS' EXOL (1:30) концентрат, 20 л", "price": 250.00, "desc": "Для мийки.", "img": "auto_foam_plus_20l.png", "category": "auto_care", "tag": None, "is_highlight": False},
    224: {"name": "Сушильний віск EXOL (1:200), 1л", "price": 250.00, "desc": "Для авто.", "img": "auto_drying_wax_1l.png", "category": "auto_care", "tag": None, "is_highlight": False},
    225: {"name": "Сушильний віск EXOL, 20л", "price": 250.00, "desc": "Для авто.", "img": "auto_drying_wax_20l.png", "category": "auto_care", "tag": None, "is_highlight": False},
    226: {"name": "Засіб для очищення дисків та ковпаків EXOL, 10 л", "price": 250.00, "desc": "Для авто.", "img": "auto_wheel_cleaner_10l.png", "category": "auto_care", "tag": None, "is_highlight": False},
    227: {"name": "Рідкий віск EXOL, 5л", "price": 250.00, "desc": "Для авто.", "img": "auto_liquid_wax_5l.png", "category": "auto_care", "tag": None, "is_highlight": False},
    228: {"name": "ADBLUE NOXy, 10кг", "price": 250.00, "desc": "Для авто.", "img": "auto_adblue_10kg.png", "category": "auto_care", "tag": None, "is_highlight": False},
    229: {"name": "Поліроль для шкіри та шкіряних поверхонь, 500мл", "price": 250.00, "desc": "Для авто.", "img": "auto_leather_polish_500.png", "category": "auto_care", "tag": None, "is_highlight": False},
    230: {"name": "Поліроль для шкіри та шкіряних поверхонь, 5л", "price": 250.00, "desc": "Для авто.", "img": "auto_leather_polish_5l.png", "category": "auto_care", "tag": None, "is_highlight": False},
}


HIGHLIGHTS = [1, 2, 3, 39, 45] # Продукти, які будуть показані на головній сторінці (ID)

CATEGORY_TITLES = {
    "laundry": "Пральні засоби та догляд за тканинами",
    "bath": "Для ванної та сантехніки",
    "kitchen": "Для кухні, жировідведення та посуду",
    "floor_furniture": "Для підлоги, скла та меблів",
    "special_sets": "Спеціалізовані засоби, Набори та Аксесуари",
    "body_care": "Рідке мило та Гелі для душу",
    "auto_care": "Автохімія та Автокосметика",
    "vesna": "Vesna: Натуральна косметика",
}

# =========================================================================
# ДОПОМІЖНІ ФУНКЦІЇ
# =========================================================================

def render_highlight_products(products_data):
    """Генерує HTML для відображення актуальних пропозицій."""
    highlights_html = ""
    
    for product_id in HIGHLIGHTS:
        product = products_data.get(product_id)
        if product:
            # Створення копії для уникнення змін у PRODUCTS
            prod_copy = product.copy()
            prod_copy['id'] = str(product_id)
            
            # 🔴 ЗМІНЕНО: Коректне формування шляху для static
            image_path = product['img']
            prod_copy['image'] = 'images/' + image_path

            # Обробка ціни та тегу
            price_old_html = f'<span class="old-price">₴{prod_copy.get("price_old", 0) :.2f}</span>' if prod_copy.get("price_old") else ''
            tag_html = f'<div class="product-tag">{prod_copy.get("tag")}</div>' if prod_copy.get("tag") else ''

            # Використовуємо url_for для коректного шляху до static
            img_url = url_for('static', filename=prod_copy['image'])

            highlights_html += f"""
                <div class="product-highlight" data-id="{prod_copy['id']}">
                    {tag_html}
                    <div class="product-img-box">
                        <img src="{img_url}" alt="{prod_copy['name']}" />
                    </div>
                    <div class="highlight-details">
                        <div class="highlight-title">{prod_copy['name']}</div>
                        <div class="highlight-desc">{prod_copy['desc']}</div>
                        <div class="highlight-price">
                            {price_old_html}
                            ₴{prod_copy['price'] :.2f}
                        </div>
                    </div>
                    <button class="btn-sm add-to-cart-btn" data-id="{prod_copy['id']}">В кошик</button>
                </div>
            """
    return highlights_html

def get_cart_count():
    """Повертає загальну кількість товарів у кошику."""
    return sum(session.get('cart', {}).values())

# =========================================================================
# 🔴 МАРШРУТИ ДЛЯ КОШИКА (Backend Logic)
# =========================================================================

@app.before_request
def initialize_cart():
    """Ініціалізує кошик у сесії, якщо він ще не існує."""
    if 'cart' not in session:
        session['cart'] = {}

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    """Обробляє POST-запит для додавання товару до кошика (з каталогу)."""
    product_id = request.form.get('product_id')
    
    if product_id and product_id.isdigit():
        prod_id = int(product_id)
        if prod_id in PRODUCTS:
            product_id_str = str(prod_id)
            session['cart'][product_id_str] = session['cart'].get(product_id_str, 0) + 1
            session.modified = True 
            
            total_items = get_cart_count()
            return jsonify({'success': True, 'total_items': total_items})
            
    return jsonify({'success': False, 'message': 'Недійсний ID товару'}), 400

@app.route('/update_cart', methods=['POST'])
def update_cart():
    """Обробляє POST-запит для зміни кількості товару в кошику (+/-) або видалення."""
    
    product_id = request.form.get('product_id')
    action = request.form.get('action') # 'increase', 'decrease' або 'remove'
    
    if not product_id or not product_id.isdigit():
        return jsonify({'success': False, 'message': 'Недійсний ID товару'}), 400
        
    product_id_str = str(int(product_id))
    current_cart = session.get('cart', {})
    current_quantity = current_cart.get(product_id_str, 0)
    
    product = PRODUCTS.get(int(product_id))
    if not product:
        return jsonify({'success': False, 'message': 'Товар не знайдено'}), 404

    new_quantity = current_quantity
    
    if action == 'increase':
        new_quantity = current_quantity + 1
        current_cart[product_id_str] = new_quantity
    elif action == 'decrease':
        new_quantity = max(0, current_quantity - 1)
        if new_quantity > 0:
            current_cart[product_id_str] = new_quantity
        else:
            if product_id_str in current_cart:
                del current_cart[product_id_str]
    elif action == 'remove':
        if product_id_str in current_cart:
            del current_cart[product_id_str]
        new_quantity = 0 
    else:
        return jsonify({'success': False, 'message': 'Невідома дія'}), 400

    session['cart'] = current_cart
    session.modified = True 

    # Перераховуємо нову загальну кількість товарів у кошику
    total_items = get_cart_count()
    
    # Розраховуємо нову підсумкову суму для цього товару
    new_subtotal = (product['price'] * current_cart.get(product_id_str, 0))
    
    # Розраховуємо нову загальну суму кошика
    total_price = sum(PRODUCTS.get(int(pid))['price'] * qty for pid, qty in current_cart.items() if PRODUCTS.get(int(pid)))
    
    return jsonify({
        'success': True, 
        'total_items': total_items, 
        'new_quantity': current_cart.get(product_id_str, 0),
        'new_subtotal': f'₴{new_subtotal:.2f}', # Формат для відображення
        'total_price': f'₴{total_price:.2f}', # Формат для відображення
        'product_id': product_id_str
    })


@app.route('/cart')
def view_cart():
    """Відображає вміст кошика користувача."""
    cart_data = session.get('cart', {})
    detailed_cart_items = []
    total_price = 0
    
    for product_id_str, quantity in cart_data.items():
        product_id = int(product_id_str)
        product = PRODUCTS.get(product_id)
        
        if product and quantity > 0:
            subtotal = product['price'] * quantity
            total_price += subtotal
            
            # 🔴 ЗМІНЕНО: Коректне формування шляху для static
            detailed_cart_items.append({
                'id': product_id_str,
                'name': product['name'],
                'price': product['price'],
                'quantity': quantity,
                'subtotal': subtotal,
                # Тут додаємо images/ до назви файлу з PRODUCTS
                'image': 'images/' + product['img'] 
            })

    cart_count = get_cart_count()
    
    return render_template(
        'index.html', 
        title='Кошик', 
        products=None, 
        highlights=None, 
        category_titles=CATEGORY_TITLES,
        cart_count=cart_count,
        cart_items=detailed_cart_items,
        total_price=total_price
    )

# =========================================================================
# ОСНОВНІ МАРШРУТИ
# =========================================================================

@app.route('/')
def index():
    products_list = []
    highlights_html = render_highlight_products(PRODUCTS)
    cart_count = get_cart_count()
    
    return render_template(
        'index.html', 
        products=products_list, 
        highlights=highlights_html,
        category_titles=CATEGORY_TITLES, 
        cart_count=cart_count, 
        cart_items=None, 
        total_price=0
    )

@app.route('/catalog/<category_name>')
def catalog(category_name):
    
    filtered_products = []
    for product_id, product in PRODUCTS.items():
        if product.get('category') == category_name:
            prod_copy = product.copy()
            prod_copy['id'] = str(product_id)
            
            # 🔴 ЗМІНЕНО: Коректне формування шляху для static
            # Тут додаємо images/ до назви файлу з PRODUCTS
            prod_copy['image'] = 'images/' + product['img']
            
            filtered_products.append(prod_copy)

    page_title = CATEGORY_TITLES.get(category_name, 'Каталог товарів')
    cart_count = get_cart_count()

    return render_template(
        'index.html', 
        products=filtered_products, 
        highlights='', 
        title=page_title,
        category_titles=CATEGORY_TITLES,
        cart_count=cart_count, 
        cart_items=None, 
        total_price=0
    )

if __name__ == '__main__':
    # 🌟 ВИПРАВЛЕНО: Використовуємо '0.0.0.0', щоб дозволити підключення з локальної мережі.
    # Додаток буде доступний на http://ВАШ_ЛОКАЛЬНИЙ_IP:5000/
    app.run(debug=True, host='0.0.0.0', port=5000)