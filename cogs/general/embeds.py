import discord


class DonateEmbed(discord.Embed):
    def __init__(self):
        super().__init__()
        self.color = discord.Color.green()
        self.title = "💚 Thank you for using Robotnic!"
        self.description = (
            "\n"
            "This bot as a **[FOSS](<https://wikipedia.org/wiki/Free_and_open-source_software>)** project with a **free** to use public instance, however this **costs money**. Current donations do not even cover hosting costs."
        )
        self.add_field(
            name="💸 Please Consider Supporting through Ko-fi!",
            value="",
            inline=False
        )


class HelpEmbed(discord.Embed):
    def __init__(self):
        super().__init__()
        self.color = discord.Color.green()
        self.title = "Command List"
        self.description = (
        )
        self.add_field(
            name="/setup",
            value=(
                "Use this menu to create new `Creator Channel`s by clicking the green \"Make new Creator\" button or edit existing `Creator Channel`s using the dropdown list."
            ),
            inline=True
        )
        self.add_field(
            name="/settings controls",
            value="Allows changing the controls available to channel owners. Every button is togglable and you can choose between labeled buttons, icons or a dropdown menu as controls.",
            inline=True
        )
        self.add_field(
            name="/settings logging",
            value="Allows for setting a log channel, if set, selected events will be logged in that channel. To customise the list, simply deselect the ones you would not like to include.",
            inline=True
        )
        self.add_field(
            name="/settings profanity_filter",
            value="While still basic, this setting allows for disabling or only sending an alert if the profanity filter is triggered rather than blocking the action.",
            inline=True
        )
        self.add_field(
            name="/settings dm-owner",
            value="Enable or disable DMing channel owners when they create a temporary channel. Defaults to on.",
            inline=True
        )
        self.add_field(
            name="/settings placeholder add",
            value="Add a custom placeholder for use in the naming scheme of a channel creator",
            inline=True
        )
        self.add_field(
            name="/settings placeholder list",
            value="List all custom placeholders for this server",
            inline=True
        )
        self.add_field(
            name="/settings placeholder remove",
            value="Remove a custom placeholder for this server",
            inline=True
        )
        self.add_field(
            name="/donate | /support | /website",
            value="Returns with information on how to support Robotnic's uptime.",
            inline=True
        )
        self.set_footer(text="📩 Need more help? Reach out to support below!")