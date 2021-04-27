import time
import json
import random
import math
import discord
import os
from os import listdir
from os.path import isfile, join
import os.path
import sys
import sqlite3
import secrets
import tex2pix
import datetime
import itertools
from discord.ext import tasks, commands
from discord.ext.commands.cooldowns import BucketType
from sympy import preview
from sympy.solvers import solve
import asyncio
import ffmpeg
import youtube_dl
try:
	source = '/media/Lonnon/CoolDrive/Coding Shit/Code/PortalRadio'
	os.chdir('/media/Lonnon/CoolDrive/Coding Shit/Code/PortalRadio')
except:
	source = 'E:/Coding Shit/Code/PortalRadio/'
	os.chdir('E:/Coding Shit/Code/PortalRadio/')


class TasksCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.index = 0
		self.sunnydnick = "hentai lover"
		self.changenickname.start()

	def cog_unload(self, bot):
		self.changenickname.cancel()

	@tasks.loop(seconds=5.0)
	async def changenickname(self):
		await self.bot.wait_until_ready()
		guild = self.bot.get_guild(785241980162408450)
		david = guild.get_member(348559658232971265)
		sunnyd = guild.get_member(751466125631422537)
		try:
			if david.nick != "TransLover":
				await david.edit(nick="TransLover")
		except:
			pass
		try:
			if sunnyd.nick != self.sunnydnick:
				await sunnyd.edit(nick=self.sunnydnick)
		except:
			pass

	@commands.Cog.listener()
	async def on_message(self, ctx):
		if ctx.author.id == 593456905754771497 and ctx.channel.id == 809997824585367592:
			await ctx.delete()
		else:
			if ctx.channel.id == 809997824585367592:
				guild = self.bot.get_guild(785241980162408450)
				ruleschannel = guild.get_channel(809997824585367592)
				lastmessages = await ruleschannel.history(limit=2).flatten()
				message = [lastmessages[1].content, lastmessages[0].content]
				rule1 = message[0].split(" ")
				oldrulenumber = rule1[1]
				newrulenumber = int(oldrulenumber.replace(":", "")) + 1
				if ctx.content.lower().startswith(f"rule {newrulenumber}: "):
					pass
				else:
					await ctx.delete()
			else:
				pass

	@commands.Cog.listener()
	async def on_message_edit(self, before, after):
		if after.channel.id == 809997824585367592:
			guild = self.bot.get_guild(785241980162408450)
			ruleschannel = guild.get_channel(809997824585367592)
			lastmessages = await ruleschannel.history(limit=2).flatten()
			message = [lastmessages[1].content, lastmessages[0].content]
			rule1 = message[0].split(" ")
			oldrulenumber = rule1[1]
			newrulenumber = int(oldrulenumber.replace(":", "")) + 1
			if after.content.lower().startswith(f"rule {newrulenumber}: "):
				pass
			else:
				await before.delete()
		else:
			pass

	@commands.command()
	@commands.has_role(825911968464502815) 
	async def sunnydnick(self, ctx, nick: str):
		self.sunnydnick = nick
		
# setup the Cog
def setup(bot):
	print("Tasks Commands Loaded...")
	bot.add_cog(TasksCog(bot))
def teardown(bot):
	print("Tasks Commands Unloaded...")