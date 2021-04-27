import time
import json
import random
import math
import discord
import os
import sys
import sqlite3
import secrets
import discord
import datetime
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from os import listdir
import datetime
import asyncio
# import the token
from config import *

try:
	source = '../Wheatly/'
	os.chdir('../Wheatly/')
except:
	source = '../Wheatly/'
	os.chdir('../Wheatly/')

conn = sqlite3.connect("Database/people.db")
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS people (
			id blob,
			coin real,
			bank real
			)""")
conn.commit()
c.execute("""CREATE TABLE IF NOT EXISTS style (
			id blob,
			style blob
			)""")
conn.commit()
c.execute("""CREATE TABLE IF NOT EXISTS items (
			id blob,
			items blob
			)""")
conn.commit()


# shard id
shardids = 1
# shard count
shardcount = 1
# command prefix
commandprefix = ["w!","W!"]

intents = discord.Intents.all()

bot = commands.AutoShardedBot(case_insensitive=True, loop=None, shard_id=shardids, shard_count=shardcount, command_prefix=commands.when_mentioned_or(*commandprefix), help_command=None, intents=intents)

# cogs
try:
	path = f'{source}/cogs'
	cogs = []
	for f in listdir(path):
		file = f"cogs.{f}".replace('.py', '')
		cogs += [file]
	cogs.remove('cogs.__pycache__')
	#cogs.remove('Cogs.errorhandler')
	print(cogs)
except:
	pass

for extension in cogs:
	bot.load_extension(extension)

x = datetime.datetime.now()
now = str(x.strftime("%d Day(s), %H Hour(s), %M Minute(s), %S Second(s)"))
f = open(f"{source}/started.txt", 'w')
f.write(now)
f.close()
# run the bot
print("Running...")
bot.run(config)