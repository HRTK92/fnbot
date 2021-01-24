import fortnitepy
import fortnitepy.ext.commands


class Class():
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def set_status(self):
        party = self.bot.party
        member_count = party.member_count
        status = "{party_member}/{friend_content}｜fnbot".format(
            praty_member=member_count, friend_content=12)
        await self.bot.send_presence(status)
