import discord


class PlaceholderAddModal(discord.ui.DesignerModal):
    def __init__(self, bot, ctx):
        super().__init__(title="Add Placeholder")
        self.bot = bot

        self.placeholder_label = discord.ui.Label(
            "Placeholder",
            discord.ui.TextInput(
                placeholder="e.g. {game}",
                required=True,
                max_length=100,
            ),
        )
        self.add_item(self.placeholder_label)

        self.replace_text_label = discord.ui.Label(
            "Replace Text",
            discord.ui.TextInput(
                placeholder="Text to replace the placeholder with",
                required=True,
                max_length=100,
            ),
        )
        self.add_item(self.replace_text_label)

        self.role_required_label = discord.ui.Label(
            "Role Required",
            discord.ui.RoleSelect(
                min_values=0,
                max_values=1,
                required=False,
                placeholder="Optional role required to use this placeholder",
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
            title="Placeholder Added!",
            description="",
            color=discord.Color.green(),
        )
        embed.add_field(name="Placeholder", value=f"`{placeholder}`", inline=False)
        embed.add_field(name="Replace Text", value=f"`{replace_text}`", inline=False)
        embed.add_field(
            name="Role Required",
            value=role.mention if role else "`None`",
            inline=False,
        )
        embed.set_footer(text="This message will disappear in 60 seconds.")

        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=60)
