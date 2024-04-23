import logging
import os
import random

import requests
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler, ContextTypes

load_dotenv()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

reply_keyboard1 = [['/start']]
reply_keyboard2 = [["Начать игру"], ["Помощь"], ["Баланс"]]
reply_keyboard3 = [['Да', 'Нет']]

money_to_qwest = [0, 500, 1000, 2000, 3000, 5000, 10000, 15000, 25000, 50000, 100000, 200000, 400000, 800000, 1500000,
                  3000000]

markup = ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=False)
markup2 = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=False)
murkup3 = ReplyKeyboardMarkup(reply_keyboard3, one_time_keyboard=False)


def get_qwest(level, ids):
    request = f'http://127.0.0.1:8000/api/quest/{level}'
    params = {'ids': ids}
    responce = requests.get(request, json=params).json()
    logger.info(str(responce))
    if 'error' in responce:
        return 'error'
    return responce


def refactor_user(user_id, money):
    request = f'http://127.0.0.1:8000/api/user/{user_id}'
    params = {'money': money}
    logger.info(str(requests.post(request, json=params)))


def get_cat():
    a = requests.get('https://api.thecatapi.com/v1/images/search').json()[0]['url']
    while a[-4:] != '.jpg':
        a = requests.get('https://api.thecatapi.com/v1/images/search').json()[0]['url']
    return requests.get(a).content


def get_user(user_id):
    request = f'http://127.0.0.1:8000/api/user/{user_id}'
    a = requests.get(request).json()
    logger.info(str(a))
    return a['money']


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.full_name}! Это игра кто хочет стать миллионером. Правила игры очень просты.\n"
        f"Вам задаётся вопрос и 4 варианта ответа на него вы должны выбрать правильный ответ. Если вы ошибётесь"
        f' то вы выбывете из игры. Также у вас есть несколько подсказок, а именно "50/50" - убирает 2 неверных ответа,'
        f' "Сменить вопрос" - меняет вопрос, "Второй шанс" - даёт возможность 1 раз ответить на вопрос неправильно.'
        f' Введите "Начать игру" чтобы играть, "Помощь", чтобы прочитать инструкцию или "Баланс", '
        f'чтобы узнать свой счёт.', reply_markup=markup2)
    return 4


async def choice_before_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == 'Начать игру':
        user = update.effective_user
        context.user_data['qwest_num'] = 1
        context.user_data['ids'] = []
        context.user_data['helps'] = [['Сменить вопрос'], ['50/50', 'Второй шанс'], ['назад']]
        context.user_data['second_chance'] = False
        # тут происходит запрос на вопрос
        n = get_qwest((context.user_data['qwest_num'] + 2) // 3, context.user_data['ids'])
        if n == 'error':
            await update.message.reply_text(f"Вопросы закончились.")
            await update.message.reply_text(
                f'Вы вывиграли {money_to_qwest[context.user_data["qwest_num"] - 1]} рублей.\n'
                f'До новых встреч.')
            refactor_user(user.id, money_to_qwest[context.user_data["qwest_num"] - 1])
            context.user_data.clear()
            return 4
        context.user_data['ans'] = n['answers']
        context.user_data['qwest_type'] = n['type']
        context.user_data['ids'].append(n['id'])
        context.user_data['r_ans'] = n['r_answer']
        context.user_data['qwest'] = n['text']
        context.user_data['photo'] = 'API/' + str(n['photo'])
        num_to_ans = [[str(i) for i in range(1, len(context.user_data['ans']) + 1)], ['Подсказки', 'Правила игры']]
        murkup_ans = ReplyKeyboardMarkup(num_to_ans, one_time_keyboard=False)
        q = '\n'.join([str(i + 1) + ') ' + context.user_data['ans'][i] for i in range(len(context.user_data['ans']))])
        await update.message.reply_text(f"Привет {user.full_name}! Вы попали на передачу кто хочет стать миллионером.")
        if context.user_data['qwest_type'] == 'text':
            await update.message.reply_text(f"Вопрос номер {context.user_data['qwest_num']}:\n"
                                            f"{context.user_data['qwest']}\n\nВарианты ответа:\n{q}",
                                            reply_markup=murkup_ans)
        elif context.user_data['qwest_type'] == 'photo':
            await update.message.reply_text(f"Вопрос номер {context.user_data['qwest_num']}:\n"
                                            f"{context.user_data['qwest']}", reply_markup=murkup_ans)
            await update.message.reply_photo(open(context.user_data['photo'], 'rb'))
            await update.message.reply_text(f"Варианты ответа:\n{q}")
        return 1
    elif update.message.text == 'Помощь':
        await update.message.reply_text(
            f"Правила игры: "
            f"Вам задаётся вопрос и 4 варианта ответа на него вы должны выбрать правильный ответ. Если вы ошибётесь"
            f' то вы выбывете из игры. Также у вас есть несколько подсказок, а именно "50/50" - убирает 2 неверных ответа,'
            f' "Сменить вопрос" - меняет вопрос, "Второй шанс" - даёт возможность 1 раз ответить на вопрос неправильно.'
            f' Введите "Начать игру" чтобы играть, "Помощь", чтобы прочитать инструкцию или "Баланс", '
            f'чтобы узнать свой счёт. \n'
            f'за каждый правильно отвеченный вопрос вы получаете деньги(деньги за вопросы не сумируются):\n'
            f'<b><i>№ Вопроса      Количество денег</i></b>\n'
            f'1                         500\n'
            f'2                         1000\n'
            f'3                         2000\n'
            f'4                         3000\n'
            f'5                         <b><i>5000</i></b>\n'
            f'6                         10000\n'
            f'7                         15000\n'
            f'8                         25000\n'
            f'9                         50000\n'
            f'10                       <b><i>100000</i></b>\n'
            f'11                       200000\n'
            f'12                       400000\n'
            f'13                       800000\n'
            f'14                       1500000\n'
            f'15                       <b><i>3000000</i></b>\n'
            f'жирным обозначена несгораемая сумма.', parse_mode="html")
        return 4
    elif update.message.text == "Баланс":
        user = update.effective_user
        money = get_user(user.id)
        await update.message.reply_text(f"Ваш счёт: {money}")
        return 4


async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    helps_murkup = ReplyKeyboardMarkup(context.user_data['helps'], one_time_keyboard=False)
    if update.message.text not in ['1', '2', '3', '4', 'Подсказки', 'Правила игры']:
        await update.message.reply_text('Выведете число от 1 до 4 - вариант ответа или попросите подсказку,'
                                        ' введя слово "Подсказки"')
        return 1

    if update.message.text == 'Подсказки':
        await update.message.reply_text('Выберете одну из подсказок: Второй шанс, 50/50, Сменить вопрос или '
                                        'вернитесь обратно, написав слово "назад"', reply_markup=helps_murkup)
        return 3

    if update.message.text == 'Правила игры':
        await update.message.reply_text(
            f"Правила игры: "
            f"Вам задаётся вопрос и 4 варианта ответа на него вы должны выбрать правильный ответ. Если вы ошибётесь"
            f' то вы выбывете из игры. Также у вас есть несколько подсказок, а именно "50/50" - убирает 2 неверных ответа,'
            f' "Сменить вопрос" - меняет вопрос, "Второй шанс" - даёт возможность 1 раз ответить на вопрос неправильно.'
            f' Введите "Начать игру" чтобы играть, "Помощь", чтобы прочитать инструкцию или "Баланс", '
            f'чтобы узнать свой счёт. \n'
            f'за каждый правильно отвеченный вопрос вы получаете деньги(деньги за вопросы не сумируются):\n'
            f'<b><i>№ Вопроса      Количество денег</i></b>\n'
            f'1                         500\n'
            f'2                         1000\n'
            f'3                         2000\n'
            f'4                         3000\n'
            f'5                         <b><i>5000</i></b>\n'
            f'6                         10000\n'
            f'7                         15000\n'
            f'8                         25000\n'
            f'9                         50000\n'
            f'10                       <b><i>100000</i></b>\n'
            f'11                       200000\n'
            f'12                       400000\n'
            f'13                       800000\n'
            f'14                       1500000\n'
            f'15                       <b><i>3000000</i></b>\n'
            f'жирным обозначена несгораемая сумма.', parse_mode="html")
        q = '\n'.join(
            [str(i + 1) + ') ' + context.user_data['ans'][i] for i in range(len(context.user_data['ans']))])
        await update.message.reply_text(f"Вопрос номер {context.user_data['qwest_num']}:\n"
                                        f"{context.user_data['qwest']}\n\nВарианты ответа:\n{q}")
        return 1

    if context.user_data['ans'][int(update.message.text) - 1] != context.user_data['r_ans']:
        await update.message.reply_text('К сожалению это неправильный ответ.')
        if context.user_data['second_chance']:
            context.user_data['second_chance'] = False
            await update.message.reply_text('Второй шанс.')
            del context.user_data['ans'][int(update.message.text) - 1]
            num_to_ans = [[str(i) for i in range(1, len(context.user_data['ans']) + 1)], ['Подсказки', 'Правила игры']]
            murkup_ans = ReplyKeyboardMarkup(num_to_ans, one_time_keyboard=False)
            q = '\n'.join(
                [str(i + 1) + ') ' + context.user_data['ans'][i] for i in range(len(context.user_data['ans']))])
            await update.message.reply_text(f"Вопрос номер {context.user_data['qwest_num']}:\n"
                                            f"{context.user_data['qwest']}\n\nВарианты ответа:\n{q}",
                                            reply_markup=murkup_ans)
            return 1

        await update.message.reply_text(
            f'Вы выиграли '
            f'{money_to_qwest[context.user_data["qwest_num"] - (context.user_data["qwest_num"] % 5)]} рублей,\n'
            f'Прощайте.', reply_markup=markup2)
        refactor_user(user.id, money_to_qwest[context.user_data["qwest_num"] - (context.user_data["qwest_num"] % 5)])
        context.user_data.clear()
        return 4
    if context.user_data['qwest_num'] == 15:
        await update.message.reply_text(f'Поздравляю вы победили!\n'
                                        f'Вы вывиграли {money_to_qwest[context.user_data["qwest_num"]]} рублей.\n'
                                        f'До новых встреч.')
        await update.message.reply_photo(get_cat())
        refactor_user(user.id, money_to_qwest[context.user_data["qwest_num"]])
        context.user_data.clear()
        return 4
    context.user_data['second_chance'] = False
    await update.message.reply_text('И это правильный ответ.')
    await update.message.reply_text(f'хотите продолжить?', reply_markup=murkup3)
    return 2


async def choice_to_play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if update.message.text not in ['Да', 'Нет']:
        await update.message.reply_text('Я вас не понял, просто напишите "ДА" или "Нет"')
        return 2
    elif update.message.text == 'Нет':
        await update.message.reply_text(f"Поздравляю вы выиграли {money_to_qwest[context.user_data['qwest_num']]}",
                                        reply_markup=markup2)
        refactor_user(user.id, money_to_qwest[context.user_data["qwest_num"]])
        context.user_data.clear()
        return 4
    else:
        context.user_data['qwest_num'] += 1
        # тут происходит запрос на вопрос
        n = get_qwest((context.user_data['qwest_num'] + 2) // 3, context.user_data['ids'])
        if n == 'error':
            await update.message.reply_text(f"Вопросы закончились.")
            await update.message.reply_text(
                f'Вы вывиграли {money_to_qwest[context.user_data["qwest_num"] - 1]} рублей.\n'
                f'До новых встреч.')
            refactor_user(user.id, money_to_qwest[context.user_data["qwest_num"]])
            context.user_data.clear()
            return 4
        context.user_data['ans'] = n['answers']
        context.user_data['qwest_type'] = n['type']
        context.user_data['ids'].append(n['id'])
        context.user_data['r_ans'] = n['r_answer']
        context.user_data['qwest'] = n['text']
        context.user_data['photo'] = 'API/' + str(n['photo'])
        num_to_ans = [[str(i) for i in range(1, len(context.user_data['ans']) + 1)], ['Подсказки', 'Правила игры']]
        murkup_ans = ReplyKeyboardMarkup(num_to_ans, one_time_keyboard=False)
        q = '\n'.join([str(i + 1) + ') ' + context.user_data['ans'][i] for i in range(len(context.user_data['ans']))])
        if context.user_data['qwest_type'] == 'text':
            await update.message.reply_text(f"Вопрос номер {context.user_data['qwest_num']}:\n"
                                            f"{context.user_data['qwest']}\n\nВарианты ответа:\n{q}",
                                            reply_markup=murkup_ans)
        elif context.user_data['qwest_type'] == 'photo':
            await update.message.reply_text(f"Вопрос номер {context.user_data['qwest_num']}:\n"
                                            f"{context.user_data['qwest']}", reply_markup=murkup_ans)
            await update.message.reply_photo(open(context.user_data['photo'], 'rb'))
            await update.message.reply_text(f"Варианты ответа:\n{q}")
        return 1


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=markup
    )


async def helps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if update.message.text == 'Сменить вопрос':
        if len(context.user_data['helps']) == 1:
            return 3
        if 'Сменить вопрос' in context.user_data['helps'][0]:
            context.user_data['helps'][0].remove('Сменить вопрос')
        else:
            return 3
        if not all(context.user_data['helps']):
            context.user_data['helps'].remove([])
        # тут происходит запрос на вопрос
        n = get_qwest((context.user_data['qwest_num'] + 2) // 3, context.user_data['ids'])
        if n == 'error':
            await update.message.reply_text(f"Вопросы закончились.")
            await update.message.reply_text(
                f'Вы вывиграли {money_to_qwest[context.user_data["qwest_num"] - 1]} рублей.\n'
                f'До новых встреч.')
            refactor_user(user.id, money_to_qwest[context.user_data["qwest_num"] - 1])
            context.user_data.clear()
            return ConversationHandler.END
        context.user_data['ans'] = n['answers']
        context.user_data['qwest_type'] = n['type']
        context.user_data['ids'].append(n['id'])
        context.user_data['r_ans'] = n['r_answer']
        context.user_data['qwest'] = n['text']
        context.user_data['photo'] = 'API/' + str(n['photo'])
        num_to_ans = [[str(i) for i in range(1, len(context.user_data['ans']) + 1)], ['Подсказки', 'Правила игры']]
        murkup_ans = ReplyKeyboardMarkup(num_to_ans, one_time_keyboard=False)
        q = '\n'.join([str(i + 1) + ') ' + context.user_data['ans'][i] for i in range(len(context.user_data['ans']))])
        if context.user_data['qwest_type'] == 'text':
            await update.message.reply_text(f"Вопрос номер {context.user_data['qwest_num']}:\n"
                                            f"{context.user_data['qwest']}\n\nВарианты ответа:\n{q}",
                                            reply_markup=murkup_ans)
        elif context.user_data['qwest_type'] == 'photo':
            await update.message.reply_text(f"Вопрос номер {context.user_data['qwest_num']}:\n"
                                            f"{context.user_data['qwest']}", reply_markup=murkup_ans)
            await update.message.reply_photo(open(context.user_data['photo'], 'rb'))
            await update.message.reply_text(f"Варианты ответа:\n{q}")
        return 1
    elif update.message.text == '50/50':
        if len(context.user_data['helps']) == 1:
            return 3
        if '50/50' in context.user_data['helps'][0]:
            context.user_data['helps'][0].remove('50/50')
        elif '50/50' in context.user_data['helps'][1]:
            context.user_data['helps'][1].remove('50/50')
        else:
            return 3
        if not all(context.user_data['helps']):
            context.user_data['helps'].remove([])
        a = random.choice(context.user_data['ans'])
        while a == context.user_data['r_ans']:
            a = random.choice(context.user_data['ans'])
        context.user_data['ans'] = [a, context.user_data['r_ans']]
        random.shuffle(context.user_data['ans'])
        num_to_ans = [[str(i) for i in range(1, len(context.user_data['ans']) + 1)], ['Подсказки', 'Правила игры']]
        murkup_ans = ReplyKeyboardMarkup(num_to_ans, one_time_keyboard=False)
        q = '\n'.join([str(i + 1) + ') ' + context.user_data['ans'][i] for i in range(len(context.user_data['ans']))])
        await update.message.reply_text(f"Вопрос номер {context.user_data['qwest_num']}:\n"
                                        f"{context.user_data['qwest']}\n\nВарианты ответа:\n{q}",
                                        reply_markup=murkup_ans)
        return 1
    elif update.message.text == 'Второй шанс':
        if len(context.user_data['helps']) == 1:
            return 3
        if 'Второй шанс' in context.user_data['helps'][0]:
            context.user_data['helps'][0].remove('Второй шанс')
        elif 'Второй шанс' in context.user_data['helps'][1]:
            context.user_data['helps'][1].remove('Второй шанс')
        else:
            return 3
        if not all(context.user_data['helps']):
            context.user_data['helps'].remove([])
        context.user_data['second_chance'] = True
        num_to_ans = [[str(i) for i in range(1, len(context.user_data['ans']) + 1)], ['Подсказки', 'Правила игры']]
        murkup_ans = ReplyKeyboardMarkup(num_to_ans, one_time_keyboard=False)
        q = '\n'.join([str(i + 1) + ') ' + context.user_data['ans'][i] for i in range(len(context.user_data['ans']))])
        await update.message.reply_text(f"Вопрос номер {context.user_data['qwest_num']}:\n"
                                        f"{context.user_data['qwest']}\n\nВарианты ответа:\n{q}",
                                        reply_markup=murkup_ans)
        return 1
    elif update.message.text == 'назад':
        num_to_ans = [[str(i) for i in range(1, len(context.user_data['ans']) + 1)], ['Подсказки', 'Правила игры']]
        murkup_ans = ReplyKeyboardMarkup(num_to_ans, one_time_keyboard=False)
        q = '\n'.join([str(i + 1) + ') ' + context.user_data['ans'][i] for i in range(len(context.user_data['ans']))])
        await update.message.reply_text(f"Вопрос номер {context.user_data['qwest_num']}:\n"
                                        f"{context.user_data['qwest']}\n\nВарианты ответа:\n{q}",
                                        reply_markup=murkup_ans)
        return 1


def main():
    token = os.environ.get('TOKEN', '')
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, choice_to_play)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, helps)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, choice_before_game)]
        },
        fallbacks=[CommandHandler('stop', close_keyboard)]
    )
    app = Application.builder().token(token).build()
    app.add_handler(conv_handler)
    app.run_polling()


if __name__ == '__main__':
    main()
