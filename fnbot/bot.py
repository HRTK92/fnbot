import os
import sys
import fortnitepy
from fortnitepy.ext import commands
import BenBotAsync
import FortniteAPIAsync
import pypresence
from functools import partial
import requests
import logging
import json
import time
import asyncio

from .colors import blue, green, magenta, yellow, red
from .setting import get_time
from .setting import BotSettings
from .client import ClientCommands
from . import web


class MyBot(commands.Bot):
	def __init__(self, settings: BotSettings, loop: asyncio.AbstractEventLoop) -> None:
		self.settings = settings
        device_auth_details = self.get_device_auth_details().get(self.settings.email, {})
        super().__init__(
		    command_prefix='!',
		    status=self.settings.status,
		    platform=fortnitepy.Platform(self.settings.platform),
		    avatar=fortnitepy.Avatar(
		        asset=self.settings.cid,
		        background_colors=fortnitepy.KairosBackgroundColorPreset.PINK.
		        value),
		    auth=fortnitepy.AdvancedAuth(
		        email=self.settings.email,
		        password=self.settings.password,
		        prompt_authorization_code=True,
		        delete_existing_device_auths=True,
		        **device_auth_details))
        self.message = f'[PartyBot] {get_time()} %s'

	def get_device_auth_details(self):
		filename = 'device_auths.json'
		if os.path.isfile(filename):
			with open(filename, 'r') as fp:
				return json.load(fp)
		return {}

	def store_device_auth_details(self, email, details):
		existing = self.get_device_auth_details()
		existing[email] = details

		with open(filename, 'w') as fp:
			json.dump(existing, fp)

	async def event_device_auth_generate(self, details, email):
		self.store_device_auth_details(email, details)

	async def status(self):
		status = "{party_member}/{friend_content}｜fnbot".format(
		    party_member=1, friend_content=12)
		await self.bot.send_presence(status)

	async def start_discord_rich_presence(self) -> None:
		rpc = Presence("798068676514414602")
		await rpc.connect()
		start_time = datetime.datetime.now().timestamp()
		while True:
			await rpc.update(
			    details=f"Logged in as {self.user.display_name}.",
			    state=f"{self.party.leader.display_name}'s party.",
			    large_image="skull_trooper",
			    large_text="",
			    small_image="outfit",
			    small_text="",
			    start=int(start_time),
			    party_id=self.party.id,
			    party_size=[self.party.member_count, 16],
			    join=uuid.uuid4().hex)

			await asyncio.sleep(20)

	async def event_ready(self):
		await web.setup()
		print(green(f'{get_time()} [{self.user.display_name}]｜ログインしました\n'))
		owner = self.get_friend(self.settings.owner)

		if owner == None:
			print(red(f'管理者とフレンドではありません'))
			await self.add_friend(self.settings.owner)
		else:
			await owner.send('起動しました')

	async def event_restart(self):
		print('再ログインしました')

	# ノート
	# [{self.user.display_name}]｜
	# [{get_time()}]

	# パーティー

	async def event_party_invite(self, invitation):
		print(
		    f'{get_time()} [{self.user.display_name}]｜{invitation.sender.display_name}から招待'
		)
		if self.settings.party_invite:
			await invitation.accept()
		else:
			member = self.get_friend(self, invitation)
			await invitation.send('現在パーティー招待を受け付けてません')

	async def event_party_member_join(self, member):
		party = self.party
		print(
		    f'{get_time()} [{self.user.display_name}]｜{member.display_name}がパーティーに参加\n人数:{party.member_count}'
		)
		await party.send(f'(≧▽≦)')
		# await BenBotAsync.set_default_loadout(self, self.settings.to_dict(),member)
		if party.member_count > 1:
			member = self.party.me
			await member.set_ready(fortnitepy.ReadyState.SITTING_OUT)

	async def event_party_member_leave(self, member):
		party = self.party
		print(
		    f'{get_time()} [{self.user.display_name}]｜{member.display_name}がパーティーを離脱\n人数:{party.member_count}'
		)

	async def event_party_member_kick(self, member):
		party = self.party
		print(
		    f'{get_time()} [{self.user.display_name}]｜{member.display_name}がキックされました\n人数:{party.member_count}'
		)

	# フレンド

	async def event_friend_add(self, friend):
		print(
		    f'{get_time()} [{self.user.display_name}]｜[フレンド] {friend.display_name} 追加'
		)

	async def event_friend_remove(self, friend):
		print(
		    f'{get_time()} [{self.user.display_name}]｜[フレンド] {friend.display_name} 削除'
		)

	async def event_friend_request(self, request):
		print(
		    f'{get_time()} [{self.user.display_name}]｜[フレンド] {request.display_name}からリクエスト'
		)
		try:
			if self.settings.friend_accept:
				await request.accept()
			else:
				print(
				    f'[{self.user.display_name}]｜[フレンド] {request.display_name}からリクエストを断りました'
				)
		except:
			pass

	# メッセージ

	async def event_friend_message(self, message):
		print(f'{get_time()} [{message.author}] | {message.content}')

	async def event_party_message(self, message):
		print(f'{get_time()} [パーティー] [{message.author}] | {message.content}')
		response = requests.get(
		    f'https://fortnite-api.com/v2/cosmetics/br/search?language=ja&searchLanguage=ja&matchMethod=contains&name={message.content}'
		)
		geted = response.json()
		if response.status_code == 200:
			request_id = geted["data"]["id"]
			request_type = geted["data"]["type"]["value"]
			request_displayValue = geted["data"]["type"]["displayValue"]
			request_name = geted["data"]["name"]
			party = self.party.me
			await message.reply(
			    f'{request_displayValue}｜{request_name}, {request_id}')
			print(
			    f'{get_time()} [{self.user.display_name}]｜{request_displayValue}｜{request_id}'
			)
			if request_type == "emote":
				await party.set_emote(request_id)
			if request_type == "emoji":
				await party.set_emoji(request_id)
			if request_type == "outfit":
				await party.set_outfit(request_id)
			if request_type == "backpack":
				await party.set_backpack(request_id)
			if request_type == "pickaxe":
				await party.set_pickaxe(request_id)
			if request_type == "banner":
				await party.set_banner(request_id)
