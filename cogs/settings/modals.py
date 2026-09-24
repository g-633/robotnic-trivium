import discord
from discord.ui import View, Select, Button, Modal, InputText

from config.i18n import t


def display_list(items):
    items = [f"`{item}`" for item in items]
    if not items:
        return t("settings.none")
    return ", ".join(items)


class ControlsModal(discord.ui.DesignerModal):
    def __init__(self, bot, ctx):
        super().__init__(title=t("settings.controls.modal_title"))
        self.bot = bot
        guild_settings = self.bot.repos.guild_settings.get(ctx.guild.id)

        self._add_enabled_controls(guild_settings)
        self._add_mention_owner(guild_settings)
        self._add_control_options(guild_settings)

    def _add_enabled_controls(self, guild_settings):
        enabled_controls = guild_settings["enabled_controls"]
        controls_options = [
            discord.SelectOption(value="rename", label=t("settings.controls.actions.rename"), emoji="🏷️", default="rename" in enabled_controls),
            discord.SelectOption(value="limit", label=t("settings.controls.actions.limit"), emoji="🚧", default="limit" in enabled_controls),
            discord.SelectOption(value="clear", label=t("settings.controls.actions.clear"), emoji="🧽", default="clear" in enabled_controls),
            discord.SelectOption(value="ban", label=t("settings.controls.actions.ban"), emoji="🔨", default="ban" in enabled_controls),
            discord.SelectOption(value="mute", label=t("settings.controls.actions.mute"), emoji="🔇", default="mute" in enabled_controls),
            discord.SelectOption(value="deafen", label=t("settings.controls.actions.deafen"), emoji="🔕", default="deafen" in enabled_controls),
            discord.SelectOption(value="give", label=t("settings.controls.actions.give"), emoji="🎁", default="give" in enabled_controls),
            discord.SelectOption(value="delete", label=t("settings.controls.actions.delete"), emoji="🗑️", default="delete" in enabled_controls),
            discord.SelectOption(value="lock", label=t("settings.controls.actions.lock"), emoji="🔒", default="lock" in enabled_controls),
            discord.SelectOption(value="hide", label=t("settings.controls.actions.hide"), emoji="🙈", default="hide" in enabled_controls),
        ]
        controls_select = Select(
            placeholder=t("settings.controls.enabled_placeholder"),
            options=controls_options,
            max_values=len(controls_options),
            min_values=0,
            required=False,
        )
        self.controls_select_label = discord.ui.Label(
            t("settings.controls.enabled_label"),
            controls_select,
        )
        self.add_item(self.controls_select_label)

    def _save_enabled_controls(self, guild_id, embed):
        enabled_controls = self.controls_select_label.item.values
        self.bot.repos.guild_settings.edit(
            guild_id,
            enabled_controls=list(enabled_controls),
        )
        display_values = [
            t(f"settings.controls.actions.{control}")
            for control in enabled_controls
        ]
        embed.add_field(
            name=t("settings.controls.enabled_field"),
            value=display_list(display_values),
            inline=False,
        )

    def _add_mention_owner(self, guild_settings):
        mention_owner = guild_settings["mention_owner_bool"]
        options = [
            discord.SelectOption(
                value="true",
                label=t("settings.controls.mention_yes"),
                default=mention_owner,
            ),
            discord.SelectOption(
                value="false",
                label=t("settings.controls.mention_no"),
                default=not mention_owner,
            ),
        ]

        self.mention_owner_label = discord.ui.Label(
            t("settings.controls.mention_label"),
            discord.ui.Select(
                options=options,
                min_values=1,
                max_values=1,
                required=True,
            ),
        )
        self.add_item(self.mention_owner_label)

    def _save_mention_owner(self, guild_id, embed):
        should_mention = self.mention_owner_label.item.values[0] == "true"
        self.bot.repos.guild_settings.edit(guild_id, mention_owner=should_mention)
        embed.add_field(
            name=t("settings.controls.mention_field"),
            value=t("settings.enabled" if should_mention else "settings.disabled"),
            inline=False,
        )

    def _add_control_options(self, guild_settings):
        enabled_options = guild_settings["control_options"]
        if "dropdown" in enabled_options:
            default = "dropdown"
        elif "buttons" in enabled_options and "labels" in enabled_options:
            default = "buttons_labels"
        else:
            default = "buttons_icons"

        control_options = [
            discord.SelectOption(
                value="dropdown",
                label=t("settings.controls.types.dropdown"),
                default=default == "dropdown",
            ),
            discord.SelectOption(
                value="buttons_labels",
                label=t("settings.controls.types.buttons_labels"),
                default=default == "buttons_labels",
            ),
            discord.SelectOption(
                value="buttons_icons",
                label=t("settings.controls.types.buttons_icons"),
                default=default == "buttons_icons",
            ),
        ]
        options_select = Select(
            placeholder=t("settings.controls.type_placeholder"),
            options=control_options,
            max_values=1,
            min_values=1,
            required=True,
        )
        self.options_select_label = discord.ui.Label(
            t("settings.controls.type_label"),
            options_select,
        )
        self.add_item(self.options_select_label)

    def _save_control_options(self, guild_id, embed):
        control_type = self.options_select_label.item.values[0]
        control_type_map = {
            "dropdown": {"dropdown", "labels"},
            "buttons_labels": {"buttons", "icons", "labels"},
            "buttons_icons": {"buttons", "icons"},
        }
        selected_control_options = list(control_type_map.get(control_type, []))

        self.bot.repos.guild_settings.edit(
            guild_id,
            control_options=selected_control_options,
        )
        embed.add_field(
            name=t("settings.controls.type_field"),
            value=t(f"settings.controls.types.{control_type}"),
            inline=False,
        )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=t("settings.controls.submitted"),
            description="",
            color=discord.Color.green(),
        )
        embed.set_footer(text=t("common.message_disappears", seconds=60))

        self._save_enabled_controls(interaction.guild_id, embed)
        self._save_mention_owner(interaction.guild_id, embed)
        self._save_control_options(interaction.guild_id, embed)

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True,
            delete_after=60,
        )


class LogsModal(discord.ui.DesignerModal):
    def __init__(self, bot, ctx):
        super().__init__(title=t("settings.logs.modal_title"))
        self.bot = bot
        guild_settings = self.bot.repos.guild_settings.get(ctx.guild.id)

        self._add_log_channel(guild_settings)
        self._add_log_events(guild_settings)

    def _add_log_channel(self, guild_settings):
        if guild_settings["logs_channel_id"] is not None and int(guild_settings["logs_channel_id"]) != 0:
            log_channel = self.bot.get_channel(guild_settings["logs_channel_id"])
        else:
            log_channel = None

        self.log_channel_select = discord.ui.Label(
            t("settings.logs.channel_label"),
            discord.ui.ChannelSelect(
                channel_types=[discord.ChannelType.text],
                min_values=1,
                max_values=1,
                default_values=[log_channel] if log_channel else None,
                required=False,
            ),
        )
        self.add_item(self.log_channel_select)

    def _save_log_channel(self, guild_id, embed):
        if len(self.log_channel_select.item.values) >= 1:
            log_channel = self.log_channel_select.item.values[0]
            self.bot.repos.guild_settings.edit(
                guild_id,
                logs_channel_id=log_channel.id,
            )
            value = f"{log_channel.mention}/`#{log_channel.name}` (`{log_channel.id}`)"
        else:
            self.bot.repos.guild_settings.edit(guild_id, logs_channel_id=0)
            value = t("settings.logs.disabled_value")

        embed.add_field(
            name=t("settings.logs.selected_channel_field"),
            value=value,
            inline=False,
        )

    def _add_log_events(self, guild_settings):
        enabled_events = guild_settings["enabled_log_events"]
        events_options = [
            discord.SelectOption(value="channel_create", label=t("settings.logs.events.channel_create"), emoji="🎁", default="channel_create" in enabled_events),
            discord.SelectOption(value="channel_rename", label=t("settings.logs.events.channel_rename"), emoji="🏷️", default="channel_rename" in enabled_events),
            discord.SelectOption(value="channel_remove", label=t("settings.logs.events.channel_remove"), emoji="🗑️", default="channel_remove" in enabled_events),
            discord.SelectOption(value="profanity_block", label=t("settings.logs.events.profanity_block"), emoji="😶", default="profanity_block" in enabled_events),
        ]
        events_select = Select(
            placeholder=t("settings.logs.events_placeholder"),
            options=events_options,
            max_values=len(events_options),
            min_values=0,
            required=False,
        )

        self.events_select_label = discord.ui.Label(
            t("settings.logs.events_label"),
            events_select,
        )
        self.add_item(self.events_select_label)

    def _save_log_events(self, guild_id, embed):
        enabled_log_events = self.events_select_label.item.values
        self.bot.repos.guild_settings.edit(
            guild_id,
            enabled_log_events=enabled_log_events,
        )
        display_values = [
            t(f"settings.logs.events.{event}")
            for event in enabled_log_events
        ]
        embed.add_field(
            name=t("settings.logs.enabled_events_field"),
            value=display_list(display_values),
            inline=False,
        )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=t("settings.logs.submitted"),
            description="",
            color=discord.Color.green(),
        )
        embed.set_footer(text=t("common.message_disappears", seconds=60))

        self._save_log_channel(interaction.guild_id, embed)
        self._save_log_events(interaction.guild_id, embed)

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True,
            delete_after=60,
        )
