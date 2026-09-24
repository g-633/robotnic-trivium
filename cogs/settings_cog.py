import discord
from discord.ext import commands
from cogs.settings.modals import ControlsModal, LogsModal
from cogs.settings.placeholders.modals import PlaceholderAddModal
from config.i18n import t


async def placeholder_remove_autocomplete(ctx: discord.AutocompleteContext):
    entries = ctx.bot.repos.placeholders.get_all(ctx.interaction.guild.id)
    query = (ctx.value or "").lower()
    choices = []
    for entry in entries:
        role = (
            ctx.interaction.guild.get_role(entry["role_id"])
            if entry["role_id"]
            else None
        )
        label = t(
            "settings.placeholder.autocomplete",
            placeholder=entry["placeholder"],
            replace_text=entry["replace_text"],
            role_name=role.name if role else "@everyone",
        )
        if query and query not in label.lower():
            continue
        choices.append(discord.OptionChoice(name=label[:100], value=str(entry["id"])))
        if len(choices) >= 25:
            break
    return choices


class SettingsMenuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    settings = discord.SlashCommandGroup(
        "settings",
        t("settings.group_description"),
        default_member_permissions=discord.Permissions(manage_channels=True),
    )

    @settings.command(description=t("settings.logging_description"))
    async def logging(
        self,
        ctx: discord.ApplicationContext,
    ):
        await ctx.send_modal(LogsModal(self.bot, ctx))

        embed = discord.Embed(
            title="",
            description=t("settings.submit_hint"),
            color=discord.Color.yellow(),
        )
        embed.set_footer(text=t("common.message_disappears", seconds=30))
        reply = await ctx.send_followup(embed=embed, ephemeral=True, wait=True)
        await reply.delete(delay=30)

    @settings.command(description=t("settings.controls_description"))
    async def controls(
        self,
        ctx: discord.ApplicationContext,
    ):
        await ctx.send_modal(ControlsModal(self.bot, ctx))

        embed = discord.Embed(
            title="",
            description=t("settings.submit_hint"),
            color=discord.Color.yellow(),
        )
        embed.set_footer(text=t("common.message_disappears", seconds=30))
        reply = await ctx.send_followup(embed=embed, ephemeral=True, wait=True)
        await reply.delete(delay=30)

    @settings.command(description=t("settings.profanity_description"))
    async def profanity_filter(
        self,
        ctx: discord.ApplicationContext,
        mode: discord.Option(
            str,
            choices=[
                discord.OptionChoice(
                    name=t("settings.profanity_choices.off"),
                    value="off",
                ),
                discord.OptionChoice(
                    name=t("settings.profanity_choices.alert"),
                    value="alert",
                ),
                discord.OptionChoice(
                    name=t("settings.profanity_choices.alert_block"),
                    value="alert & block",
                ),
            ],
            description=t("settings.profanity_mode_description"),
        ),
    ):
        self.bot.repos.guild_settings.edit(ctx.guild_id, profanity_filter=mode)
        mode_key = {
            "off": "off",
            "alert": "alert",
            "alert & block": "alert_block",
        }[mode]
        await ctx.respond(
            t(
                "settings.profanity_saved",
                mode=t(f"settings.profanity_choices.{mode_key}"),
            )
        )

    @settings.command(
        name="dm-owner",
        description=t("settings.dm_owner_description"),
    )
    async def dm_owner(
        self,
        ctx: discord.ApplicationContext,
        enabled: discord.Option(
            bool,
            description=t("settings.dm_owner_option_description"),
        ),
    ):
        self.bot.repos.guild_settings.edit(ctx.guild_id, dm_owner=enabled)
        await ctx.respond(
            t(
                "settings.dm_owner_saved",
                state=t("settings.enabled" if enabled else "settings.disabled"),
            )
        )

    placeholder = settings.create_subgroup(
        "placeholder",
        t("settings.placeholder.group_description"),
    )

    @placeholder.command(
        name="add",
        description=t("settings.placeholder.add_description"),
    )
    async def add_placeholder(
        self,
        ctx: discord.ApplicationContext,
    ):
        await ctx.send_modal(PlaceholderAddModal(self.bot, ctx))

        embed = discord.Embed(
            title="",
            description=t("settings.submit_hint"),
            color=discord.Color.yellow(),
        )
        embed.set_footer(text=t("common.message_disappears", seconds=30))
        reply = await ctx.send_followup(embed=embed, ephemeral=True, wait=True)
        await reply.delete(delay=30)

    @placeholder.command(
        name="list",
        description=t("settings.placeholder.list_description"),
    )
    async def list_placeholder(
        self,
        ctx: discord.ApplicationContext,
    ):
        placeholders = self.bot.repos.placeholders.get_all(ctx.guild.id)
        if not placeholders:
            await ctx.respond(
                t("settings.placeholder.empty"),
                ephemeral=True,
            )
            return

        lines = []
        for entry in placeholders:
            role = ctx.guild.get_role(entry["role_id"]) if entry["role_id"] else None
            lines.append(
                t(
                    "settings.placeholder.list_line",
                    placeholder=entry["placeholder"],
                    replace_text=entry["replace_text"],
                    role=role.mention if role else "`@everyone`",
                )
            )

        embed = discord.Embed(
            title=t(
                "settings.placeholder.list_title",
                count=len(placeholders),
            ),
            description="\n".join(lines),
            color=discord.Color.blue(),
        )
        await ctx.respond(embed=embed, ephemeral=True)

    @placeholder.command(
        name="remove",
        description=t("settings.placeholder.remove_description"),
    )
    async def remove_placeholder(
        self,
        ctx: discord.ApplicationContext,
        entry: discord.Option(
            str,
            description=t("settings.placeholder.remove_option_description"),
            autocomplete=placeholder_remove_autocomplete,
        ),
    ):
        try:
            entry_id = int(entry)
        except (TypeError, ValueError):
            await ctx.respond(
                t("settings.placeholder.invalid_selection"),
                ephemeral=True,
            )
            return

        existing = self.bot.repos.placeholders.get(ctx.guild.id, entry_id)
        if not existing:
            await ctx.respond(
                t("settings.placeholder.not_found"),
                ephemeral=True,
            )
            return

        self.bot.repos.placeholders.remove(ctx.guild.id, entry_id)
        await ctx.respond(
            t(
                "settings.placeholder.removed",
                placeholder=existing["placeholder"],
                replace_text=existing["replace_text"],
            ),
            ephemeral=True,
        )


def setup(bot):
    bot.add_cog(SettingsMenuCog(bot))
