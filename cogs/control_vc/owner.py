import logging

from config.i18n import t

logger = logging.getLogger(__name__)


async def claim_or_verify_owner(bot, channel, user):
    if user not in channel.members:
        logger.debug(
            f"User '{user}' interacted with control that they are not connected to "
            f"in guild '{channel.guild.name}'."
        )
        return False, t("control_panel.errors.not_connected", mention=user.mention)

    connected_user_ids = [member.id for member in channel.members]
    owner_id = bot.repos.temp_channels.get_info(channel.id).owner_id

    # If owner isn't connected, make interacting user owner and update info embed
    if owner_id is None or owner_id not in connected_user_ids:
        bot.repos.temp_channels.set_owner_id(channel.id, user.id)
        await bot.EmbedUpdateScheduler.schedule(channel)

    # If owner is connected and isn't interacting user, deny
    elif owner_id != user.id:
        logger.debug(
            f"User '{user}' interacted with control that they don't own "
            f"in guild '{channel.guild.name}'."
        )
        return False, t("control_panel.errors.not_owner", mention=user.mention)

    return True, None


async def is_owner(view, interaction):
    ok, error = await claim_or_verify_owner(
        view.bot, interaction.channel, interaction.user
    )
    if not ok:
        await interaction.response.send_message(
            error, ephemeral=True, delete_after=15
        )
        return False
    return True
