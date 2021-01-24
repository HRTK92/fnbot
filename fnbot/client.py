from typing import Optional, Union

# Third party imports.
from fortnitepy.ext import commands

import fortnitepy


class ClientCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def set_status(self):
        status = "{party_member}/{friend_content}｜fnbot".format(party_member=1, friend_content=12)
        await self.bot.send_presence(status)

        @commands.dm_only()
        @commands.command(
            description="[Client] Sends and sets the status.",
            help="Sends and sets the status.\n"
            "Example: !status Presence Unknown")
        async def status(self, ctx: fortnitepy.ext.commands.Context, *,
                         content: str) -> None:
            await self.bot.set_presence(content)

            await ctx.send(f'Status set to {content}')
            print(self.bot.message % f'Status set to {content}.')

        @commands.dm_only()
        @commands.command()
        async def relogin(self, ctx):
            await ctx.send(f'{get_time()} 再起動します')
            await bot.restart()

        @commands.dm_only()
        @commands.command(
            description="[Client] Sets the clients kairos/PartyHub avatar.",
            help="Sets the clients kairos/PartyHub avatar.\n"
            "Example: !avatar stw_soldier_f")
        async def avatar(self, ctx: fortnitepy.ext.commands.Context,
                         kairos_cid: str) -> None:
            kairos_avatar = fortnitepy.Avatar(asset=kairos_cid)

            self.bot.set_avatar(kairos_avatar)

            await ctx.send(f'Kairos avatar set to {kairos_cid}.')
            print(self.bot.message % f'Kairos avatar set to {kairos_cid}.')

        @commands.dm_only()
        @commands.command(
            aliases=['clear'],
            description="[Client] Clears command prompt/terminal.",
            help="Clears command prompt/terminal.\n"
            "Example: !clean")
        async def clean(self, ctx: fortnitepy.ext.commands.Context) -> None:
            os.system('cls' if 'win' in sys.platform else 'clear')

            print(
                crayons.cyan(self.bot.message % f'PartyBot made by xMistt. '
                             'Massive credit to Terbau for creating the library.'))
            print(
                crayons.cyan(
                    self.bot.message %
                    f'Discord server: https://discord.gg/fnpy - For support, questions, etc.'
                ))

            await ctx.send('Command prompt/terminal cleared.')
            print(self.bot.message % f'Command prompt/terminal cleared.')

        @commands.dm_only()
        @commands.command(
            description="[Client] Sends and sets the status to away.",
            help="Sends and sets the status to away.\n"
            "Example: !away")
        async def away(self, ctx: fortnitepy.ext.commands.Context) -> None:
            await self.bot.set_presence(
                status=self.bot.status, away=fortnitepy.AwayStatus.AWAY)

        @commands.command(
            description="[Client] Sends and sets the status to away.",
            help="Sends and sets the status to away.\n"
            "Example: !away")
        async def away(self, ctx: fortnitepy.ext.commands.Context) -> None:
            await self.bot.set_presence(
                status=self.bot.status, away=fortnitepy.AwayStatus.AWAY)

            await ctx.send('Status set to away.')
