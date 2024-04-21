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

reply_keyboard1 = [['/start', '/help', '/account']]
reply_keyboard3 = [['Да', 'Нет']]

money_to_qwest = [0, 500, 1000, 2000, 3000, 5000, 10000, 15000, 25000, 50000, 100000, 200000, 400000, 800000, 1500000,
                  3000000]

markup = ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=False)
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

def get_user(user_id):
    request = f'http://127.0.0.1:8000/api/user/{user_id}'
    a = requests.get(request).json()
    logger.info(str(a))
    return a['money']


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    context.user_data['qwest_num'] = 1
    context.user_data['ids'] = []
    context.user_data['helps'] = [['Сменить вопрос'], ['50/50', 'Второй шанс'], ['назад']]
    context.user_data['second_chance'] = False
    # тут происходит запрос на вопрос
    n = get_qwest((context.user_data['qwest_num'] + 2) // 3, context.user_data['ids'])
    if n == 'error':
        await update.message.reply_text(f"Вопросы закончились.")
        await update.message.reply_text(f'Вы вывиграли {money_to_qwest[context.user_data["qwest_num"] - 1]} рублей.\n'
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
    num_to_ans = [[str(i) for i in range(1, len(context.user_data['ans']) + 1)], ['Подсказки']]
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


async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    helps_murkup = ReplyKeyboardMarkup(context.user_data['helps'], one_time_keyboard=False)
    if update.message.text not in ['1', '2', '3', '4', 'Подсказки']:
        await update.message.reply_text('Выведете число от 1 до 4 - вариант ответа или попросите подсказку,'
                                        ' введя слово "Подсказки"')
        return 1

    if update.message.text == 'Подсказки':
        await update.message.reply_text('Выберете одну из подсказок: Второй шанс, 50/50, Сменить вопрос или '
                                        'вернитесь обратно, написав слово "назад"', reply_markup=helps_murkup)
        return 3

    if context.user_data['ans'][int(update.message.text) - 1] != context.user_data['r_ans']:
        await update.message.reply_text('К сожалению это неправильный ответ.')
        if context.user_data['second_chance']:
            context.user_data['second_chance'] = False
            await update.message.reply_text('Второй шанс.')
            del context.user_data['ans'][int(update.message.text) - 1]
            num_to_ans = [[str(i) for i in range(1, len(context.user_data['ans']) + 1)], ['Подсказки']]
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
            f'Прощайте.', reply_markup=markup)
        refactor_user(user.id, money_to_qwest[context.user_data["qwest_num"] - (context.user_data["qwest_num"] % 5)])
        context.user_data.clear()
        return ConversationHandler.END
    if context.user_data['qwest_num'] == 15:
        await update.message.reply_text(f'Поздравляю вы победили!\n'
                                        f'Вы вывиграли {money_to_qwest[context.user_data["qwest_num"]]} рублей.\n'
                                        f'До новых встреч.')
        refactor_user(user.id, money_to_qwest[context.user_data["qwest_num"]])
        context.user_data.clear()
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
                                        reply_markup=markup)
        refactor_user(user.id, money_to_qwest[context.user_data["qwest_num"]])
        context.user_data.clear()
        return ConversationHandler.END
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
            return ConversationHandler.END
        context.user_data['ans'] = n['answers']
        context.user_data['qwest_type'] = n['type']
        context.user_data['ids'].append(n['id'])
        context.user_data['r_ans'] = n['r_answer']
        context.user_data['qwest'] = n['text']
        context.user_data['photo'] = 'API/' + str(n['photo'])
        num_to_ans = [[str(i) for i in range(1, len(context.user_data['ans']) + 1)], ['Подсказки']]
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


async def help_command(update, context):
    await update.message.reply_text("<b><del>Мой создатель ещё не добавил эту функцию</del></b>", parse_mode="html")


async def my_money(update, context):
    user = update.effective_user
    money = get_user(user.id)
    await update.message.reply_text(f"Ваш счёт: {money}")


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
        num_to_ans = [[str(i) for i in range(1, len(context.user_data['ans']) + 1)], ['Подсказки']]
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
        num_to_ans = [[str(i) for i in range(1, len(context.user_data['ans']) + 1)], ['Подсказки']]
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
        num_to_ans = [[str(i) for i in range(1, len(context.user_data['ans']) + 1)], ['Подсказки']]
        murkup_ans = ReplyKeyboardMarkup(num_to_ans, one_time_keyboard=False)
        q = '\n'.join([str(i + 1) + ') ' + context.user_data['ans'][i] for i in range(len(context.user_data['ans']))])
        await update.message.reply_text(f"Вопрос номер {context.user_data['qwest_num']}:\n"
                                        f"{context.user_data['qwest']}\n\nВарианты ответа:\n{q}",
                                        reply_markup=murkup_ans)
        return 1
    elif update.message.text == 'назад':
        num_to_ans = [[str(i) for i in range(1, len(context.user_data['ans']) + 1)], ['Подсказки']]
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
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, helps)]
        },
        fallbacks=[CommandHandler('stop', close_keyboard)]
    )
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("account", my_money))
    app.add_handler(conv_handler)
    app.run_polling()


if __name__ == '__main__':
    main()
