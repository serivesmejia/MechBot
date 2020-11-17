import discord

import os
import datetime
from re import match

bot = discord.Client()

def start(discord_token):
    bot.run(discord_token); #start bot execution

@bot.event
async def on_ready():
    print('Logged in as {0}!'.format(bot.user))
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Rocket League"))

@bot.event
async def on_message(message):

  if(contains_mention(message.content, "778282808879218759")):
    await message.channel.send("Hola {0}!".format(message.author.mention))
  elif str.startswith(message.content, "$setteam"):
    await cmd_set_team(message)


async def cmd_set_team(message):
  if is_staff(message.author):
      args = message.content.replace("$setteam ", "") .split(" ")
      if len(args) < 2 or len(args) > 2 or len(message.mentions) < 1 or len(message.mentions) > 1:
        await message.channel.send("Argumentos invalidos, usa ```$setteam <usuario> <numero de equipo>```")
        return
      try:  
        team_number = int(args[1].strip())
        role_name = "Team " + str(team_number)
        role = discord.utils.get(message.guild.roles, name=role_name)
        await message.author.add_roles(role)
        await message.channel.send("Agregado el rol {0} al usuario especificado".format(role_name))
        return
      except:
        await message.channel.send("Argumentos invalidos, usa ```$setteam <usuario> <numero de equipo>```")
  else:
    await message.channel.send("Permisos insuficientes para usar el comando")


def has_permission(author, role_name):
  return discord.utils.get(author.roles, name=role_name) is None

def is_staff(author):
  return has_permission(author, "Mod") or has_permission(author, "Staff")

def contains_mention(content, mention_id):
  return match("<@!{0}>".format(mention_id), content) is not None