import discord

from config.i18n import t


class DonateEmbed(discord.Embed):
    def __init__(self):
        super().__init__()
        self.color = discord.Color.green()
        self.title = t("general.donate.title")
        self.description = t("general.donate.description")
        self.add_field(
            name=t("general.donate.field"),
            value="",
            inline=False,
        )


class HelpEmbed(discord.Embed):
    def __init__(self):
        super().__init__()
        self.color = discord.Color.green()
        self.title = t("general.help.title")
        self.add_field(
            name="/setup",
            value=t("general.help.setup"),
            inline=True,
        )
        self.add_field(
            name="/settings controls",
            value=t("general.help.controls"),
            inline=True,
        )
        self.add_field(
            name="/settings logging",
            value=t("general.help.logging"),
            inline=True,
        )
        self.add_field(
            name="/settings profanity_filter",
            value=t("general.help.profanity"),
            inline=True,
        )
        self.add_field(
            name="/settings dm-owner",
            value=t("general.help.dm_owner"),
            inline=True,
        )
        self.add_field(
            name="/settings placeholder add",
            value=t("general.help.placeholder_add"),
            inline=True,
        )
        self.add_field(
            name="/settings placeholder list",
            value=t("general.help.placeholder_list"),
            inline=True,
        )
        self.add_field(
            name="/settings placeholder remove",
            value=t("general.help.placeholder_remove"),
            inline=True,
        )
        self.add_field(
            name="/donate | /support | /website",
            value=t("general.help.donate"),
            inline=True,
        )
        self.set_footer(text=t("general.help.footer"))
