import os
import time
import traceback
from typing import Literal

import discord
from discord import app_commands
from dotenv import load_dotenv

import bot_responses
import database
import get_store
import riot_authorization

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


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


client = Bot()
tree = app_commands.CommandTree(client)


@tree.command(name="store", description="Retrieve the store of a player")
async def self(interaction: discord.Interaction, username: str, region: Literal["ap", "eu", "kr", "na"]):
    print(f"/store command ran by {interaction.user}")
    await interaction.response.defer()
    # Valid region check
    region = region.lower()
    if region not in ["ap", "eu", "kr", "na"]:
        await interaction.followup.send(embed=bot_responses.invalid_region())
        return
    # User does not exist check
    if not database.check_user_existence(username, region):
        await interaction.followup.send(embed=bot_responses.user_does_not_exist(username))
        return
    # Get user credentials
    credentials = database.get_user(username, region)
    # Database fetch failed check
    if not credentials:
        await interaction.followup.send(embed=bot_responses.user_does_not_exist(username))
        return
    # Authorize riot account
    password = credentials["password"]
    try:
        auth = riot_authorization.RiotAuth()
        await auth.authorize(username, password)
    except riot_authorization.Exceptions.RiotAuthenticationError:
        await interaction.followup.send(embed=bot_responses.authentication_error())
        return
    except riot_authorization.Exceptions.RiotRatelimitError:
        await interaction.followup.send(embed=bot_responses.rate_limit_error())
        return
    except riot_authorization.Exceptions.RiotMultifactorError:
        await interaction.followup.send(embed=bot_responses.multifactor_error())
        return
    except Exception as exception:
        await interaction.followup.send(embed=bot_responses.unknown_error())
        print(f"Unknown exception occurred: {str(exception)}")
        traceback.print_exc()
        return
    # Get store
    try:
        # noinspection SpellCheckingInspection
        headers = {
            "Authorization": f'Bearer {auth.access_token}',
            "User-Agent": username,
            "X-Riot-Entitlements-JWT": auth.entitlements_token,
            "X-Riot-ClientPlatform": "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9",
            "X-Riot-ClientVersion": "pbe-shipping-55-604424"
        }
        store = get_store.getStore(headers, auth.user_id, region)
        embed = discord.Embed(title="Offer ends in", description=store[1], color=discord.Color.gold())
        await interaction.followup.send(embed=embed)
        for item in store[0]:
            embed = discord.Embed(title=item[0], description=f"Cost: {item[1]} Valorant Points", color=discord.Color.gold())
            embed.set_thumbnail(url=item[2])
            await interaction.channel.send(embed=embed)
        return
    except Exception as exception:
        await interaction.followup.send(embed=bot_responses.unknown_error())
        print(f"Unknown exception occurred: {str(exception)}")
        traceback.print_exc()
        return


@tree.command(name="balance", description="Retrieves the balance of your Valorant account")
async def self(interaction: discord.Interaction, username: str, region: Literal["ap", "eu", "kr", "na"]):
    print(f"/balance command ran by {interaction.user}")
    await interaction.response.defer()
    # Valid region check
    region = region.lower()
    if region not in ["ap", "eu", "kr", "na"]:
        await interaction.followup.send(embed=bot_responses.invalid_region())
        return
    # User does not exist check
    if not database.check_user_existence(username, region):
        await interaction.followup.send(embed=bot_responses.user_does_not_exist(username))
        return
    # Get user credentials
    credentials = database.get_user(username, region)
    # Database fetch failed check
    if not credentials:
        await interaction.followup.send(embed=bot_responses.user_does_not_exist(username))
        return
    # Authorize riot account
    password = credentials["password"]
    try:
        auth = riot_authorization.RiotAuth()
        await auth.authorize(username, password)
    except riot_authorization.Exceptions.RiotAuthenticationError:
        await interaction.followup.send(embed=bot_responses.authentication_error())
        return
    except riot_authorization.Exceptions.RiotRatelimitError:
        await interaction.followup.send(embed=bot_responses.rate_limit_error())
        return
    except riot_authorization.Exceptions.RiotMultifactorError:
        await interaction.followup.send(embed=bot_responses.multifactor_error())
        return
    except Exception as exception:
        await interaction.followup.send(embed=bot_responses.unknown_error())
        print(f"Unknown exception occurred: {str(exception)}")
        traceback.print_exc()
        return
    # Get balance
    try:
        # noinspection SpellCheckingInspection
        headers = {
            "Authorization": f'Bearer {auth.access_token}',
            "User-Agent": username,
            "X-Riot-Entitlements-JWT": auth.entitlements_token,
            "X-Riot-ClientPlatform": "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9",
            "X-Riot-ClientVersion": "pbe-shipping-55-604424"
        }
        vp, rp = await get_store.get_balance(headers, auth.user_id, region)
        embed = discord.Embed(title="Balance", description=f"Valorant Points: {vp}\nRadianite Points: {rp}", color=discord.Color.gold())
        await interaction.followup.send(embed=embed)
        return
    except Exception as exception:
        await interaction.followup.send(embed=bot_responses.unknown_error())
        print(f"Unknown exception occurred: {str(exception)}")
        traceback.print_exc()
        return


@tree.command(name="adduser", description="Saves login credentials to the database (ONLY use this command in DMs)")
async def self(interaction: discord.Interaction, username: str, password: str, region: Literal["ap", "eu", "kr", "na"]):
    print(f"/adduser command ran by {interaction.user}")
    await interaction.response.defer()
    # Private DM check
    if interaction.channel.type != discord.ChannelType.private:
        await interaction.followup.send(embed=bot_responses.invalid_channel(), ephemeral=True)
        return
    # Valid region check
    region = region.lower()
    if region not in ["ap", "eu", "kr", "na"]:
        await interaction.followup.send(embed=bot_responses.invalid_region())
        return
    # User already exists check
    if database.check_user_existence(username, region):
        await interaction.followup.send(embed=bot_responses.user_already_exists(username))
        return
    # Valid login credentials check
    try:
        auth = riot_authorization.RiotAuth()
        await auth.authorize(username, password)
    except riot_authorization.Exceptions.RiotAuthenticationError:
        await interaction.followup.send(embed=bot_responses.authentication_error())
        return
    except riot_authorization.Exceptions.RiotRatelimitError:
        await interaction.followup.send(embed=bot_responses.rate_limit_error())
        return
    except riot_authorization.Exceptions.RiotMultifactorError:
        pass
    except Exception as exception:
        await interaction.followup.send(embed=bot_responses.unknown_error())
        print(f"Unknown exception occurred: {str(exception)}")
        traceback.print_exc()
        return
    # Add to database
    print("Adding account details to database...")
    database.add_user(username, password, region)
    await interaction.followup.send(embed=bot_responses.user_added(username))
    return


@tree.command(name="deluser", description="Deletes login credentials from the database")
async def self(interaction: discord.Interaction, username: str, region: Literal["ap", "eu", "kr", "na"]):
    print(f"/deluser command ran by {interaction.user}")
    await interaction.response.defer()
    # Valid region check
    region = region.lower()
    if region not in ["ap", "eu", "kr", "na"]:
        await interaction.followup.send(embed=bot_responses.invalid_region())
        return
    # User does not exist check
    if not database.check_user_existence(username, region):
        await interaction.followup.send(embed=bot_responses.user_does_not_exist(username))
        return
    # Delete from database
    print("Deleting account details from database...")
    database.delete_user(username, region)
    await interaction.followup.send(embed=bot_responses.user_deleted(username))
    return


@tree.command(name="setpassword", description="Edits the password of the user in the database (ONLY use this command in DMs)")
async def self(interaction: discord.Interaction, username: str, password: str, region: Literal["ap", "eu", "kr", "na"]):
    print(f"/setpassword command ran by {interaction.user}")
    await interaction.response.defer()
    # Private DM check
    if interaction.channel.type != discord.ChannelType.private:
        await interaction.followup.send(embed=bot_responses.invalid_channel(), ephemeral=True)
        return
    # Valid region check
    region = region.lower()
    if region not in ["ap", "eu", "kr", "na"]:
        await interaction.followup.send(embed=bot_responses.invalid_region())
        return
    # User does not exist check
    if not database.check_user_existence(username, region):
        await interaction.followup.send(embed=bot_responses.user_does_not_exist(username))
        return
    # Valid login credentials check
    try:
        auth = riot_authorization.RiotAuth()
        await auth.authorize(username, password)
    except riot_authorization.Exceptions.RiotAuthenticationError:
        await interaction.followup.send(embed=bot_responses.authentication_error())
        return
    except riot_authorization.Exceptions.RiotRatelimitError:
        await interaction.followup.send(embed=bot_responses.rate_limit_error())
        return
    except riot_authorization.Exceptions.RiotMultifactorError:
        pass
    except Exception as exception:
        await interaction.followup.send(embed=bot_responses.unknown_error())
        print(f"Unknown exception occurred: {str(exception)}")
        traceback.print_exc()
        return
    # Update password
    print("Updating account details to database...")
    database.update_password(username, password, region)
    await interaction.followup.send(embed=bot_responses.user_updated(username))
    return


@tree.command(name="help", description="Lists all available commands and details")
async def self(interaction: discord.Interaction):
    print(f"/help command ran by {interaction.user}")
    await interaction.response.send_message(embed=bot_responses.help_command())


@tree.command(name="info", description="About Valemporium")
async def self(interaction: discord.Interaction):
    print(f"/info command ran by {interaction.user}")
    await interaction.response.send_message(embed=bot_responses.about_command())


@tree.command(name="about", description="About Valemporium")
async def self(interaction: discord.Interaction):
    print(f"/about command ran by {interaction.user}")
    await interaction.response.send_message(embed=bot_responses.about_command())


client.run(BOT_TOKEN)
