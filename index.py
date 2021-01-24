import os
import sys
import platform
import json
import time

try:
	import fortnitepy
	import BenBotAsync
	import sanic
	import asyncio
	import aiofiles
	import logging
	import colorama
	import aiohttp
	import requests
	import timeout_decorator
except ModuleNotFoundError as e:
	print(e, '\nモジュールの読み込みに失敗しました。')
	sys.exit()

try:
	import fnbot
except ModuleNotFoundError as e:
	print(e, "\nfnbotの読み込みに失敗しました\n")
	sys.exit()

print(
    fnbot.colors.green(f'\nPython {platform.python_version()}\n'
                       f'fortnitepy {fortnitepy.__version__}\n'))


async def start():
	bot = fnbot.botnew
	web = fnbot.web
	c = input(f'{fnbot.setting.get_time()} ファイルの更新をしますか？\n[yes or no] : ')
	if c == "yes":
		print("更新を実行します\n")
		updater = fnbot.auto_updater
		updater.setup()
		bot.setup()
	else:
		print("更新を実行しません\n")
		setup()


async def main() -> None:
  settings = fnbot.BotSettings()
  await settings.load_settings_from_file()
  client = fnbot.MyBot(settings=settings)
  client.add_cog(fnbot.ClientCommands(client))
  client.add_cog(fnbot.PartyCommands(client))
  await client.start()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
