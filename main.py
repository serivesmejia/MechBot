import os

from flask_server import KeepAliveServer
import bot

KeepAliveServer().asyncStart() #start server which will be pinged ocassionally to avoid repl.it turning off our bot

discord_token = os.getenv("discord_token") #get bot token from .env file

bot.start(discord_token) #initialize bot client instance