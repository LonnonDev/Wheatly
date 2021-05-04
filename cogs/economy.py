import time
import json
import random
import math
import discord
import os
import sys
import sqlite3
import secrets
import tex2pix
import datetime
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from sympy import preview
from sympy.solvers import solve
import asyncio
from discord.ext import tasks, commands
from discord.ext.commands.cooldowns import BucketType
from fractions import Fraction

try:
	source = '../Wheatly/'
	os.chdir('../Wheatly/')
except:
	source = '../Wheatly/'
	os.chdir('../Wheatly/')

conn = sqlite3.connect("Database/people.db")
c = conn.cursor()

class Economy(commands.Cog, name="Economy Commands"):
	def __init__(self, bot):
		self.bot = bot
		self.bs = False

	def getperson(self, ctx, person: discord.Member = None):
		if person == None:
			personog = ctx.author
			person = str(ctx.author.id)
			member = str(ctx)
			membername = str(ctx.author)
		else:
			personog = person
			member = str(person)
			membername = str(person)
			person = str(person.id)
		self.personhandler(person)
		return personog, member, membername, person

	def personhandler(self, person):
		c.execute("SELECT * FROM people WHERE id=?", (person,))
		conn.commit()
		if c.fetchone() == None:
			c.execute("INSERT INTO people (id, coin, bank) VALUES (?, 0, 0)", (person,))
			conn.commit()
		c.execute("SELECT * FROM style WHERE id=?", (person,))
		conn.commit()
		if c.fetchone() == None:
			c.execute("INSERT INTO style (id, style) VALUES (?, \"blue\")", (person,))
			conn.commit()
		c.execute("SELECT * FROM items WHERE id=?", (person,))
		conn.commit()
		if c.fetchone() == None:
			c.execute("INSERT INTO items (id, items) VALUES (?, \"[]\")", (person,))
			conn.commit()

	def emojistype(self, person):
		c.execute("SELECT * FROM style WHERE id=?", (person,))
		conn.commit()
		fetchall = c.fetchall()
		fetch = fetchall[0]
		style = fetch[1]
		emoji = ""
		if style == "blue":
			emoji = "<:blueportal:821744980506181643>"
		elif style == "orange":
			emoji = "<:orangeportal:826285436497297419>"
		elif style == "cake":
			emoji = "<:cake:821743200490094642>"
		elif style == "red":
			emoji = "<:redportal:826485977865388103>"
		elif style == "brown":
			emoji = "<:brownportal:826486070844588042>"
		elif style == "cyan":
			emoji = "<:cyanportal:826485977719635978>"
		elif style == "darkblue":
			emoji = "<:darkblueportal:826485978272628746>"
		elif style == "astolfo":
			emoji = "<:astolfobean:826847520641908766>"
		else:
			emoji = "<:blueportal:821744980506181643>"
		return emoji

	def reset(self, person):
		c.execute("INSERT INTO style (id, style) VALUES (?, blue)", (person,))
		conn.commit()
		c.execute("INSERT INTO people (id, coin, bank) VALUES (?, 0, 0)", (person,))
		conn.commit()

	def fetchbalance(self, person):
		c.execute("SELECT * FROM people WHERE id=?", (person,))
		conn.commit()
		fetchall = c.fetchall()
		fetch = fetchall[0]
		pocket = int(round(fetch[1], 2))
		bank = int(round(fetch[2], 2))
		return pocket, bank

	def removemoney(self, person, lost):
		pocket, bank = self.fetchbalance(person)
		newbalance = pocket - lost
		c.execute("UPDATE people SET coin=? WHERE id=?", (newbalance, person))
		conn.commit()

	def fetchitem(self, item, linestoread):
		file = open(f"Database/items/{item}.item", "r")
		linestoread = linestoread - 1
		for position, line in enumerate(file):
			if position == linestoread:
				return format(line)

	def formatitem(self, item):
		itemformatted = f"```ID: {item}\nCost: {self.fetchitem(item, 1)}```"
		return format(itemformatted)

	def fetchitems(self, person):
		c.execute("SELECT * FROM items WHERE id=?", (person,))
		conn.commit()
		fetchall = c.fetchall()
		fetch = fetchall[0]
		items = fetch[1]
		items = items.strip('][').split(' ')
		return items

	def removedemoncode(self, text):
		text = text.replace("../", "")
		text = text.replace("..\\", "")
		text = text.replace("/", "")
		text = text.replace("\\", "")
		text = text.replace("con", "")
		text = text.replace("aux", "")
		text = text.replace("prn", "")
		text = text.replace("nul", "")
		text = text.replace("'", "")
		text = text.replace("\"", "")
		text = text.replace("\n", "")
		return text

	def turnlistintostring(self, listobj):
		finalstring = "["
		for x in listobj:
			finalstring += f"{x} "
		finalstring += "]"
		return finalstring

	def decreaseitemquantity(self, item):
		file = open(f"Database/items/{item}.item", "r")
		linelist = file.readlines()
		linelist[3] = str(int(linelist[3]) - 1)
		if int(linelist[3]) < 0:
			return False
		else:
			file = open(f"Database/items/{item}.item", "w")
			file.writelines(linelist)
			file.close()
			return True

			finalstring += f"{x}, "
		finalstring += "]"
		return finalstring

	@commands.command()
	async def reset(self, ctx):
		person = None
		personog, member, membername, person = self.getperson(ctx, person)
		await ctx.send(person)
		self.reset(person)

	@commands.command(aliases=["bal"])
	async def balance(self, ctx, person: discord.Member = None):
		color = random.randint(0, 0xFFFFFF)
		personog, member, membername, person = self.getperson(ctx, person)
		self.personhandler(person)
		pocket, bank = self.fetchbalance(person)
		emoji = self.emojistype(person)
		embed=discord.Embed(title=f"Balance", color=color)
		embed.set_author(name=membername[:-5],icon_url=personog.avatar_url)
		embed.add_field(name="Pocket", value=f"{pocket} {emoji}", inline=True)
		embed.add_field(name="Bank", value=f"{bank} {emoji}", inline=True)
		embed.add_field(name="Total", value=f"{pocket + bank} {emoji}", inline=True)
		await ctx.send(embed=embed)

	@commands.command(aliases=["spg","shootportal","sp", "shootpg"])
	@commands.cooldown(1, 60*2, commands.BucketType.user)
	async def shootportalgun(self, ctx):
		color = random.randint(0, 0xFFFFFF)
		personog, member, membername, person = self.getperson(ctx)
		pocket, bank = self.fetchbalance(person)
		amount = 1
		paycheck = amount + pocket
		emoji = self.emojistype(person) 
		embed=discord.Embed(name="Portal Gun", color=color)
		embed.add_field(name="You shot", value=f"{amount} {emoji}", inline=True)
		embed.set_author(name=membername[:-5],icon_url=personog.avatar_url)
		randomimg = random.randint(1, 2)
		if randomimg == 1:
			embed.set_image(url="https://media1.tenor.com/images/0d0c8ca68d5db8231813b095ef079b76/tenor.gif")
		elif randomimg == 2:
			embed.set_image(url="https://media.tenor.com/images/e0b55c4cb1a105308b1c7fa742600ab2/tenor.gif")
		await ctx.send(embed=embed)
		c.execute("UPDATE people SET coin=? WHERE id=?", (paycheck, person))
		conn.commit()

	@commands.command()
	async def buy(self, ctx, item: str):
		item = self.removedemoncode(item)
		canbuy = self.decreaseitemquantity(item)
		if canbuy == True:
			personog, member, membername, person = self.getperson(ctx)
			pocket, bank = self.fetchbalance(person)
			items = self.fetchitems(person)
			if int(pocket) >= int(self.fetchitem(item, 1)):
				paycheck = pocket - int(self.fetchitem(item, 1))
				c.execute("UPDATE people SET coin=? WHERE id=?", (paycheck, person))
				conn.commit()
				items += [item]
				items = self.turnlistintostring(items)
				c.execute("UPDATE items SET items=? WHERE id=?", (items, person))
				conn.commit()
				await ctx.send("worked")
		else:
			await ctx.send("Not Enough Stock, wait for us to restock that item")
		personog, member, membername, person = self.getperson(ctx)
		pocket, bank = self.fetchbalance(person)
		items = self.fetchitems(person)
		if int(pocket) >= int(self.fetchitem(item, 1)):
			paycheck = pocket - int(self.fetchitem(item, 1))
			c.execute("UPDATE people SET coin=? WHERE id=?", (paycheck, person))
			conn.commit()
			items += [item]
			items = self.turnlistintostring(items)
			await ctx.send(items)
			c.execute("UPDATE items SET items=? WHERE id=?", (items, person))
			conn.commit()
			await ctx.send("worked")

	@commands.command(aliases=["shop"])
	async def items(self, ctx):
		files = [f"Big Chungus Coin: {self.formatitem('bigchungus')}", f"Gaming: {self.formatitem('gaming')}"]
		per_page = 3 # 10 files per page
		pages = math.ceil(len(files) / per_page)
		cur_page = 1
		chunk = files[:per_page]
		linebreak = ""
		message = await ctx.send(f"Page {cur_page}/{pages}:\n>>> {linebreak.join(chunk)}")
		await message.add_reaction("◀️")
		await message.add_reaction("▶️")
		active = True

		def check(reaction, user):
			return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
						 # or you can use unicodes, respectively: "\u25c0" or "\u25b6"

		while active:
			try:
				reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
			
				if str(reaction.emoji) == "▶️" and cur_page != pages:
					cur_page += 1
					if cur_page != pages:
						chunk = files[(cur_page-1)*per_page:cur_page*per_page]
					else:
						chunk = files[(cur_page-1)*per_page:]
					await message.edit(content=f"Page {cur_page}/{pages}:\n```{linebreak.join(chunk)}```")
					await message.remove_reaction(reaction, user)

				elif str(reaction.emoji) == "◀️" and cur_page > 1:
					cur_page -= 1
					chunk = files[(cur_page-1)*per_page:cur_page*per_page]
					await message.edit(content=f"Page {cur_page}/{pages}:\n```{linebreak.join(chunk)}```")
					await message.remove_reaction(reaction, user)
			except asyncio.TimeoutError:
				await message.delete()
				active = False

	@commands.command(aliases=["inv"])
	async def inventory(self, ctx):
		personog, member, membername, person = self.getperson(ctx)
		files = self.fetchitems(person)
		per_page = 10 # 10 files per page
		pages = math.ceil(len(files) / per_page)
		cur_page = 1
		chunk = files[:per_page]
		linebreak = "\n"
		message = await ctx.send(f"Page {cur_page}/{pages}:\n>>> ```Items:\n{linebreak.join(chunk)}```")
		await message.add_reaction("◀️")
		await message.add_reaction("▶️")
		active = True

		def check(reaction, user):
			return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
						 # or you can use unicodes, respectively: "\u25c0" or "\u25b6"

		while active:
			try:
				reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
			
				if str(reaction.emoji) == "▶️" and cur_page != pages:
					cur_page += 1
					if cur_page != pages:
						chunk = files[(cur_page-1)*per_page:cur_page*per_page]
					else:
						chunk = files[(cur_page-1)*per_page:]
					await message.edit(content=f"Page {cur_page}/{pages}:\n```{linebreak.join(chunk)}```")
					await message.remove_reaction(reaction, user)

				elif str(reaction.emoji) == "◀️" and cur_page > 1:
					cur_page -= 1
					chunk = files[(cur_page-1)*per_page:cur_page*per_page]
					await message.edit(content=f"Page {cur_page}/{pages}:\n```{linebreak.join(chunk)}```")
					await message.remove_reaction(reaction, user)
			except asyncio.TimeoutError:
				await message.delete()
				active = False

	def truncate(self, number, decimals=2):
		return round(number*100) / 100

	@commands.command()
	@commands.is_owner()
	async def bsmode(self, ctx):
		if self.bs == False:
			self.bs = True
		else:
			self.bs = False

	@commands.command()
	@commands.is_owner()
	async def bsvalue(self, ctx, value: int):
		self.bsvalue = value

	@commands.command(aliases=["tr"])
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def transrights(self, ctx, person: discord.Member = None, bet: int = 0):
		if person == None and bet == 0:
			myfinalmessage = ""
			numberoftrans = 0
			while(True):
				if ctx.author.id == 600798393459146784 and self.bs == True:
					numberoftrans += self.bsvalue
				numberoftrans += 1
				if(random.randint(1,5) == 1):
					s = 0.8
					n = numberoftrans
					ans = self.truncate((s**(n-1) - s**(n))*100)
					frac = Fraction((s**(n-1) - s**(n))).limit_denominator(1000)
					if len(str(numberoftrans)) == 3:
						myfinalmessage += "<:p_:830938952277950496>" * int(str(numberoftrans)[0])
						myfinalmessage += "<:b_:830936622701740083>" * int(str(numberoftrans)[1])
						myfinalmessage += "<:t_:830935905871200286>" * int(str(numberoftrans)[2])
					elif len(str(numberoftrans)) == 2:
						myfinalmessage += "<:b_:830936622701740083>" * int(str(numberoftrans)[0])
						myfinalmessage += "<:t_:830935905871200286>" * int(str(numberoftrans)[1])
					else:
						myfinalmessage += "<:t_:830935905871200286>" * int(str(numberoftrans)[0])
					color = random.randint(0, 0xFFFFFF)
					personog, member, membername, person = self.getperson(ctx, person)
					embed=discord.Embed(title=f"TransRights", color=color)
					embed.set_author(name=membername[:-5],icon_url=personog.avatar_url)
					embed.add_field(name=f"{myfinalmessage}", value=f"{numberoftrans} Flag(s)!\n {ans}% ({frac}) chance of happening", inline=False)
					await ctx.send(embed=embed)
					break
		elif person != None and bet == 0:
			errortype = 'MissingRequiredArgument'
			embed=discord.Embed(title=f"Error MissingRequiredArgument", color=color)
			embed.add_field(name="-", value=f"```\nBet is a required argument that is missing.\n```", inline=False)
			await ctx.send(embed=embed, delete_after=30)

def setup(bot):
	print("Economy Commands Loaded...")
	bot.add_cog(Economy(bot))
def teardown(bot):
	print("Economy Commands Unloaded...")