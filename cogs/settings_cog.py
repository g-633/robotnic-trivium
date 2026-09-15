import discord
from discord.ext import commands
from cogs.settings.modals import SettingsModal, LogsModal, PlaceholdersModal


class SettingsMenuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    settings = discord.SlashCommandGroup(
        "settings",
        "Change Guild Settings",
        default_member_permissions=discord.Permissions(manage_channels=True),
    )

    @settings.command(description="Select which controls users should have access to by default")
    async def logging(
            self,
            ctx: discord.ApplicationContext,
    ):
        await ctx.send_modal(LogsModal(self.bot, ctx))

        embed = discord.Embed(
            title="",
            description=f"Make sure to click \"SUBMIT\" after editing the pop-up menu.",
            color=discord.Color.yellow()
        )
        embed.set_footer(text="This message will disappear in 30 seconds.")
        reply = await ctx.send_followup(embed=embed, ephemeral=True, wait=True)
        await reply.delete(delay=30)

    @settings.command(description="Select which controls users should have access to by default")
    async def controls(
        self,
        ctx: discord.ApplicationContext,
    ):
        await ctx.send_modal(SettingsModal(self.bot, ctx))

        embed = discord.Embed(
            title="",
            description=f"Make sure to click \"SUBMIT\" after editing the pop-up menu.",
            color=discord.Color.yellow()
        )
        embed.set_footer(text="This message will disappear in 30 seconds.")
        reply = await ctx.send_followup(embed=embed, ephemeral=True, wait=True)
        await reply.delete(delay=30)

    @settings.command(description="Set the profanity check in channel names")
    async def profanity_filter(
        self,
        ctx: discord.ApplicationContext,
        mode: discord.Option(
            str,
            choices=["off", "alert", "alert & block"],
            description="Filter mode, alert will send a profanity alert in the logs channel."
        )
    ):
        self.bot.repos.guild_settings.edit(ctx.guild_id, profanity_filter=mode)
        await ctx.respond(
            f"profanity filter set to `{mode}`"
        )

    @settings.command(name="dm-owner", description="Enable or disable DMing channel owners on create")
    async def dm_owner(
        self,
        ctx: discord.ApplicationContext,
        enabled: discord.Option(
            bool,
            description="Whether to DM owners when they create a channel",
        ),
    ):
        self.bot.repos.guild_settings.edit(ctx.guild_id, dm_owner=enabled)
        await ctx.respond(f"dm-owner set to `{enabled}`")

    placeholder = settings.create_subgroup(
        "placeholder",
        "Manage custom channel name placeholders",
    )

    @placeholder.command(name="add", description="Add a custom channel name placeholder")
    async def add_placeholder(
        self,
        ctx: discord.ApplicationContext,
    ):
        await ctx.send_modal(PlaceholdersModal(self.bot, ctx))

        embed = discord.Embed(
            title="",
            description=f"Make sure to click \"SUBMIT\" after editing the pop-up menu.",
            color=discord.Color.yellow()
        )
        embed.set_footer(text="This message will disappear in 30 seconds.")
        reply = await ctx.send_followup(embed=embed, ephemeral=True, wait=True)
        await reply.delete(delay=30)

    @placeholder.command(name="list", description="List custom channel name placeholders")
    async def list_placeholder(
        self,
        ctx: discord.ApplicationContext,
    ):
        placeholders = self.bot.repos.placeholders.list(ctx.guild_id)
        if not placeholders:
            await ctx.respond("No custom placeholders configured.", ephemeral=True)
            return

        embed = discord.Embed(
            title="Custom Placeholders",
            color=discord.Color.blue(),
        )
        for entry in placeholders:
            role = ctx.guild.get_role(entry["role_id"]) if entry["role_id"] else None
            role_text = role.mention if role else "`None`"
            embed.add_field(
                name=f"`{entry['placeholder']}`",
                value=f"Replace: `{entry['replace_text']}`\nRole Required: {role_text}",
                inline=False,
            )
        await ctx.respond(embed=embed, ephemeral=True)

    @placeholder.command(name="remove", description="Remove a custom channel name placeholder")
    async def remove_placeholder(
        self,
        ctx: discord.ApplicationContext,
        placeholder: discord.Option(
            str,
            description="The placeholder to remove, e.g. {game}",
        ),
    ):
        removed = self.bot.repos.placeholders.remove(ctx.guild_id, placeholder)
        if removed:
            await ctx.respond(f"Removed placeholder `{placeholder}`.", ephemeral=True)
        else:
            await ctx.respond(f"No placeholder `{placeholder}` found.", ephemeral=True)


def setup(bot):
    bot.add_cog(SettingsMenuCog(bot))
