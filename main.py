import logging
import asyncio
from telegram import Update
from telegram.ext import (ApplicationBuilder, ContextTypes, CommandHandler)
from random import choice
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv, find_dotenv
import os

from picture import make_image

TIME = 10
load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

connection_string = (f"mongodb+srv://bakamouto:{password}@exoworld.38dib1x"
                     ".mongodb.net/?retryWrites=true&w=majority")

client = MongoClient(connection_string)

db = client.exoworld
quests = db.quests
users = db.users


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def generate_quests(user, quest_type):
    type_quests = list(quests.find({"type": quest_type}).sort("reward"))
    if user["played"]:
        stats = user["won"] / user["played"]
    else:
        stats = 0
    if stats <= (1/3):
        return choice(type_quests[:len(type_quests)//3])
    if stats <= (2/3):
        return choice(type_quests[len(type_quests)//3:len(type_quests)*2//3])
    return choice(type_quests[len(type_quests)*2//3:])


async def starter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = users.find_one({"telegram_id": update.effective_chat.id})
    if not user:
        new_user = {
            "telegram_id": update.effective_chat.id,
            "first name": update.effective_user.first_name,
            "played": 0,
            "won": 0
        }
        users.insert_one(new_user)
    user = users.find_one({"telegram_id": update.effective_chat.id})

    timer = True
    counter = 0
    daily = generate_quests(user, "daily")
    weekly = generate_quests(user, "weekly")
    while timer:
        counter = (counter + 1) % 7

        img = make_image(daily, weekly, user["telegram_id"])

        await context.bot.send_photo(chat_id=update.effective_chat.id,
                                     photo=img)

        daily = generate_quests(user, "daily")
        if counter == 6:
            weekly = generate_quests(user, "weekly")

        await asyncio.sleep(TIME)


if __name__ == '__main__':
    application = ApplicationBuilder().token('6409648099:AAF4kYLlcwi6q_Som1BhnO3xBxp70Zc4egM').build()

    start_handler = CommandHandler('start', starter)

    application.add_handler(start_handler)

    application.run_polling()