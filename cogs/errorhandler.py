import traceback
import sys
from discord.ext import commands
import discord
import time
import json
import random
import os
import asyncio
from datetime import datetime
import sqlite3
from uuid import uuid4
import psutil
import itertools
try:
	source = '../Wheatly/'
	os.chdir('../Wheatly/')
except:
	source = '../Wheatly/'
	os.chdir('../Wheatly/')

class ErrorHandler(commands.Cog, name="ErrorHandler"):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandInvokeError):
			# Silly random color
			color = random.randint(0, 0xFFFFFF)
			errortype = error.original.__class__.__name__
			embed=discord.Embed(title=f"Error {errortype}", color=color)
			embed.add_field(name="-", value=f"```\n{error}\n```", inline=False)
			await ctx.send(embed=embed, delete_after=30)
			try:
				await ctx.message.delete()
			except:
				pass
		elif isinstance(error, commands.CommandError):
			# Silly random color
			color = random.randint(0, 0xFFFFFF)
			errortype = error.__class__.__name__
			embed=discord.Embed(title=f"Error {errortype}", color=color)
			embed.add_field(name="-", value=f"```\n{error}\n```", inline=False)
			await ctx.send(embed=embed, delete_after=30)
			try:
				await ctx.message.delete()
			except:
				pass


		ctx.author = 'console'
		erro = traceback.format_exception(type(error), error, error.__traceback__)
		dw = ''
		error = dw.join(erro)
		log(ctx, '\n\nIgnoring exception in command {}:'.format(ctx.command))
		log(ctx, error)

def log(ctx, logtext):
	errorlog = open("errorlogs.txt", 'w', encoding='utf-8')
	now = datetime.now()
	ct = now.strftime("%H:%M:%S")
	if ctx.author == 'console':
		person = ''
	else:
		person = str(ctx.author.id)
	errorlog.write(f"\n{ct} | {ctx.author} {person} {logtext}")
	errorlog.close()

def setup(bot):
	print("ErrorHandler Loaded...")
	bot.add_cog(ErrorHandler(bot))
def teardown(bot):
	print("ErrorHandler Unloaded...")