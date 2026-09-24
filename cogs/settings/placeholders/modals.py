import discord

from config.i18n import t


class PlaceholderAddModal(discord.ui.DesignerModal):
    def __init__(self, bot, ctx):
        super().__init__(title=t("settings.placeholder.modal_title"))
        self.bot = bot

        self.placeholder_label = discord.ui.Label(
            t("settings.placeholder.placeholder_label"),
            discord.ui.TextInput(
                placeholder=t("settings.placeholder.placeholder_example"),
                required=True,
                max_length=100,
            ),
        )
        self.add_item(self.placeholder_label)

        self.replace_text_label = discord.ui.Label(
            t("settings.placeholder.replace_text_label"),
            discord.ui.TextInput(
                placeholder=t("settings.placeholder.replace_text_placeholder"),
                required=True,
                max_length=100,
            ),
        )
        self.add_item(self.replace_text_label)

        self.role_required_label = discord.ui.Label(
            t("settings.placeholder.role_label"),
            discord.ui.RoleSelect(
                min_values=0,
                max_values=1,
                required=False,
                placeholder=t("settings.placeholder.role_placeholder"),
            ),
        )
        self.add_item(self.role_required_label)

    async def callback(self, interaction: discord.Interaction):
        placeholder = self.placeholder_label.item.value.strip()
        replace_text = self.replace_text_label.item.value
        role = self.role_required_label.item.values[0] if self.role_required_label.item.values else None

        self.bot.repos.placeholders.add(
            guild_id=interaction.guild.id,
            placeholder=placeholder,
            replace_text=replace_text,
            role_id=role.id if role else None,
        )

        embed = discord.Embed(
            title=t("settings.placeholder.added_title"),
            description="",
            color=discord.Color.green(),
        )
        embed.add_field(
            name=t("settings.placeholder.field_placeholder"),
            value=f"`{placeholder}`",
            inline=False,
        )
        embed.add_field(
            name=t("settings.placeholder.field_replace_text"),
            value=f"`{replace_text}`",
            inline=False,
        )
        embed.add_field(
            name=t("settings.placeholder.field_role"),
            value=role.mention if role else "`@everyone`",
            inline=False,
        )
        embed.set_footer(text=t("common.message_disappears", seconds=60))

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True,
            delete_after=60,
        )
