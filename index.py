import os
import sys
import platform
import json
import time

try:
	import fortnitepy
	import BenBotAsync
	import asyncio
	import aiofiles
	import logging
	import colorama
	import aiohttp
	import requests
	import crayons
except ModuleNotFoundError as e:
	print(e, '\nモジュールの読み込みに失敗しました。')
	sys.exit()

try:
	import fnbot
except ModuleNotFoundError as e:
	print(e, "\nfnbotの読み込みに失敗しました\n")
	sys.exit()




def start():
	print(fnbot.colors.green(
		f'\nPython {platform.python_version()}\n'
		f'fortnitepy {fortnitepy.__version__}\n'))
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())

async def main() -> None:
  print(fnbot.colors.green(
		f'\nPython {platform.python_version()}\n'
		f'fortnitepy {fortnitepy.__version__}\n'))
  loop = asyncio.get_event_loop()
  settings = fnbot.BotSettings()
  await settings.load_settings_from_file()
  client = fnbot.MyBot(settings=settings, loop=loop)
  client.add_cog(fnbot.ClientCommands(client))
  client.add_cog(fnbot.PartyCommands(client))
  await client.start()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())