import discord
from cogs.control_vc.enums import ChannelState
from cogs.manage_vcs.create_name import create_temp_channel_name
from config.i18n import t


class ControlIconsEmbed(discord.Embed):
    def __init__(self, bot, channel):
        super().__init__(
            title="",
            description="",
            color=0x00ff00
        )

        self.add_field(name=t("control_panel.icons.rename"), value="", inline=True)
        self.add_field(name=t("control_panel.icons.limit"), value="", inline=True)
        self.add_field(name=t("control_panel.icons.give"), value="", inline=True)
        self.add_field(name=t("control_panel.icons.clear"), value="", inline=True)
        self.add_field(name=t("control_panel.icons.access"), value="", inline=True)
        self.add_field(name=t("control_panel.icons.mute"), value="", inline=True)
        self.add_field(name=t("control_panel.icons.deafen"), value="", inline=True)
        self.add_field(name=t("control_panel.icons.delete"), value="", inline=True)
        control_options = bot.repos.guild_settings.get(channel.guild.id)["control_options"]
        if "state_changeable" in control_options:
            self.add_field(name=t("control_panel.icons.public"), value="", inline=True)
            self.add_field(name=t("control_panel.icons.hide"), value="", inline=True)
            self.add_field(name=t("control_panel.icons.lock"), value="", inline=True)


class ChannelInfoEmbed(discord.Embed):
    def __init__(self, bot, temp_channel, title=None, user_limit=None):
        super().__init__(
            color=discord.Color.blue()
        )

        temp_channel_info = bot.repos.temp_channels.get_info(temp_channel.id)

        # title input incase it was just changed and propagated to channel yet
        self.title = title
        if not self.title:
            is_renamed = temp_channel_info.is_renamed
            if is_renamed:
                self.title = f"{temp_channel.name}"
            else:
                self.title = create_temp_channel_name(bot, temp_channel)

        self.footer = discord.EmbedFooter(t("control_panel.info.rename_footer"))

        owner_id = temp_channel_info.owner_id
        if owner_id:
            if owner_id is not None:
                owner = f"<@{owner_id}>"
            else:
                owner = t("control_panel.info.no_owner")
        else:
            owner = t("control_panel.info.no_owner")
        self.add_field(name=t("control_panel.info.owner"), value=f"{owner}", inline=True)

        if not user_limit:
            user_limit = temp_channel.user_limit
        if user_limit == 0:
            user_limit = t("control_panel.info.unlimited")
        self.add_field(name=t("control_panel.info.user_limit"), value=f"{user_limit}", inline=True)

        # region = temp_channel.rtc_region
        # if region is None:
        #     region = "🌍 Auto"
        # self.add_field(name="Region", value=f"{region}", inline=True)

        control_options = bot.repos.guild_settings.get(temp_channel.guild.id)["control_options"]
        if "state_changeable" in control_options:
            channel_state_id = temp_channel_info.channel_state
            if channel_state_id == ChannelState.PUBLIC.value:
                channel_state = t("control_panel.info.public")
            elif channel_state_id == ChannelState.LOCKED.value:
                channel_state = t("control_panel.info.locked")
            elif channel_state_id == ChannelState.HIDDEN.value:
                channel_state = t("control_panel.info.hidden")
            else:
                channel_state = t("control_panel.info.none")
            self.add_field(name=t("control_panel.info.access"), value=f"{channel_state}", inline=True)
