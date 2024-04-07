import logging
import os

from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler, ContextTypes

load_dotenv()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

reply_keyboard1 = [['/close', '/help']]
reply_keyboard2 = [['/start']]
reply_keyboard3 = [['Да', 'Нет']]
reply_keyboard4 = [['1', '2', '3', '4']]
money_to_qwest = [500, 1000, 2000, 3000, 5000, 10000, 15000, 25000, 50000, 100000, 200000, 400000, 800000, 1500000,
                  3000000]

markup = ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=False)
murkup2 = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=False)
murkup3 = ReplyKeyboardMarkup(reply_keyboard3, one_time_keyboard=False)
murkup4 = ReplyKeyboardMarkup(reply_keyboard4, one_time_keyboard=False)
TIMER = 5


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    context.user_data['qwest_num'] = 1
    # тут происходит запрос на вопрос
    context.user_data['ans'] = ['1', '2', '3', '4']
    context.user_data['r_ans'] = '4'
    context.user_data['qwest'] = '2+2='
    q = '\n'.join([str(i + 1) + '. ' + context.user_data['ans'][i] for i in range(4)])
    await update.message.reply_text(f"Привет {user.full_name}! Вы попали на передачу кто хочет стать миллионером.\n ")

    await update.message.reply_text(f"Вопрос номер {context.user_data['qwest_num']}:\n"
                                    f"{context.user_data['qwest']}\n\nВарианты ответа:\n{q}",
                                    reply_markup=murkup4)
    return 1


async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text not in ['1', '2', '3', '4']:
        await update.message.reply_text('Выведете число от 1 до 4 - вариант ответа')
        return 1
    if context.user_data['ans'][int(update.message.text) - 1] != context.user_data['r_ans']:
        await update.message.reply_text('К сожалению это неправильный ответ, вы проиграли, прощайте.')
        return ConversationHandler.END
    await update.message.reply_text('И это правильный ответ.')
    context.user_data['qwest_num'] += 1
    await update.message.reply_text(f'хотите продолжить?', reply_markup=murkup3)
    return 2


async def choice_to_play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text not in ['Да', 'Нет']:
        await update.message.reply_text('Я вас не понял, просто напишите "ДА" или "Нет"')
        return 2
    if update.message.text == 'Да':
        await update.message.reply_text()


async def help_command(update, context):
    await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=murkup2
    )


def main():
    token = os.environ.get('TOKEN', '')
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer)]
        },
        fallbacks=[CommandHandler('stop', close_keyboard)]
    )
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("close", close_keyboard))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(conv_handler)
    app.run_polling()


if __name__ == '__main__':
    main()
