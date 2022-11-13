import discord


def invalid_channel():
    return discord.Embed(title="Invalid Channel", description="To ensure privacy, please use this command in direct messages only.", color=discord.Color.red())


def invalid_region():
    embed = discord.Embed(title="Invalid Region Provided", description="Please use one of the following regions", color=discord.Color.red())
    embed.add_field(name="ap", value="Asia Pacific", inline=False)
    embed.add_field(name="eu", value="Europe", inline=False)
    embed.add_field(name="kr", value="Korea", inline=False)
    embed.add_field(name="na", value="North America, Brazil, and PBE", inline=False)
    return embed


def user_already_exists(username):
    return discord.Embed(title="User Already Exists", description=f"\"{username}\" is already in the database.\nIf you want to update your password, use /setpassword.", color=discord.Color.red())


def user_does_not_exist(username):
    return discord.Embed(title="User Does Not Exist", description=f"\"{username}\" is not in the database.\nIf you want to add this user, use /adduser", color=discord.Color.red())


def user_added(username):
    return discord.Embed(title="User Added", description=f"\"{username}\" has been added to the database.", color=discord.Color.green())


def user_deleted(username):
    return discord.Embed(title="User Deleted", description=f"\"{username}\" has been deleted from the database.", color=discord.Color.green())


def user_updated(username):
    return discord.Embed(title="User Credentials Updated", description=f"The credentials of \"{username}\" have been updated to the database.", color=discord.Color.green())


def authentication_error():
    return discord.Embed(title="Authentication Error", description="Make sure your username and password are correct and try again.", color=discord.Color.red())


def rate_limit_error():
    return discord.Embed(title="Rate Limited", description="Your request has been rate limited by riot.\nPlease try again in a couple minutes.", color=discord.Color.red())


def multifactor_error():
    return discord.Embed(title="Multifactor Unsupported", description="Your account has 2FA enabled.\nPlease disable 2FA and try again", color=discord.Color.red())


def unknown_error():
    return discord.Embed(title="An Error Occurred", description="An unknown error occurred. This issue has been raised and will be fixed as soon as possible.", color=discord.Color.dark_red())


def help_command():
    embed = discord.Embed(title="Valemporium - Help", description="All available commands", color=discord.Color.blue())
    embed.add_field(name="/store", value="Retrieve the store of a player", inline=False)
    embed.add_field(name="/balance", value="Retrieves the balance of your Valorant account", inline=False)
    embed.add_field(name="/adduser", value="Saves login credentials to the database (ONLY use this command in DMs)", inline=False)
    embed.add_field(name="/deluser", value="Deletes login credentials from the database", inline=False)
    embed.add_field(name="/setpassword", value="Edits the password of the user in the database (ONLY use this command in DMs)", inline=False)
    embed.add_field(name="/about", value="About Valemporium", inline=False)
    embed.add_field(name="⠀", value="Enter your riot username, not your Valorant display name\nOnly enter passwords in direct messages with the bot", inline=False)
    return embed


def about_command():
    embed = discord.Embed(title="Valemporium - About", description="About Valemporium", color=discord.Color.blue())
    embed.add_field(name="Developer", value="Bot created and coded by Pure#0004", inline=False)
    embed.add_field(name="Security and Privacy", value="All passwords and credentials are encrypted with Fernet and stored in a secure database.", inline=False)
    embed.add_field(name="Source", value="This project is open source and can be viewed on Github.", inline=False)
    embed.add_field(name="Built with", value="This project is heavy based on Valorina, Python, PyMongo.", inline=False)
    embed.add_field(name="License", value="Distributed under the MIT License. Copyright (c) 2022 Phineas Ou", inline=False)
    embed.add_field(name="Legal", value="For any riot employees, please contact Pure#0004 regarding this bot before taking any actions on our players and users.\n\nValemporium is not endorsed by Riot Games and the developer is not liable for any damage, bans, or loss of account caused by this bot.\nRiot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.", inline=False)
    return embed
