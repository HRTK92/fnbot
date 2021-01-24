import json
import time
import datetime
import pytz
import os
import aiofiles

class BotSettings:
	def __init__(self,
	             email: str = "",
	             password: str = "",
	             owner:str = "",
	             cid: str = "",
	             bid: str = "",
	             eid: str = "",
	             pickaxe_id: str = "",
	             banner: str = "",
	             banner_colour: str = "",
	             level: int = 0,
	             bp_tier: int = 0,
	             status: str = "",
	             platform: str = "",
	             debug: bool = False,
	             party_invite:bool=True,
	             friend_accept: bool = True) -> None:

		self.email = email
		self.password = password
		self.owner = owner
		self.cid = cid
		self.bid = bid
		self.eid = eid
		self.pickaxe_id = pickaxe_id
		self.banner = banner
		self.banner_colour = banner_colour
		self.level = level
		self.bp_tier = bp_tier
		self.status = status
		self.platform = platform
		self.debug = debug
		self.party_invite = party_invite
		self.friend_accept = friend_accept
	async def load_settings_from_file(self) -> None:
		async with aiofiles.open("config/config.json", mode='r+') as f:
			raw = await f.read()
		data = json.loads(raw)
		self.email = data.get('email', self.email)
		self.password = data.get('password', self.password)
		self.owner = data.get('owner', self.owner)
		self.cid = data.get('cid', self.cid)
		self.bid = data.get('bid', self.bid)
		self.eid = data.get('eid', self.eid)
		self.pickaxe_id = data.get('pickaxe_id', self.pickaxe_id)
		self.banner = data.get('banner', self.banner)
		self.banner_colour = data.get('banner_colour', self.banner_colour)
		self.level = data.get('level', self.level)
		self.bp_tier = data.get('bp_tier', self.bp_tier)
		self.status = data.get('status', self.status)
		self.platform = data.get('platform', self.platform)
		self.debug = data.get('debug', self.debug)
		self.party_invite = data.get('party_invite',self.party_invite)
		self.friend_accept = data.get('friend_accept', self.friend_accept)
	def to_dict(self) -> dict:
		return {
		    "email": self.email,
		    "password": self.password,
		    "cid": self.cid,
		    "bid": self.bid,
		    "eid": self.eid,
		    "pickaxe_id": self.pickaxe_id,
		    "banner": self.banner,
		    "banner_colour": self.banner_colour,
		    "level": self.level,
		    "bp_tier": self.bp_tier,
		    "status": self.status,
		    "platform": self.platform,
		    "debug": self.debug,
		    "friend_accept": self.friend_accept
		}


def config():
	try:
		json_open_config = open('config.json', 'r')
		config = json.load(json_open_config)
	except:
		print('jsonの読み込みに失敗しました')
	return config


def get_time():
	today = datetime.datetime.fromtimestamp(time.time())
	now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
	data = now.strftime('[%m/%d %H:%M:%S]')
	return data
