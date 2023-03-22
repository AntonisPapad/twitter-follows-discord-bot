import asyncio
import discord
from discord.ext import commands
# from datetime import datetime
from twitter_functions import get_user, get_new_friends
from db_functions import add_user, remove_user, check_for_user, read_channel_id, write_channel_id, get_tracked_users, update_friends_number, delete_channel_id
from config import read_config


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Bot is online")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

    # Read the stored channel_id when the bot comes online
    bot.tracked_channel_id = read_channel_id()
    if bot.tracked_channel_id is not None:
        bot.loop.create_task(track_users())


async def track_users():
    while bot.tracked_channel_id is not None:
        tracked_users = get_tracked_users()
        if tracked_users:   # check if the database is not empty
            for user in tracked_users:
                (username, friends_num) = user
                new_friends = get_new_friends(username, friends_num)
                if new_friends is not None:
                    update_friends_number(username, len(new_friends))

                    for friend in new_friends:
                        profile = friend.screen_name
                        url = f"https://www.twitter.com/{profile}"
                        follower_num = friend.followers_count
                        pfp_url = friend.profile_image_url
                        date_created = friend.created_at.date()

                        embed = discord.Embed(color=discord.Color.blue())

                        embed.add_field(
                            name="",
                            value=f"**[{profile}]({url})**",
                            inline=False
                        )

                        embed.add_field(
                            name="**Was followed by:**",
                            value=username,
                            inline=False
                        )

                        embed.add_field(
                            name="**Profile Stats:**",
                            value=(
                                f"Followers: {follower_num}\n"
                                f"Account Created: {date_created}"
                            ),
                            inline=False
                        )

                        embed.set_thumbnail(url=pfp_url)

                        channel = bot.get_channel(bot.tracked_channel_id)
                        await channel.send(embed=embed)

        await asyncio.sleep(10)


@bot.tree.command(name="start", description="Initialize the bot")
async def start(interaction: discord.Interaction):
    bot.tracked_channel_id = interaction.channel_id
    user = str(interaction.user)
    # Store the channel_id and the discord user when the /start command is called
    write_channel_id(bot.tracked_channel_id, user)
    await interaction.response.send_message("Bot initiated", ephemeral=True)
    bot.loop.create_task(track_users())  # Start the track_users task here


@bot.tree.command(name="stop", description="Stop the bot")
async def stop(interaction: discord.Interaction):
    bot.tracked_channel_id = None
    # Deletethe channel_id from the database
    delete_channel_id(interaction.channel_id)
    await interaction.response.send_message("Bot stopped", ephemeral=True)


@bot.tree.command(name="add", description="Add Twitter user to tracker")
async def add(interaction: discord.Interaction, username: str):
    user = get_user(username)
    if user is None:
        await interaction.response.send_message(f"User {username} doesn't exist", ephemeral=True)
    else:
        await interaction.response.send_message(f"User {username} added", ephemeral=True)
        add_user(username)    # add user to the database


@bot.tree.command(name="remove", description="Remove Twitter user from tracker")
async def remove(interaction: discord.Interaction, username: str):
    # user = get_user(username)
    if check_for_user(username) is None:
        await interaction.response.send_message(f"User {username} not in the database", ephemeral=True)
    else:
        await interaction.response.send_message(f"User {username} removed", ephemeral=True)
        remove_user(username)    # remove user to the database


config_values = read_config()
discord_api_key = config_values['discord']['api_key']

bot.run(discord_api_key)
