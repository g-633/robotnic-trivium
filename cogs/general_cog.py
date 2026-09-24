import discord
from discord.ext import commands
from cogs.general.embeds import DonateEmbed, HelpEmbed
from cogs.general.views import ButtonsView
from config.i18n import t


class GeneralCCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description=t("general.ping_description"))
    @discord.default_permissions(manage_channels=True)
    async def ping(self, ctx):
        await ctx.respond(
            t("general.ping_response", latency=self.bot.latency)
        )

    @discord.slash_command(description=t("general.help_description"))
    async def help(self, ctx):
        await ctx.respond("", embeds=[HelpEmbed()], view=ButtonsView())

    @discord.slash_command(description=t("general.donate_description"))
    async def donate(self, ctx):
        await ctx.respond("", embeds=[DonateEmbed()], view=ButtonsView())

    # Alias to /donate
    @discord.slash_command(description=t("general.support_description"))
    async def support(self, ctx):
        await self.donate.callback(self, ctx)

    # Alias to /donate
    @discord.slash_command(description=t("general.website_description"))
    async def website(self, ctx):
        await self.donate.callback(self, ctx)


def setup(bot):
    bot.add_cog(GeneralCCog(bot))
