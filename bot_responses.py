import discord


# ------- Argument Error Responses -------

def invalid_channel():
    return discord.Embed(title="Invalid Channel", description="To ensure privacy, please use this command in direct messages only.", color=discord.Color.red())


def invalid_region():
    embed = discord.Embed(title="Invalid Region Provided", description="Please use one of the following regions", color=discord.Color.red())
    embed.add_field(name="ap", value="Asia Pacific", inline=False)
    embed.add_field(name="eu", value="Europe", inline=False)
    embed.add_field(name="kr", value="Korea", inline=False)
    embed.add_field(name="na", value="North America, Brazil, and PBE", inline=False)
    return embed


# ------- Database Responses -------

def user_already_exists(username):
    return discord.Embed(title="User Already Exists", description=f"\"{username}\" is already in the database.\nIf you want to update your password, use /setpassword.", color=discord.Color.red())


def user_does_not_exist(username):
    return discord.Embed(title="User Does Not Exist", description=f"\"{username}\" is not in the database.\nIf you want to add this user, use /adduser in DMs.", color=discord.Color.red())


def user_added(username):
    return discord.Embed(title="User Added", description=f"\"{username}\" has been added to the database.", color=discord.Color.green())


def user_deleted(username):
    return discord.Embed(title="User Deleted", description=f"\"{username}\" has been deleted from the database.", color=discord.Color.green())


def user_updated(username):
    return discord.Embed(title="User Credentials Updated", description=f"The credentials of \"{username}\" have been updated to the database.", color=discord.Color.green())


# ------- Riot Authentication Errors/Responses -------

def authentication_error():
    return discord.Embed(title="Authentication Error", description="Make sure your username and password are correct and try again.\nEnsure you are using your riot account sign-in and not your Valorant display name.\nIf you have updated your password, please use /setpassword <username> <password> <region> in DMs.", color=discord.Color.red())


def rate_limit_error():
    return discord.Embed(title="Rate Limited", description="Your request has been rate limited by riot.\nPlease try again in a couple minutes.", color=discord.Color.red())


def multifactor_detected():
    return discord.Embed(title="Enter 2FA Code", description="Your account has 2FA enabled.\nCheck your emails and use the command: /store <username> <region> <multifactor_code>.\n\nNote that you will need enter a new multifactor code every time you check your store.\nAlternatively, you can disable 2FA at [Riot Account Management](https://account.riotgames.com/)", color=discord.Color.red())


def multifactor_error():
    return discord.Embed(title="Multifactor Failed", description="The 2FA code you entered was incorrect.\nPlease confirm your code or request a new code with the command: /store <username> <region>.\n\nNote that you will need enter a new multifactor code every time you check your store.\nAlternatively, you can disable 2FA at [Riot Account Management](https://account.riotgames.com/)", color=discord.Color.red())


# ------- Discord Bot Setup Error Responses -------

def permission_error():
    return discord.Embed(title="Permission Error (403 Forbidden)", description="Permissions in this server channel do not allow messages to be sent.\nA server admin will need to allow message sending for Valemporium in channel permission settings.", color=discord.Color.dark_red())


# ------- Unknown Error (Unhandled exception) -------

def unknown_error():
    return discord.Embed(title="An Error Occurred", description="An unknown error occurred. This issue has been raised and will be fixed as soon as possible.\nIf this issue persists, please submit a request in the [Valemporium support server](https://discord.gg/ejvddZr4Dw)", color=discord.Color.dark_red())


# ------- Informational Responses -------

def help_command():
    embed = discord.Embed(title="Valemporium - Help", description="All available commands and important command arguments", color=discord.Color.blue())
    embed.add_field(name="/store", value="Retrieves the store of a player", inline=False)
    embed.add_field(name="/accessorystore", value="Retrieves the accessory store of a player", inline=False)
    embed.add_field(name="/balance", value="Retrieves the balance of your Valorant account", inline=False)
    embed.add_field(name="/adduser", value="Saves login credentials to the database (ONLY use this command in DMs)", inline=False)
    embed.add_field(name="/deluser", value="Deletes login credentials from the database (ONLY use this command in DMs)", inline=False)
    embed.add_field(name="/setpassword", value="Edits the password of the user in the database (ONLY use this command in DMs)", inline=False)
    embed.add_field(name="/about", value="About Valemporium", inline=False)
    embed.add_field(name="Region Selection", value="ap - Asia/Pacific\neu - Europe\nkr - Korea\nna - North America, Brazil, and PBE", inline=False)
    embed.add_field(name="Support Server", value="For Discord support, join the [Valemporium support server](https://discord.gg/ejvddZr4Dw)", inline=False)
    embed.add_field(name="⠀", value="Enter your riot username, not your Valorant display name\nOnly enter passwords in direct messages with the bot", inline=False)
    return embed


def about_command():
    embed = discord.Embed(title="Valemporium - About", description="About Valemporium", color=discord.Color.blue())
    embed.add_field(name="Developer", value="Bot created and coded by Pure#2254", inline=False)
    embed.add_field(name="Privacy and Security", value="All passwords and credentials are encrypted with Fernet and stored in a secure database.", inline=False)
    embed.add_field(name="Source", value="This project is open source and can be viewed on [Github](https://github.com/PureAspiration/Valemporium).", inline=False)
    embed.add_field(name="Built with", value="This project is heavy based on [Valorina](https://github.com/sanjaybaskaran01/Valorina), [python-riot-auth](https://github.com/floxay/python-riot-auth), PyMongo.", inline=False)
    embed.add_field(name="License", value="Distributed under the MIT License. Copyright (c) 2022 PureAspiration", inline=False)
    embed.add_field(name="Legal", value="For any riot employees, please contact Pure#2254 regarding this bot before taking any actions on our players and users.\n\nValemporium is not endorsed by Riot Games and the developer is not liable for any damage, bans, or loss of account caused by this bot.\nRiot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.", inline=False)
    return embed
