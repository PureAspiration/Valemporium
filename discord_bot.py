import asyncio
import datetime
import os
import time
import traceback
from typing import Literal, Optional

import discord
from discord import app_commands
from dotenv import load_dotenv

import bot_responses
import database
import get_store
import riot_authorization
from keep_alive import keep_alive

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


def separator():
    print(f"\n==========[@ {datetime.datetime.fromtimestamp(time.time()).strftime('%d/%m/%Y %H:%M:%S')}]==========")


class Bot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        print("Starting command sync...")
        sync_start_time = time.time()
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"Sync completed in {round(time.time() - sync_start_time, 2)} seconds")
        print(f"Bot started and logged in as {self.user}")
        self.loop.create_task(loop_task())


client = Bot()
tree = app_commands.CommandTree(client)


@tree.command(name="store", description="Retrieve the store of a player")
async def self(interaction: discord.Interaction, username: str, region: Literal["ap", "eu", "kr", "na", "help"], multifactor_code: Optional[str] = None):
    try:
        separator()
        print(f"/store command ran by {interaction.user}")
        # Valid region check
        region = region.lower()
        if region not in ["ap", "eu", "kr", "na"]:
            await interaction.response.send_message(embed=bot_responses.invalid_region())
            print("Invalid region")
            return
        # User does not exist check
        if not database.check_user_existence(username, region):
            await interaction.response.send_message(embed=bot_responses.user_does_not_exist(username))
            print("User does not exist")
            return
        # Get user credentials
        credentials = database.get_user(username, region)
        # Database fetch failed check
        if not credentials:
            await interaction.response.send_message(embed=bot_responses.user_does_not_exist(username))
            print("User does not exist")
            return
        # Start response defer
        await interaction.response.defer()
        # Authorize riot account
        password = credentials['password']
        auth = riot_authorization.RiotAuth()
        try:
            await auth.authorize(username, password, multifactor_code=multifactor_code)
        except riot_authorization.Exceptions.RiotAuthenticationError:
            await interaction.followup.send(embed=bot_responses.authentication_error())
            print("Authentication error")
            return
        except riot_authorization.Exceptions.RiotRatelimitError:
            await interaction.followup.send(embed=bot_responses.rate_limit_error())
            print("Rate limited")
            return
        except riot_authorization.Exceptions.RiotMultifactorError:
            # No multifactor provided check
            if multifactor_code is None:
                await interaction.followup.send(embed=bot_responses.multifactor_detected())
                print("Multifactor detected")
                return
            await interaction.followup.send(embed=bot_responses.multifactor_error())
            print("Multifactor authentication error")
            return
        # All other exceptions will be handled by global

        # Get store
        # noinspection SpellCheckingInspection
        headers = {
            "Authorization": f"Bearer {auth.access_token}",
            "User-Agent": username,
            "X-Riot-Entitlements-JWT": auth.entitlements_token,
            "X-Riot-ClientPlatform": "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9",
            "X-Riot-ClientVersion": "pbe-shipping-55-604424"
        }
        store = get_store.getStore(headers, auth.user_id, region)
        try:
            for item in store[0]:
                embed = discord.Embed(title=item[0], description=f"Cost: {item[1]} Valorant Points", color=discord.Color.gold())
                embed.set_thumbnail(url=item[2])
                await interaction.channel.send(embed=embed)
        except discord.errors.Forbidden:
            await interaction.followup.send(embed=bot_responses.permission_error())
        else:
            embed = discord.Embed(title="Offer ends in", description=store[1], color=discord.Color.gold())
            await interaction.followup.send(embed=embed)
        print("Store fetch successful")
        return

    except Exception as exception:
        print(f"Unknown exception occurred: {str(exception)}")
        traceback.print_exc()
        await unknown_exception(interaction)
        return


@tree.command(name="balance", description="Retrieves the balance of your Valorant account")
async def self(interaction: discord.Interaction, username: str, region: Literal["ap", "eu", "kr", "na", "help"], multifactor_code: Optional[str] = None):
    try:
        separator()
        print(f"/balance command ran by {interaction.user}")
        # Valid region check
        region = region.lower()
        if region not in ["ap", "eu", "kr", "na"]:
            await interaction.response.send_message(embed=bot_responses.invalid_region())
            print("Invalid region")
            return
        # User does not exist check
        if not database.check_user_existence(username, region):
            await interaction.response.send_message(embed=bot_responses.user_does_not_exist(username))
            print("User does not exist")
            return
        # Get user credentials
        credentials = database.get_user(username, region)
        # Database fetch failed check
        if not credentials:
            await interaction.response.send_message(embed=bot_responses.user_does_not_exist(username))
            print("User does not exist")
            return
        # Start response defer
        await interaction.response.defer()
        # Authorize riot account
        password = credentials['password']
        try:
            auth = riot_authorization.RiotAuth()
            await auth.authorize(username, password)
        except riot_authorization.Exceptions.RiotAuthenticationError:
            await interaction.followup.send(embed=bot_responses.authentication_error())
            print("Authentication error")
            return
        except riot_authorization.Exceptions.RiotRatelimitError:
            await interaction.followup.send(embed=bot_responses.rate_limit_error())
            print("Rate limited")
            return
        except riot_authorization.Exceptions.RiotMultifactorError:
            # No multifactor provided check
            if multifactor_code is None:
                await interaction.followup.send(embed=bot_responses.multifactor_detected())
                print("Multifactor detected")
                return
            await interaction.followup.send(embed=bot_responses.multifactor_error())
            print("Multifactor authentication error")
            return
        # All other exceptions will be handled by global
        # Get balance
        # noinspection SpellCheckingInspection
        headers = {
            "Authorization": f"Bearer {auth.access_token}",
            "User-Agent": username,
            "X-Riot-Entitlements-JWT": auth.entitlements_token,
            "X-Riot-ClientPlatform": "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9",
            "X-Riot-ClientVersion": "pbe-shipping-55-604424"
        }
        vp, rp = await get_store.get_balance(headers, auth.user_id, region)
        embed = discord.Embed(title="Balance", description=f"Valorant Points: {vp}\nRadianite Points: {rp}", color=discord.Color.gold())
        await interaction.followup.send(embed=embed)
        print("Balance fetch successful")
        return

    except Exception as exception:
        print(f"Unknown exception occurred: {str(exception)}")
        traceback.print_exc()
        await unknown_exception(interaction)
        return


@tree.command(name="adduser", description="Saves login credentials to the database (ONLY use this command in DMs)")
async def self(interaction: discord.Interaction, username: str, password: str, region: Literal["ap", "eu", "kr", "na", "help"]):
    try:
        separator()
        print(f"/adduser command ran by {interaction.user}")
        # Private DM check
        if interaction.channel.type != discord.ChannelType.private:
            await interaction.response.send_message(embed=bot_responses.invalid_channel(), ephemeral=True)
            print("Invalid channel")
            return
        # Valid region check
        region = region.lower()
        if region not in ["ap", "eu", "kr", "na"]:
            await interaction.response.send_message(embed=bot_responses.invalid_region())
            print("Invalid region")
            return
        # User already exists check
        if database.check_user_existence(username, region):
            await interaction.response.send_message(embed=bot_responses.user_already_exists(username))
            print("User already exists")
            return
        # Start response defer
        await interaction.response.defer()
        # Valid login credentials check
        try:
            auth = riot_authorization.RiotAuth()
            await auth.authorize(username, password)
        except riot_authorization.Exceptions.RiotAuthenticationError:
            await interaction.followup.send(embed=bot_responses.authentication_error())
            print("Authentication error")
            return
        except riot_authorization.Exceptions.RiotRatelimitError:
            await interaction.followup.send(embed=bot_responses.rate_limit_error())
            print("Rate limited")
            return
        except riot_authorization.Exceptions.RiotMultifactorError:
            pass
        # All other exceptions will be handled by global
        # Add to database
        print("Adding account details to database...")
        database.add_user(username, password, region)
        await interaction.followup.send(embed=bot_responses.user_added(username))
        print("Added account details to database")
        return

    except Exception as exception:
        print(f"Unknown exception occurred: {str(exception)}")
        traceback.print_exc()
        await unknown_exception(interaction)
        return


@tree.command(name="deluser", description="Deletes login credentials from the database (ONLY use this command in DMs)")
async def self(interaction: discord.Interaction, username: str, region: Literal["ap", "eu", "kr", "na", "help"]):
    try:
        separator()
        print(f"/deluser command ran by {interaction.user}")
        # Private DM check
        if interaction.channel.type != discord.ChannelType.private:
            await interaction.response.send_message(embed=bot_responses.invalid_channel(), ephemeral=True)
            print("Invalid channel")
            return
        # Valid region check
        region = region.lower()
        if region not in ["ap", "eu", "kr", "na"]:
            await interaction.response.send_message(embed=bot_responses.invalid_region())
            print("Invalid region")
            return
        # User does not exist check
        if not database.check_user_existence(username, region):
            await interaction.response.send_message(embed=bot_responses.user_does_not_exist(username))
            print("User does not exist")
            return
        # Delete from database
        print("Deleting account details from database...")
        database.delete_user(username, region)
        await interaction.response.send_message(embed=bot_responses.user_deleted(username))
        print("Deleted account details from database")
        return

    except Exception as exception:
        print(f"Unknown exception occurred: {str(exception)}")
        traceback.print_exc()
        await unknown_exception(interaction)
        return


@tree.command(name="setpassword", description="Edits the password of the user in the database (ONLY use this command in DMs)")
async def self(interaction: discord.Interaction, username: str, password: str, region: Literal["ap", "eu", "kr", "na", "help"]):
    try:
        separator()
        print(f"/setpassword command ran by {interaction.user}")
        # Private DM check
        if interaction.channel.type != discord.ChannelType.private:
            await interaction.response.send_message(embed=bot_responses.invalid_channel(), ephemeral=True)
            print("Invalid channel")
            return
        # Valid region check
        region = region.lower()
        if region not in ["ap", "eu", "kr", "na"]:
            await interaction.response.send_message(embed=bot_responses.invalid_region())
            print("Invalid region")
            return
        # User does not exist check
        if not database.check_user_existence(username, region):
            await interaction.response.send_message(embed=bot_responses.user_does_not_exist(username))
            print("User does not exist")
            return
        # Start response defer
        await interaction.response.defer()
        # Valid login credentials check
        try:
            auth = riot_authorization.RiotAuth()
            await auth.authorize(username, password)
        except riot_authorization.Exceptions.RiotAuthenticationError:
            await interaction.followup.send(embed=bot_responses.authentication_error())
            print("Authentication error")
            return
        except riot_authorization.Exceptions.RiotRatelimitError:
            await interaction.followup.send(embed=bot_responses.rate_limit_error())
            print("Rate limited")
            return
        except riot_authorization.Exceptions.RiotMultifactorError:
            pass
        # All other exceptions will be handled by global
        # Update password
        print("Updating account details to database...")
        database.update_password(username, password, region)
        await interaction.followup.send(embed=bot_responses.user_updated(username))
        print("Updated account details to database")
        return

    except Exception as exception:
        print(f"Unknown exception occurred: {str(exception)}")
        traceback.print_exc()
        await unknown_exception(interaction)
        return


@tree.command(name="help", description="Lists all available commands and details")
async def self(interaction: discord.Interaction):
    separator()
    print(f"/help command ran by {interaction.user}")
    await interaction.response.send_message(embed=bot_responses.help_command())


@tree.command(name="info", description="About Valemporium")
async def self(interaction: discord.Interaction):
    separator()
    print(f"/info command ran by {interaction.user}")
    await interaction.response.send_message(embed=bot_responses.about_command())


@tree.command(name="about", description="About Valemporium")
async def self(interaction: discord.Interaction):
    separator()
    print(f"/about command ran by {interaction.user}")
    await interaction.response.send_message(embed=bot_responses.about_command())


async def unknown_exception(interaction: discord.Interaction):
    try:
        await interaction.response.send_message(embed=bot_responses.unknown_error())
        print("Unknown error raised and sent with response.send_message")
    except discord.errors.InteractionResponded:
        print("Response could not be sent as interaction has been deferred. Attempting with followup...")
        try:
            await interaction.followup.send(embed=bot_responses.unknown_error())
            print("Unknown error raised and sent with followup.send")
        except Exception as exception:
            try:
                # Use channel.send if response.send_message and followup.send cannot be used
                print(f"Follow up could not be sent: {type(exception).__name__} {exception}")
                print("Force sending to channel")
                await interaction.channel.send(embed=bot_responses.unknown_error())
                print("Unknown error raised and sent with channel.send")
            except discord.errors.Forbidden:
                print("Unknown error raised but could not be sent with response.send_message/followup.send/channel.send")


# Update status every 30 seconds to keep alive
async def loop_task():
    while True:
        await client.change_presence(activity=discord.Game(""))
        await asyncio.sleep(30)

keep_alive()

while True:
    try:
        client.run(BOT_TOKEN)
    except discord.errors.HTTPException as exception:  # Too many requests sent, cloudflare blocks request
        print(f"HTTPException: {exception}")
        traceback.print_exc()
        print("Attempting to reset ip...")
        os.system("kill 1")
