#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from weather_fun import whole

_city_name="\0"
from telegram import InlineKeyboardButton
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CITY,EXTRACT_WEATHER = range(2)
user_id=0

def start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['台北市信義區', '新竹市東區','台北市南港區','新北市汐止區','基隆市中山區']]

    update.message.reply_text(
        'Hi! Tell me which city that you would like to know the weather \n',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return CITY


def city(update: Update, context: CallbackContext) -> int:
    global _city_name,user_id
    _city_name = update.message.text
    #print(type(update.message))
    user_id = update.message.chat_id
    reply_keyboard = [['三小時氣溫', '六小時降雨','both']]
    #logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'what\'s the information you would like to know?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return EXTRACT_WEATHER


def extract_weather(update: Update, context: CallbackContext) -> int:
    global _city_name
    global user_id
    function_name = update.message.text

    if function_name=='三小時氣溫':
        _str = whole(0,_city_name,user_id)
    elif function_name =='六小時降雨':
        _str = whole(1,_city_name,user_id)
    else:
        _str = whole(2,_city_name,user_id)
        
    #print(_str)
    update.message.reply_text(_str)

    return ConversationHandler.END



def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    telegram_token = ""
    updater = Updater(telegram_token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CITY: [MessageHandler(Filters.regex('^(台北市信義區|新竹市東區|台北市南港區|新北市汐止區|基隆市中山區)$'), city)],
            EXTRACT_WEATHER: [MessageHandler(Filters.regex('^(三小時氣溫|六小時降雨|both)$'),extract_weather)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
