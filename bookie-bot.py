# import discord
import random
# import discord.ext
# from discord.utils import get
from discord.ext import commands
# from discord.ext.commands import has_permissions, CheckFailure, check
import lines
import match
import ah


# client = discord.Client()

bot = commands.Bot(command_prefix='$')


@bot.event
async def on_ready():
    print('Bitch we ready. {0.user} is here.'.format(bot))


# This code makes Schtick Bot ignore himself
# Processes all commands once match.author has updated
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    name = str(message.author)
    match.author = name.split('#')[0]
    # if match.author != "iWumbo19":
    # return
    await bot.process_commands(message)


# These are the commands that can be called with $<function name>
# Each one begins with checking for $<command> help

# Attempts to create a new event if all arguments pass checks
@bot.command()
async def create(ctx, *args):
    if len(args) == 1:
        if args[0] == "help":
            await ctx.send("$create <red> <blue>")
            return
    if len(args) != 2:
        await ctx.send("It takes two to tango slick")
        return
    red = args[0]
    blue = args[1]
    await ctx.send(f"Match between {red} and {blue} is now open for betting!")
    await ctx.send(lines.open_betting[random.randint(0, len(lines.open_betting) - 1)])
    match.matches.append(match.Match(red, blue, match.author))


# Lists all matches in order to matchId
@bot.command()
async def matches(ctx):
    if len(match.matches) == 0:
        await ctx.send("No matches scheduled I'm afraid. Maybe check back later")
        return
    for item in match.matches:
        await ctx.send(f"Match {item.matchid}:\n"
                       f"Red Corner: {item.redcorner}\n"
                       f"Blue Corner: {item.bluecorner}\n"
                       f"Odds are {item.redodd}:{item.blueodd} for a {item.redpot+item.bluepot} pot\n"
                       f"Created by: {item.creator} (Open Betting = {item.closed})")


# Places bet based on matchId and corner color
@bot.command()
async def bet(ctx, *args):
    if len(args) == 1:
        if args[0] == "help":  # Check for help command
            await ctx.send("$bet <amount> <match id> <red/blue>")
            return
    if len(args) != 3:  # Check to see if proper amount of arguments
        await ctx.send("I need three things from you\n"
                       "$bet <amount> <match id> <red/blue>")
        return
    try:  # Attempt to cast arg 0 and 1 to ints
        amount = int(args[0])
        matchId = int(args[1])
    except:  # Failure to cast arg 0 and 1 to ints
        await ctx.send(f"Couldn't make {args[0]} or {args[1]} into a number")
        return

    if amount < match.lowest_bet:  # Check to see if bet exceeds bottom bet limit
        await ctx.send(f"Are you really that broke {match.author}?")
        return
    if amount > match.max_bet:  # Check to see if bet exceeds max bet limit
        await ctx.send(f"Easy there big spender. Limit is 10000 for now")
        return
    if matchId <= 0 or matchId > len(match.matches):  # Check to make sure matchId is within list limits
        await ctx.send("Match Id not find")
        return

    for item in match.matches:  # Run through list of match objects
        if item.matchid == matchId:  # Find matching ID and update color
            if item.closed:
                await ctx.send("Betting has been closed for this event")
                return
            if args[2] == "blue":  # Need to add update odd function when made
                item.bluepot += amount
                await ctx.send(f"{match.author} puts {amount} on {item.bluecorner}!\n"
                               f"Odds are now {item.redodd}:{item.blueodd}")
                return
            elif args[2] == "red":
                item.redpot += amount
                await ctx.send(f"{match.author} puts {amount} on {item.redcorner}!\n"
                               f"Odds are now {item.redodd}:{item.blueodd}")
                return
            else:
                await ctx.send("Match found but your color is spelt wrong?")
                return


# Attempt to remove match based on author and matchId
@bot.command()
async def remove(ctx, *args):
    if len(args) == 1:
        if args[0] == "help":
            await ctx.send("$remove <matchId>")
            return
    try:
        id = int(args[0])
    except:
        await ctx.send("That aint a number fool")
        return
    if match.matches[id-1].creator != match.author:
        await ctx.send("Only the creator of the event can remove it")
        return
    match.matches.remove(id - 1)
    await ctx.send(f"Match {id} removed")


# Reports current balance based on whom asked
@bot.command()
async def balance(ctx):
    await ctx.send(ah.get_balance())


# Reports current MATCH wins based on whom asked
@bot.command()
async def wins(ctx):
    await ctx.send(ah.get_wins())


# Reports current MATCH losses based on whom asked
@bot.command()
async def losses(ctx):
    await ctx.send(ah.get_losses())


# Attempts to create new account if none is present
@bot.command()
async def noob(ctx):
    await ctx.send(ah.create_account())


# Help command (Need to figure out how to override built-in help function)
@bot.command()
async def helper(ctx):
    await ctx.send("Commands: create, matches, bet, remove, balance, wins, losses, noob\n"
                   "Be sure to use '$' before commands and use '$<command> help' for arguments")


# Method to payout match based on id
@bot.command()
async def payout(ctx, *args):
    if len(args) != 1:
        await ctx.send("Just tell me what match you're trying to close out")
        return

    if args[0] == 'help':
        await ctx.send("$payout <matchid>")
        return

    try:  # Attempt to cast arg 0 to ints
        matchId = int(args[0])
    except:  # Failure to cast arg 0 to ints
        await ctx.send(f"Couldn't make {args[0]} or {args[1]} into a number")
        return

    if match.matches[args[0]].name != match.author:
        await ctx.se("You aren't the one who created the match dumb dumb")
        return

    match.matches[matchId-1].payout_match(ctx, 'red')


# A test command for iWumbo to ensure connection
@bot.command()
async def welcome(ctx):
    if match.author != "iWumbo19":
        return
    await ctx.send("What up bitches! Time to lose your shirts")


if __name__ == '__main__':
    import config

    bot.run(config.token)
