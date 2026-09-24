import discord

from config.i18n import t


async def on_guild_join(bot, guild):
    # This event is triggered when the bot joins a new guild
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed = discord.Embed(
                title=t("guild_join.title", guild_name=guild.name),
                description=t("guild_join.description"),
                color=discord.Color.blue(),
            )
            embed.add_field(
                name="/setup",
                value=t("guild_join.setup"),
                inline=False,
            )
            embed.add_field(
                name="/help",
                value=t("guild_join.help"),
                inline=False,
            )
            embed.set_footer(text=t("guild_join.footer"))
            view = discord.ui.View()
            view.add_item(
                discord.ui.Button(
                    style=discord.ButtonStyle.url,
                    label=t("guild_join.support_button"),
                    url="https://discord.gg/rcAREJyMV5",
                )
            )
            await channel.send(
                t("guild_join.thanks"),
                embed=embed,
                view=view,
            )
            break

    # Bot-wide operational audit stays in English for upstream/debug parity.
    embed = discord.Embed(
        title="Joined a New Server!",
        description="",
        color=discord.Color.green(),
    )
    embed.add_field(name="Server Name", value=guild.name, inline=True)
    embed.add_field(name="Server ID", value=guild.id, inline=True)
    embed.add_field(name="Owner", value=f"{guild.owner} (ID: {guild.owner_id})", inline=True)
    embed.add_field(name="Member Count", value=guild.member_count, inline=True)
    embed.add_field(name="Text Channel Count", value=str(len(guild.text_channels)), inline=True)
    embed.add_field(name="Region/Locale", value=str(guild.preferred_locale), inline=True)
    unix_time = int(guild.created_at.timestamp())
    embed.add_field(name="Creation Date", value=f"<t:{unix_time}:f>\n<t:{unix_time}:R>", inline=True)
    unix_time = int(guild.get_member(bot.user.id).joined_at.timestamp())
    embed.add_field(name="Joined Date", value=f"<t:{unix_time}:f>\n<t:{unix_time}:R>", inline=True)
    await bot.BotLogService.send(event="guild_join", message="", embed=embed)


async def on_guild_remove(bot, guild):
    # Bot-wide operational audit stays in English for upstream/debug parity.
    embed = discord.Embed(
        title="Left a Server!",
        description="",
        color=discord.Color.red(),
    )
    embed.add_field(name="Server Name", value=guild.name, inline=True)
    embed.add_field(name="Server ID", value=guild.id, inline=True)
    embed.add_field(name="Owner", value=f"{guild.owner} (ID: {guild.owner_id})", inline=True)
    embed.add_field(name="Member Count", value=guild.member_count, inline=True)
    embed.add_field(name="Text Channel Count", value=str(len(guild.text_channels)), inline=True)
    embed.add_field(name="Region/Locale", value=str(guild.preferred_locale), inline=True)
    unix_time = int(guild.created_at.timestamp())
    embed.add_field(name="Creation Date", value=f"<t:{unix_time}:f>\n<t:{unix_time}:R>", inline=True)
    unix_time = int(guild.get_member(bot.user.id).joined_at.timestamp())
    embed.add_field(name="Joined Date", value=f"<t:{unix_time}:f>\n<t:{unix_time}:R>", inline=True)
    await bot.BotLogService.send(event="guild_leave", message="", embed=embed)
