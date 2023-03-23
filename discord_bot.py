import asyncio
import discord
from discord.ext import commands
from twitter_functions import get_user, get_new_friends
from db_functions import add_user, remove_user, check_for_user, read_channel_id, write_channel_id, get_tracked_users, update_friends_number, delete_channel_id
from config import read_config


class TwitterTrackerBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tracked_channel_id = None
        self.stop_event = asyncio.Event()

    async def on_ready(self):
        print("Bot is online")
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)

        self.tracked_channel_id = read_channel_id()
        if self.tracked_channel_id is not None:
            self.loop.create_task(self.track_users())

    async def track_users(self):
        while bot.tracked_channel_id is not None:
            tracked_users = get_tracked_users()
            if tracked_users:   # check if the database is not empty
                for user in tracked_users:
                    (username, friends_num) = user
                    (new_friends, diff) = get_new_friends(username, friends_num)
                    if new_friends is not None:
                        update_friends_number(username, diff)

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
                    elif diff < 0:
                        update_friends_number(username, diff)

            await asyncio.sleep(10)

            if self.stop_event.is_set():
                self.stop_event.clear()  # Reset the stop_event for future use
                break


bot = TwitterTrackerBot(command_prefix='!', intents=discord.Intents.all())


@bot.tree.command(name="start", description="Initialize the bot")
async def start(interaction: discord.Interaction):
    bot.tracked_channel_id = interaction.channel_id
    user = str(interaction.user)
    write_channel_id(bot.tracked_channel_id, user)
    await interaction.response.send_message("Bot initiated", ephemeral=True)
    bot.loop.create_task(bot.track_users())


@bot.tree.command(name="stop", description="Stop the bot")
async def stop(interaction: discord.Interaction):
    bot.tracked_channel_id = None
    bot.stop_event.set()  # Signal the track_users loop to stop
    delete_channel_id(interaction.channel_id)
    await interaction.response.send_message("Bot stopped", ephemeral=True)


@bot.tree.command(name="add", description="Add Twitter user to tracker")
async def add(interaction: discord.Interaction, username: str):
    user = get_user(username)
    if user is None:
        await interaction.response.send_message(f"User {username} doesn't exist", ephemeral=True)
    else:
        await interaction.response.send_message(f"User {username} added", ephemeral=True)
        add_user(username)


@bot.tree.command(name="remove", description="Remove Twitter user from tracker")
async def remove(interaction: discord.Interaction, username: str):
    if check_for_user(username) is None:
        await interaction.response.send_message(f"User {username} not in the database", ephemeral=True)
    else:
        await interaction.response.send_message(f"User {username} removed", ephemeral=True)
        remove_user(username)    # remove user to the database

config_values = read_config()
discord_api_key = config_values['discord']['api_key']

bot.run(discord_api_key)
