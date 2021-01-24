import traceback
import requests
import time
import json
import sys
import os
from .colors import red , green

def AddNewKey(data: dict, new: dict) -> dict:
	result = data.copy()
	for key, value in new.items():
		if type(value) == dict:
			result[key] = AddNewKey(result.get(key, {}), value)
		result.setdefault(key, value)
	return result


def CheckUpdate(filename: str, githuburl: str,
                overwrite: bool = False) -> bool:
	print(f'{filename} の更新を確認中...')
	print(f'Checking update for {filename}...')
	try:
		if "/" in filename:
			os.makedirs("/".join(filename.split("/")[:-1]), exist_ok=True)
		for count, text in enumerate(filename[::-1]):
			if text == ".":
				filename_ = filename[:len(filename) - count - 1]
				extension = filename[-count - 1:]
				break
		else:
			filename_ = filename
			extension = ""
		if extension in [".py", ".bat", ".txt", ".md", ".html", ".toml", ""]:
			if os.path.isfile(filename):
				with open(filename, "r", encoding='utf-8') as f:
					current = f.read()
			else:
				github = requests.get(githuburl + filename)
				if github.status_code != 200:
					print(red(f'{filename} のデータを取得できませんでした\n'))
					return None
				github.encoding = github.apparent_encoding
				github = github.text.encode(encoding='utf-8')
				with open(filename, "wb") as f:
					f.write(github)
				with open(filename, "r", encoding='utf-8') as f:
					current = f.read()
			github = requests.get(githuburl + filename)
			if github.status_code != 200:
				print(red(f'{filename} のデータを取得できませんでした\n'))
				return None
			github.encoding = github.apparent_encoding
			github = github.text.encode(encoding='utf-8')
			if current.replace('\n', '').replace(
			    '\r', '').encode(encoding='utf-8') != github.decode().replace(
			        '\n', '').replace('\r', '').encode(encoding='utf-8'):
				print(f'{filename} の更新を確認しました!')
				print(f'{filename} をバックアップ中...\n')
				if os.path.isfile(f'{filename_}_old{extension}'):
					try:
						os.remove(f'{filename_}_old{extension}')
					except PermissionError:
						print(red(f'{filename} ファイルを削除できませんでした\n'))
						print(traceback.format_exc())
				try:
					os.rename(filename, f'{filename_}_old{extension}')
				except PermissionError:
					print(red(f'{filename} ファイルをバックアップできませんでした\n'))
					print(traceback.format_exc())
				else:
					with open(filename, "wb") as f:
						f.write(github)
					print(green(f'{filename} の更新が完了しました!\n'))
					return True
			else:
				print(f'{filename} の更新はありません!\n')
				return False
		elif extension == ".json":
			if os.path.isfile(filename):
				with open(filename, "r", encoding='utf-8') as f:
					current = json.load(f)
			else:
				github = requests.get(githuburl + filename)
				if github.status_code != 200:
					print(f'{filename} のデータを取得できませんでした')
					print(f'Failed to get data for {filename}\n')
					return None
				github.encoding = github.apparent_encoding
				github = github.text.encode(encoding='utf-8')
				with open(filename, "wb") as f:
					f.write(github)
				try:
					with open(filename, "r", encoding='utf-8') as f:
						current = json.load(f)
				except json.decoder.JSONDecodeError:
					with open(filename, "r", encoding='utf-8-sig') as f:
						current = json.load(f)
			github = requests.get(githuburl + filename)
			if github.status_code != 200:
				print(f'{filename} のデータを取得できませんでした')
				print(f'Failed to get data for {filename}\n')
				return None
			github.encoding = github.apparent_encoding
			github = github.text
			github = json.loads(github)

			if overwrite:
				if current != github:
					print(f'{filename} の更新を確認しました!')
					print(f'{filename} をバックアップ中...')
					print(f'Update found for {filename}!')
					print(f'Backuping {filename}...\n')
					if os.path.isfile(f'{filename_}_old{extension}'):
						try:
							os.remove(f'{filename_}_old{extension}')
						except PermissionError:
							print(f'{filename} ファイルを削除できませんでした')
							print(f'Failed to remove file {filename}\n')
							print(traceback.format_exc())
					try:
						os.rename(filename, f'{filename_}_old{extension}')
					except PermissionError:
						print(f'{filename} ファイルをバックアップできませんでした')
						print(f'Failed to backup file {filename}\n')
						print(traceback.format_exc())
					else:
						with open(filename, "w", encoding="utf-8") as f:
							json.dump(github, f, indent=4, ensure_ascii=False)
						print(f'{filename} の更新が完了しました!')
						print(f'Update for {filename} done!\n')
						return True
				else:
					print(f'{filename} の更新はありません!')
					print(f'No update for {filename}!\n')
					return False
			else:
				new = AddNewKey(current, github)
				if current != new:
					print(f'{filename} の更新を確認しました!')
					print(f'{filename} をバックアップ中...')
					print(f'Update found for {filename}!')
					print(f'Backuping {filename}...\n')
					try:
						if os.path.isfile(f'{filename_}_old{extension}'):
							try:
								os.remove(f'{filename_}_old{extension}')
							except PermissionError:
								print(
								    f'{filename_}_old{extension} ファイルを削除できませんでした'
								)
								print(
								    f'Failed to remove file {filename_}_old{extension}'
								)
								print(f'{traceback.format_exc()}\n')
						os.rename(filename, f'{filename_}_old{extension}')
					except PermissionError:
						print(f'{filename} ファイルをバックアップできませんでした')
						print(f'Failed to backup file {filename}')
						print(f'{traceback.format_exc()}\n')
						return None
					else:
						with open(filename, 'w', encoding="utf-8") as f:
							json.dump(new, f, indent=4, ensure_ascii=False)
						print(f'{filename} の更新が完了しました!')
						print(f'Update for {filename} done!\n')
						return True
				else:
					print(f'{filename} の更新はありません!')
					print(f'No update for {filename}!\n')
					return False
		elif extension == ".png":
			if os.path.isfile(filename):
				with open(filename, "rb") as f:
					current = f.read()
			else:
				github = requests.get(githuburl + filename)
				if github.status_code != 200:
					print(f'{filename} のデータを取得できませんでした')
					print(f'Failed to get data for {filename}\n')
					return None
				github = github.content
				with open(filename, "wb") as f:
					f.write(github)
				with open(filename, "rb") as f:
					current = f.read()
			github = requests.get(githuburl + filename)
			if github.status_code != 200:
				print(f'{filename} のデータを取得できませんでした')
				print(f'Failed to get data for {filename}\n')
				return None
			github = github.content
			if current != github:
				print(f'{filename} の更新を確認しました!')
				print(f'{filename} をバックアップ中...')
				print(f'Update found for {filename}!')
				print(f'Backuping {filename}...\n')
				if os.path.isfile(f'{filename_}_old{extension}'):
					try:
						os.remove(f'{filename_}_old{extension}')
					except PermissionError:
						print(f'{filename} ファイルを削除できませんでした')
						print(f'Failed to remove file {filename}\n')
						print(traceback.format_exc())
				try:
					os.rename(filename, f'{filename_}_old{extension}')
				except PermissionError:
					print(f'{filename} ファイルをバックアップできませんでした')
					print(f'Failed to backup file {filename}\n')
					print(traceback.format_exc())
				else:
					with open(filename, "wb") as f:
						f.write(github)
					print(f'{filename} の更新が完了しました!')
					print(f'Update for {filename} done!\n')
					return True
			else:
				print(f'{filename} の更新はありません!')
				print(f'No update for {filename}!\n')
				return False
		else:
			print(f'拡張子 {extension} は対応していません\n')
			return None
	except Exception:
		print("更新に失敗しました")
		print(f'{traceback.format_exc()}\n')
		return None


githuburl = "https://raw.githubusercontent.com/HRTK92/fnbot-/master/"


def setup():
	if CheckUpdate("bot/auto-updater.py", githuburl):
		print("auto_updater.pyの更新を確認しました。アップデーターをもう一度起動します...\n")
		os.chdir(os.getcwd())
		os.execv(os.sys.executable, ['python', *sys.argv])
		#flag = False
	if CheckUpdate("requirements.txt", githuburl):
		print("requirements.txtの更新を確認しました。INSTALLを実行します\n")
		#flag = True
	CheckUpdate("index.py", githuburl)
	CheckUpdate("config.json", githuburl)
	CheckUpdate("fnbot/__init__.py", githuburl)
	CheckUpdate("fnbot/bot.py", githuburl)
	CheckUpdate("fnbot/commands.py", githuburl)
	CheckUpdate("fnbot/colors.py", githuburl)
	CheckUpdate("fnbot/setting.py", githuburl)
	print(green("全ての更新が完了しました"))