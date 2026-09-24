import logging
import discord
from config.i18n import t

logger = logging.getLogger(__name__)


async def on_application_command_error(self, ctx, exception):
    if isinstance(exception.original, discord.Forbidden):
        await ctx.send(t("lifecycle.application_error.permissions"))
    else:
        logger.error(f"ERROR in {__name__}\nContext: {ctx}\nException: {exception}")
        await ctx.send(t("lifecycle.application_error.generic"))
