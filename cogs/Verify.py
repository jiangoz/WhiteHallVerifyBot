import discord
import asyncio
from discord.ext import commands

# NO COMMANDS HERE, only 1 listener for on_message()
# Designed specifically for White Hall server


class Verify(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.nuidlist = open('NUIDList.txt','r').read().split('\n')

    @commands.Cog.listener()
    async def on_message(self, msg:str):

        # ignore self sent messages
        if msg.author == self.bot.user:
            return

        # if msg was sent in DM (not in a guild)
        if msg.guild == None:
            # get the NUID from input message
            provided_id = msg.content
            if provided_id.startswith('00'):
                # remove the '00' in front
                provided_id = provided_id.replace('00', '', 1)

            if provided_id in self.nuidlist:
                whserver = self.bot.get_guild(879139556409106492) # White Hall
                verifiedrole = whserver.get_role(879814996287189022)
                resident = whserver.get_member(msg.author.id)
                await resident.add_roles(verifiedrole)
                await msg.author.send('You are verified! '
                'You should now be able to see the rest of the White Hall server :)')
                await msg.add_reaction('✅')
                # log this to the verification channel (only RA/RD can see)
                verifiedchannel = self.bot.get_channel(879903438299889715)
                await verifiedchannel.send(
                    f'{msg.author.mention} ({msg.author.id}) '
                    f'verified with their NUID: {provided_id}')
            else:
                await msg.author.send(f'Sorry, try again! Send only your NUID:')
                await msg.add_reaction('❌')


def setup(bot):
    bot.add_cog(Verify(bot))
