import discord

from config.i18n import t


class ButtonsView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.create_items()

    def create_items(self):
        self.add_item(
            discord.ui.Button(
                label=t("general.buttons.source"),
                url="https://github.com/g-633/robotnic-trivium",
                emoji="📦",
                style=discord.ButtonStyle.link,
            )
        )
        self.add_item(
            discord.ui.Button(
                label=t("general.buttons.kofi"),
                url="https://ko-fi.com/jackschultzdev",
                emoji="💖",
                style=discord.ButtonStyle.link,
            )
        )
        self.add_item(
            discord.ui.Button(
                label=t("general.buttons.support_server"),
                url="https://discord.gg/rcAREJyMV5",
                emoji="🔧",
                style=discord.ButtonStyle.link,
            )
        )
        self.add_item(
            discord.ui.Button(
                label=t("general.buttons.website"),
                url="https://jackschultz.dev/Robotnic/",
                emoji="🌏",
                style=discord.ButtonStyle.link,
            )
        )
