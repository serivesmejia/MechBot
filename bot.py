import discord

import os
import sys, traceback
import datetime
import re

bot = discord.Client()

prefix = "%"

def start(discord_token):
    bot.run(discord_token); #start bot execution

@bot.event
async def on_ready():
    print('Logged in as {0}!'.format(bot.user))
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Fornait"))

@bot.event
async def on_message(message):
  if(contains_mention(message.content, "778282808879218759")):
    await message.channel.send("Hola {0}!".format(message.author.mention))
  elif is_command(message.content, "setteam"):
    await cmd_set_team(message)
  elif is_command(message.content, "teams"):
    await cmd_teams(message)
  elif is_command(message.content, "team"):
    await cmd_team(message)
  elif is_command(message.content, "participants"):
    await cmd_participants(message)
  elif is_command(message.content, "modmail"):
    await cmd_modmail(message)
  
  if re.search('ayuda', message.content, re.IGNORECASE) and not message.author.bot:
    await message.channel.send("<@!{0}>, si necesitas ayuda de un staff usa el comando %modmail".format(message.author.id))

async def cmd_set_team(message):
  if is_staff(message.author):

      args = message.content.replace(prefix + "setteam ", "").split(" ")

      if len(args) < 2 or len(message.mentions) < 1:
        await message.channel.send("Argumentos invalidos (A), usa ```{0}setteam <usuario(s)> <numero de equipo>```".format(prefix))
        return

      try:
        team_number = int(args[len(message.mentions)].strip())
        role_name = "Team " + str(team_number)
        role = discord.utils.get(message.guild.roles, name=role_name)
        
        for user in message.mentions:
          await user.add_roles(role)

        if len(message.mentions) == 1:
          await message.channel.send("Agregado el rol {0} al usuario especificado".format(role_name))
        else:
          await message.channel.send("Agregado el rol {0} a los usuarios especificados".format(role_name))

        return
      except:
        await message.channel.send("Argumentos invalidos (B), usa ```{0}setteam <usuario(s)> <numero de equipo>```".format(prefix))
  else:
    await message.channel.send("Permisos insuficientes para usar el comando")

async def cmd_team(message):
  args = message.content.replace(prefix + "team ", "").split(" ")

  if len(args) < 1 or len(args) > 1:
    await message.channel.send("Argumentos invalidos (A), usa ```{0}team <numero de equipo>```".format(prefix))
    return

  try:
    team_number = int(args[0].strip())
    role_name = "Team " + str(team_number)
    
    role = discord.utils.get(message.guild.roles, name=role_name)

    if role == None:
      await message.channel.send("El equipo especificado no existe")
      return

    members = await members_in_role(message.guild, role_name)

    if(len(members) == 0):
      await message.channel.send("El equipo especificado no tiene ningun miembro")
      return

    members_str = ""

    for member in members:
        members_str += "\n" + get_name_or_nick(member)
            
    if(members_str.strip() == ""):
      await message.channel.send("El equipo especificado no tiene ningun miembro")
      return

    await message.channel.send("Miembros en el " + role_name + " ```" + members_str + "```")

    return
  except:

    await message.channel.send("Argumentos invalidos (B) , usa ```{0}team <numero de equipo>```".format(prefix))

    traceback.print_exc(file=sys.stdout)

async def cmd_participants(message):
  
  members = await members_in_role(message.guild, "Participante")
  
  members_str = ""
  members_count = 0

  if len(members) == 0:
    await message.channel.send("No hay ningun participante")
    return

  for member in members:
    members_count += 1
    members_str += "\n" + get_name_or_nick(member)

  await message.channel.send("```" + members_str + "```")
  await message.channel.send("Cantidad de participantes: {0}".format(members_count))

async def cmd_teams(message):
  
  team_roles = get_team_roles(message.guild)
  final_msg = "```"

  wait_message = await message.channel.send("Espera, analizando equipos...")

  for role in team_roles:
    final_msg += "\n" + role.name + ":"
    members = await members_in_role(message.guild, role.name)
    for member in members:
      final_msg += "\n  " + get_name_or_nick(member)

  final_msg += "```"

  await wait_message.edit(content=final_msg)

async def cmd_modmail(message):
  msg = message.content.replace(prefix + "modmail", "").strip()

  if msg == "":
    await message.channel.send("Argumentos invalidos, usa ```%modmail <mensaje>```")
    return

  modmail_channel = discord.utils.get(message.guild.channels, name="modmail", type=discord.ChannelType.text)

  if modmail_channel == None:
    await message.channel.send("No se ha encontrado el canal #modmail!\nStaff: Asegurense de crear el canal antes mencionado (exactamente como esta escrito).")
    return

  await modmail_channel.send("@here, modmail de <@!{0}>: ```{1}```\nPresiona a este link para ir al mensaje: {2}".format(message.author.id, msg, message.jump_url))

  await message.channel.send("Mensaje enviado, espera la respuesta de algun miembro del staff pronto.")

def is_command(content, command):
  return content.startswith(prefix + command)

def has_permission(author, role_name):
  return discord.utils.get(author.roles, name=role_name) is not None

def is_staff(author):
  return has_permission(author, "Mod") or has_permission(author, "Admin")

def get_team_roles(guild):
  
  curr_team = 1
  teams = []

  team_prefix = "Team "

  while True:
    curr_team_role = discord.utils.get(guild.roles, name=team_prefix + str(curr_team))
    
    if(curr_team_role == None):
      break
    
    curr_team += 1
    teams.append(curr_team_role)

  return teams

async def members_in_role(guild, role_name):
  members = await guild.fetch_members().flatten()
  members_in_role = []
  for member in members:
      if not (discord.utils.get(member.roles, name=role_name) is None):
        members_in_role.append(member)
  return members_in_role

def get_name_or_nick(member):
  name = ""
  if member.nick == None:
    name = member.name
  else:
    name = member.nick 
  return name

def contains_mention(content, mention_id):
  return re.match("<@!{0}>".format(mention_id), content) is not None