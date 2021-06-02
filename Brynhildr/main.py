import asyncio
import discord
import dateparser
import datetime
import os
import pytz
import re
import requests
from bs4 import BeautifulSoup
from character import characterparse
from event import eventparse
from summon import summonparse
from weapon import weaponparse

client = discord.Client()

ERRORMESSAGE = "<:despair:376080252754984960> Sorry, I couldn't understand th" \
               "at. Could you try again?"
MENTIONS = ("hey bryn", "hey brynhildr", "hey brynhild", "hi bryn",
            "hi brynhildr", "hi brynhild", "okay bryn", "okay brynhildr",
            "okay brynhild")
VERSION = "v1.4"
AVATAR = "https://cdn.discordapp.com/avatars/729790460175843368/b1b7f6ac0220d" \
         "63a6ad934c9950d698d.png"

CLOCK = "\U0001F551"
QUESTION_MARK = "\U00002753"
CHECK_MARK = "\U00002714"
ERROR = "\U0000274C"
ONE = "\U00000031\U0000FE0F\U000020E3"
TWO = "\U00000032\U0000FE0F\U000020E3"
REACTIONS = ["\U00000031\U0000FE0F\U000020E3", "\U00000032\U0000FE0F\U000020E3",
             "\U00000033\U0000FE0F\U000020E3", "\U00000034\U0000FE0F\U000020E3",
             "\U00000035\U0000FE0F\U000020E3"]


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))
    # activity = discord.Game(name='on the beach')
    activity = discord.Activity(name='the stars',
                                type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if re.search("s\[(.+)]", message.content):
        await lookup(re.search("s\[(.+)]", message.content).group(1), message,
                     True, True)
    elif re.search("\[(.+)]", message.content):
        await lookup(re.search("\[(.+)]", message.content).group(1), message,
                     False, True)
    if message.content.lower().startswith(MENTIONS) or client.user in \
            message.mentions:
        if "updateannounce" in message.content.lower():
            await updateannounce(message)
        elif "remind me" in message.content.lower():
            await reminder(message.content.lower(), message)
        elif "remindme" in message.content.lower():
            await reminderstripped(message.content.lower(), message)
        elif "lookupsimple" in message.content.lower():
            await lookup(message.content, message, True, False)
        elif "lookup" in message.content.lower():
            await lookup(message.content, message, False, False)
        elif "wikihelp" in message.content.lower():
            await wikihelp(message)
        elif "help" in message.content.lower():
            await manual(message)
        elif "discord" in message.content.lower():
            await discordinvite(message)
        elif "changelog" in message.content.lower():
            await changelog(message)
        elif "zeta" in message.content.lower():
            await zeta(message)
        elif "botstats" in message.content.lower():
            await botstats(message)
    elif message.content.lower() == "bad bot":
        await message.channel.send("Bad human")
    elif message.content.lower() == "good bot":
        await message.channel.send("Good human")


async def changelog(message) -> None:
    """
    Change log. Manually typed because file I/O is effort.
    """
    await message.channel.trigger_typing()
    await message.add_reaction(CLOCK)
    embed = discord.Embed()
    embed.title = "Change Log"
    embed.add_field(name="v1.3.1", value="- Fixed display error with character "
                    "charge attacks that get an upgrade but keep the same name"
                    "\n- Fixed reactions applying the react action to all "
                    "recent messages\n- Fixed search menus sometimes displaying"
                    " more reaction options than search results found\n- "
                    "Refined search functionality to only return pages "
                    "supported by lookup\n- Fixed an edge case where looking up"
                    " pages with no description (commonly newly added pages) "
                    "would break lookup\n- Changed bot to summer mode\n- More "
                    "icons added", inline=False)
    embed.add_field(name="v1.3.2", value="- Reconfigured summon calls to "
                    "prevent text fields exceeding the maximum length allowed "
                    "by Discord with certain summons (Freyr)\n- More icons "
                    "added", inline=False)
    embed.add_field(name="v1.3.3", value="- Fixed issue causing lookup of Proto"
                    " Bahamut to fail\n- Minor error message changes\n- Changed"
                    " bot out of summer mode",
                    inline=False)
    embed.add_field(name="v1.3.4", value="- Added new icons for character "
                    "categories\n- Minor regex improvements\n- More icons "
                    "added", inline=False)
    embed.add_field(name="v1.3.5", value="- Internal code refactoring, "
                    "shouldn't impact functionality but makes the code way less"
                    " ugly",
                    inline=False)
    embed.add_field(name="1.4", value="- Added support for characters with "
                    " multiple skill tables\n- Fixed new Evoker EMPs breaking "
                    "lookup\n- More icons added")
    embed.set_footer(icon_url=AVATAR, text="Brynhildr " + VERSION +
                                           " • Made with ♥ by vicyush#4018")
    embed.timestamp = datetime.datetime.utcnow()
    await embedsend(message, embed)


async def updateannounce(message) -> None:
    if str(message.author.id) == os.environ.get("DEV1") or \
            str(message.author.id) == os.environ.get("DEV2"):
        owners = []
        update = message.content[message.content.find("announce") + 8:]
        for server in client.guilds:
            if server.owner not in owners:
                owners.append(server.owner)
        embed = discord.Embed()
        embed.title = "Brynhildr Bot has been updated"
        embed.set_footer(icon_url=AVATAR, text="Brynhildr " + VERSION +
                                               " • Made with ♥ by vicyush#4018")
        embed.description = "Brynhildr Bot has been updated to " + VERSION + \
                            ". No work is needed on your part, this is just a" \
                            " notification. Version " + VERSION + " brings " \
                            "the following changes:\n\n" + update + "\n\n" + \
                            "Thank you for using Brynhildr Bot.\n[Support " \
                            "server](https://discord.gg/3uRTuMU)"
        embed.timestamp = datetime.datetime.utcnow()
        for owner in owners:
            await owner.send(embed=embed)


async def manual(message) -> None:
    """
    Help page. That's really it.
    """
    await message.channel.trigger_typing()
    await message.add_reaction(CLOCK)
    embed = discord.Embed()
    embed.set_footer(icon_url=AVATAR, text="Brynhildr " + VERSION +
                                           " • Made with ♥ by vicyush#4018")
    embed.set_author(name="Help")
    embed.add_field(name="Reminder", value="**@Brynhildr remindme \"(action)\" "
                    "(time)** | Basic reminder function. Warning: the bot is in"
                    " active development and constant reboots mean that "
                    "reminders over a longer time period may be lost.",
                    inline=False)
    embed.add_field(name="GBF Lookup", value="**@Brynhildr lookup (item)** | "
                    "Lookup of pages from the GBF wiki. Currently, only weapon,"
                    " summon, event, and playable character lookup is "
                    "supported.", inline=False)
    embed.add_field(name="Simple GBF Lookup", value="**@Brynhildr lookupsimple"
                    " (item)** | Lookup of pages from the GBF wiki, with less "
                    "information and in a smaller embed. Currently, only "
                    "weapon, summon, event, and  playable character lookup is "
                    "supported.", inline=False)
    embed.add_field(name="Lazy GBF Lookup", value="**[(item)]** anywhere in "
                    "your message; **s[(item)]** for simple lookup | "
                    "Functionally identical to normal lookup, but less effort "
                    "to use.", inline=False)
    embed.add_field(name="Help Page", value="**@Brynhildr help** | Brings "
                                            "up the help page.", inline=False)
    embed.add_field(name="Wiki Lookup Tips", value="**@Brynhildr wikihelp** | "
                    "A separate help page just for GBF Wiki lookup, with tips "
                    "on finding the specific page you want.",
                    inline=False)
    embed.add_field(name="Support Server Invite", value="**@Brynhildr discord**"
                    " | DMs an invite to the support server to you.")
    embed.timestamp = datetime.datetime.utcnow()
    await embedsend(message, embed)


async def wikihelp(message) -> None:
    await message.channel.trigger_typing()
    await message.add_reaction(CLOCK)
    embed = discord.Embed()
    embed.title = "Wiki Lookup Tips"
    embed.description = "The lookup service is built off of the GBF Wiki. A " \
                        "side effect of this is that searches are spelling " \
                        "and case sensitive, among other peculiarities:"
    embed.add_field(name="If a character has multiple versions, its oldest or "
                         "lowest-rarity version usually gets the \"base\" name",
                    value="For example, searching only \"Vira\" will return the"
                          " SR version of her.", inline=False)
    embed.add_field(name="If a character also exists as a summon or event, the "
                         "character page usually gets the \"base\" name",
                    value="For example, searching only \"Grimnir\" will return "
                          "the playable character, and not the summon.",
                    inline=False)
    embed.add_field(name="When specifying a specific version, enclose the "
                         "specification in parentheses",
                    value="For example, to specify Baal the summon, search "
                          "\"Baal (Summon)\".", inline=False)
    embed.add_field(name="Some cases can be tricky",
                    value="For example, searching \"Robomi (Event)\" will "
                    "return the SR event character, while \"Robomi (Side Story)"
                    "\" will return the side story event where you recruit "
                    "her.", inline=False)
    embed.add_field(name="Wiki page nicknames are supported",
                    value="For those more familiar with the wiki, you can use "
                    "page nicknames and it will still function normally. For "
                    "example, searching \"AES\" returns Ancient Ecke Sachs, and"
                    " searching \"Birdman\" returns Nezahualpilli.",
                    inline=False)
    embed.add_field(name="Unite and Fight has a special notation",
                    value="While Unite and Fight event lookup is limited due to"
                    " its complex nature, it is possible to look up past "
                    "iterations to check the enemy's element in that event. To "
                    "search for a specific iteration, add the month and year "
                    "directly after \"Unite and Fight\", separated by a slash. "
                    "For example, looking up \"Unite and Fight/May 2019\" will "
                    "return the May 2019 iteration of Unite and Fight, noting "
                    "that that iteration featured Water element enemies.",
                    inline=False)
    embed.set_author(name="GBF Wiki Lookup",
                     icon_url="https://gbf.wiki/images/1/18/Vyrnball.png?0704c")
    embed.set_footer(icon_url=AVATAR, text="Brynhildr " + VERSION +
                                           " • Made with ♥ by vicyush#4018")
    embed.timestamp = datetime.datetime.utcnow()
    await embedsend(message, embed)


async def discordinvite(message) -> None:
    await message.author.send("Here is the invite to the Brynhildr Bot support "
                              "server, as you requested:\n"
                              "https://discord.gg/3uRTuMU")


async def botstats(message) -> None:
    if str(message.author.id) == os.environ.get("DEV1") or \
            str(message.author.id) == os.environ.get("DEV2"):
        servercount = 0
        usercount = 0
        servers = ""
        for server in client.guilds:
            servers += server.name + ", "
            servercount += 1
            usercount += server.member_count
        servers = servers[:-1]
        await message.channel.send("Servers: " + servers + "\n" +
                                   str(usercount) + " users in " +
                                   str(servercount) + " servers")


async def zeta(message) -> None:
    await message.channel.send("<:zeta_0_0:733749922645409803>"
                               "<:zeta_1_0:733749923031416852>"
                               "<:zeta_2_0:733749923421618206>"
                               "<:zeta_3_0:733749923627139213>"
                               "<:zeta_4_0:733749924436508683>"
                               "<:zeta_5_0:733749924465868802>"
                               "<:zeta_6_0:733749924633641042>\n"
                               "<:zeta_0_1:733749922653798491>"
                               "<:zeta_1_1:733749922771238965>"
                               "<:zeta_2_1:733749923123822694>"
                               "<:zeta_3_1:733749923647848458>"
                               "<:zeta_4_1:733749924436639834>"
                               "<:zeta_5_1:733749924478451753>"
                               "<:zeta_6_1:733749924662870086>\n"
                               "<:zeta_0_2:733749922691678218>"
                               "<:zeta_1_2:733749923081617458>"
                               "<:zeta_2_2:733749923085942805>"
                               "<:zeta_3_2:733749923710763059>"
                               "<:zeta_4_2:733749924088250440>"
                               "<:zeta_5_2:733749924197564467>"
                               "<:zeta_6_2:733749924654612570>\n"
                               "<:zeta_0_3:733749922775695441>"
                               "<:zeta_1_3:733749923169959976>"
                               "<:zeta_2_3:733749923274686555>"
                               "<:zeta_3_3:733749923362898002>"
                               "<:zeta_4_3:733749924545560716>"
                               "<:zeta_5_3:733749924461674626>"
                               "<:zeta_6_3:733749924394434581>\n"
                               "<:zeta_0_4:733749922763112499>"
                               "<:zeta_1_4:733749923165503578>"
                               "<:zeta_2_4:733749923283075177>"
                               "<:zeta_3_4:733749923937386566>"
                               "<:zeta_4_4:733749924537171999>"
                               "<:zeta_5_4:733749924142776472>"
                               "<:zeta_6_4:733749924688167053>\n"
                               "<:zeta_0_5:733749922637021267>"
                               "<:zeta_1_5:733749922880290899>"
                               "<:zeta_2_5:733749923446652939>"
                               "<:zeta_3_5:733749924415668285>"
                               "<:zeta_4_5:733749924038180935>"
                               "<:zeta_5_5:733749924373725187>"
                               "<:zeta_6_5:733749924788961361>\n"
                               "<:zeta_0_6:733749922909913128>"
                               "<:zeta_1_6:733749923232874566>"
                               "<:zeta_2_6:733749923656368249>"
                               "<:zeta_3_6:733749924507943013>"
                               "<:zeta_4_6:733749924528914552>"
                               "<:zeta_5_6:733749924533108746>"
                               "<:zeta_6_6:733749924738367498>")


async def reminder(command: str, message) -> None:
    """
    Processes natural text-style input for the reminder function. Passes
    processed input to reminderoutput. Processing done by looking for specific
    strings in input. No machine learning here, just if statements (what's the
    difference?).
    Ideal format: Hey bot/[mention], remind me to [reminder] in/at [time]
    Key strings for processing (in required order):
    - Hey bot/[mention]
    - remind me to
    - in/at
    Time must be specified AFTER the reminder or else processing will not
    function properly. Error messages will be returned if input cannot be
    processed.
    """
    now = pytz.utc.localize(datetime.datetime.now())
    if "remind me to " in command:
        action = command.split("remind me to ", 1)[1]
    else:
        await message.channel.send(ERRORMESSAGE)
        return
    if action.rfind("in ") < 0 and action.rfind("at ") < 0:
        await message.channel.send(ERRORMESSAGE)
        return
    elif action.rfind("in ") > action.rfind("at "):
        endtime = dateparser.parse(action[action.rfind("in "):])
        if not endtime:
            await message.channel.send(ERRORMESSAGE)
            return
        delta = pytz.utc.localize(endtime) - now
        action = action[:action.rfind("in ")]
    else:
        endtime = dateparser.parse(action[action.rfind("at "):])
        if not endtime:
            await message.channel.send(ERRORMESSAGE)
            return
        delta = pytz.utc.localize(endtime) - now
        action = action[:action.rfind("at ")]
    await reminderoutput(action, delta, message)


async def reminderstripped(command: str, message) -> None:
    """
    Processes command-style input for the reminder function. Passes processed
    input to reminderoutput.
    Format: Hey bot/[mention] remindme "[reminder (in quotation marks)]" [time]
    """
    now = pytz.utc.localize(datetime.datetime.now())
    action = command.split("remindme ", 1)[1]
    date = action[action.rfind('"'):]
    if not date:
        await message.channel.send(ERRORMESSAGE)
        return
    action = action[1:action.rfind('"')]
    date = pytz.utc.localize(dateparser.parse(date))
    delta = now - date
    await reminderoutput(action + " ", delta, message)


async def reminderoutput(action: str, delta: datetime.timedelta, message) -> \
        None:
    if delta.days < 0 or delta.seconds < 0 or delta.microseconds < 0:
        await message.channel.send("The time you want is in the past. It's " +
                                   "too late for that now.")
        return
    times = [delta.days, delta.seconds // 3600, (delta.seconds // 60) % 60,
             delta.seconds % 60]
    units = [" days", " hours", " minutes", " seconds"]
    unitsused = sum(1 for x in times if x > 0)
    output = "Okay " + message.author.mention + ", I'll remind you to " + \
             action + "in "
    i = 0
    if unitsused == 1:
        while i < 5:
            if times[i] > 1:
                output += str(times[i]) + units[i] + "."
                break
            elif times[i] == 1:
                output += str(times[i]) + units[i][:-1] + "."
                break
            i += 1
    elif unitsused == 2:
        while unitsused > 1 and i < 5:
            if times[i] > 1:
                output += str(times[i]) + units[i]
                unitsused -= 1
            elif times[i] == 1:
                output += str(times[i]) + units[i][:-1]
                unitsused -= 1
            i += 1
        while unitsused == 1 and i < 5:
            if times[i] > 1:
                output += " and " + str(times[i]) + units[i] + "."
                break
            elif times[i] == 1:
                output += " and " + str(times[i]) + units[i][:-1] + "."
                break
            i += 1
    else:
        while unitsused > 1 and i < 5:
            if times[i] > 1:
                output += str(times[i]) + units[i] + ", "
                unitsused -= 1
            elif times[i] == 1:
                output += str(times[i]) + units[i][:-1] + ", "
                unitsused -= 1
            i += 1
        while unitsused == 1 and i < 5:
            if times[i] > 1:
                output += "and " + str(times[i]) + units[i] + "."
                break
            elif times[i] == 1:
                output += "and " + str(times[i]) + units[i][:-1] + "."
                break
            i += 1
    await message.channel.send(output)
    if delta.days > 0 or delta.seconds // 3600 > 1:
        await message.channel.send("Please be careful when asking for reminders"
                                   " over extended periods of time. The bot is "
                                   "in constant development and will reboot to "
                                   "implement new changes, losing any "
                                   "reminders that have been set.")
    await asyncio.sleep(delta.seconds + (delta.days * 86400))
    await message.channel.send(message.author.mention +
                               ", I'm reminding you to " + action +
                               "as you requested.")


async def lookup(command: str, message, simple: bool, quick: bool) -> None:
    """
    Processes command-style input for the lookup function.
    Format: Hey bot/[mention] lookup [item]
    """
    if not quick:
        if simple:
            item = command[command.lower().rfind("lookupsimple") + 13:]
        else:
            item = command[command.lower().rfind("lookup") + 7:]
        await lookupgbf(item, message, simple)
    else:
        await lookupgbf(command, message, simple)


async def lookupgbf(item: str, message, simple: bool) -> None:
    await message.channel.trigger_typing()
    await message.add_reaction(CLOCK)
    # Get a page with the given input
    url = "https://gbf.wiki/" + item.replace(" ", "_")
    page = requests.get(url)
    # Create embed(s)
    embed = discord.Embed()
    embed2 = discord.Embed()
    # Check if the input returns a valid page
    if "There is currently no text in this page." in page.text:
        url = "https://gbf.wiki/index.php?search=" + item.replace(" ", "+")
        page = requests.get(url)
        await gbfsearch(item, page.text, message, embed, simple)
        return
    else:
        # Get page categories
        categories = page.text[page.text.find("wgCategories") +
                               15:].split("]", 1)[0].strip("\"").split("\",\"")
        if "Weapons" in categories:
            await weaponparse(categories, page.text, embed, simple)
        elif "Characters" in categories:
            embed2 = await characterparse(categories, page.text, embed, simple)
        elif "Summons" in categories:
            await summonparse(categories, page.text, embed, simple)
        elif "Events" in categories:
            await eventparse(categories, page.text, embed, simple)
        # Page type not supported
        else:
            await message.remove_reaction(CLOCK, client.user)
            await message.add_reaction(ERROR)
            output = await message.channel.send("<:despair:376080252754984960> "
                                                "This is not a weapon, summon, "
                                                "event, or playable character "
                                                "page. I can't handle those "
                                                "pages right now.")
            await asyncio.sleep(5)
            await message.remove_reaction(ERROR, client.user)
            await output.delete()
            return
    embed.url = url
    embed.set_author(name="GBF Wiki Lookup",
                     icon_url="https://gbf.wiki/images/1/18/Vyrnball.png?0704c")
    embed.set_footer(text="Brynhildr Bot is not affiliated with the GBF Wiki. •"
                     " Brynhildr " + VERSION + "\nSome links may not display "
                                               "properly on mobile. ",
                     icon_url=AVATAR)
    embed.timestamp = datetime.datetime.utcnow()
    if embed2 is not None:
        embed2.url = url
        embed2.set_author(name="GBF Wiki Lookup",
                          icon_url="https://gbf.wiki/images/1/18/Vyrnball.png?0"
                                   "704c")
        embed2.set_footer(text="Brynhildr Bot is not affiliated with the GBF "
                               "Wiki. • Brynhildr " + VERSION + "\nSome links "
                               "may not display properly on mobile. ",
                          icon_url=AVATAR)
        embed2.timestamp = datetime.datetime.utcnow()
    await embedsend(message, embed, embed2)


async def gbfsearch(item: str, source: str, message, embed: discord.Embed,
                    simple: bool) -> None:
    embed.set_author(name="GBF Wiki Lookup",
                     icon_url="https://gbf.wiki/images/1/18/Vyrnball.png?0704c")
    embed.set_footer(text="Brynhildr Bot is not affiliated with the GBF Wiki. •"
                     " Brynhildr " + VERSION + "\nSome links may not display "
                                               "properly on mobile. ",
                     icon_url=AVATAR)
    embed.timestamp = datetime.datetime.utcnow()
    parsed = BeautifulSoup(source, "html.parser")
    resultsearch = []
    results = []
    # Check if search can find anything
    if not parsed.find("p", {"class": "mw-search-nonefound"}):
        for result in parsed.find_all("div", {"class":
                                              "mw-search-result-heading"}):
            a = result.find("a")
            # Check if result is supported by lookup
            page = requests.get("https://gbf.wiki/" +
                                a.text.replace(" ", "_")).text
            categories = page[page.find("wgCategories") +
                              15:].split("]", 1)[0]
            cases = ["\"Weapons\"", "\"Characters\"", "\"Summons\"",
                     "\"Events\""]
            if not any(category in categories for category in cases):
                continue
            # Collect a duplicate for later use
            resultsearch.append(a.text)
            # Format text
            a.replace_with("[" + a.text + "](https://gbf.wiki" + a["href"] +
                           ")")
            results.append(result.text)
            # Collect first 5 valid results
            if len(results) == 5:
                break
        embed.title = "Search Results for \"" + item + "\":"
        embed.description = ""
        i = 1
        for result in results:
            embed.description += "**" + str(i) + ".** " + result + "\n"
            i += 1
            if i >= 6:
                break
    # Case for if no valid results are found
    if parsed.find("p", {"class": "mw-search-nonefound"}) or not resultsearch:
        embed.title = "No results found for \"" + item + "\""
        output = await message.channel.send(embed=embed)
        await message.remove_reaction(CLOCK, client.user)
        await message.add_reaction(ERROR)
        await asyncio.sleep(5)
        await output.delete()
        await message.remove_reaction(ERROR, client.user)
        return
    try:
        output = await message.channel.send(embed=embed)
        await message.remove_reaction(CLOCK, client.user)
        await message.add_reaction(QUESTION_MARK)
        i = 0
        while i < len(results):
            await output.add_reaction(REACTIONS[i])
            i += 1
        await output.add_reaction("\U0001F5D1")
    except Exception as e:
        await message.channel.send("Something went wrong. Please let the bot"
                                   " owner know so this can be fixed.\nError "
                                   "details: " + e.__str__())
        await message.remove_reaction(CLOCK, client.user)
        await message.add_reaction(ERROR)
        return

    # Verify that the reaction was for the right message and is one of the
    # indicated types
    def reactsearch(react, user):
        if user != client.user and react.message.id == output.id:
            if str(react.emoji) == "\U00000031\U0000FE0F\U000020E3":
                react.emoji = 1
                return 1
            elif str(react.emoji) == "\U00000032\U0000FE0F\U000020E3":
                react.emoji = 2
                return 2
            elif str(react.emoji) == "\U00000033\U0000FE0F\U000020E3":
                react.emoji = 3
                return 3
            elif str(react.emoji) == "\U00000034\U0000FE0F\U000020E3":
                react.emoji = 4
                return 4
            elif str(react.emoji) == "\U00000035\U0000FE0F\U000020E3":
                react.emoji = 5
                return 5
            elif str(react.emoji) == "\U0001F5D1":
                react.emoji = "delete"
                return "delete"

    # Wait for reaction
    try:
        reaction = await client.wait_for("reaction_add", timeout=1800,
                                         check=reactsearch)
    # Abandon check after 30 minutes
    except asyncio.TimeoutError:
        output = await message.channel.fetch_message(output.id)
        for reaction in output.reactions:
            await output.remove_reaction(str(reaction.emoji), client.user)
    # Apply lookup to the new selected search term
    else:
        await message.remove_reaction(QUESTION_MARK, client.user)
        if reaction[0].emoji == "delete":
            await output.delete()
            await message.add_reaction("\U0001F5D1")
            await asyncio.sleep(5)
            await message.remove_reaction("\U0001F5D1", client.user)
        else:
            await output.delete()
            await lookupgbf(resultsearch[reaction[0].emoji - 1], message,
                            simple)


async def embedsend(message: discord.message, embed: discord.Embed,
                    embed2: discord.Embed = None) -> None:
    state = 1
    if embed2 is not None:
        multi = True
    else:
        multi = False
    try:
        output = await message.channel.send(embed=embed)
        await message.remove_reaction(CLOCK, client.user)
        await message.add_reaction(CHECK_MARK)
        if multi:
            await output.add_reaction("🔄")
        await output.add_reaction("\U0001F5D1")
    except Exception as e:
        await message.channel.send("Something went wrong. Please let the bot"
                                   " owner know so this can be fixed.\nError "
                                   "details: " + e.__str__())
        await message.remove_reaction(CLOCK, client.user)
        await message.add_reaction(ERROR)
        return

    # Verify that the reaction was for the right message and is one of the
    # indicated types
    def reactsearch(react, user):
        if user != client.user and react.message.id == output.id:
            if str(react.emoji) == "🔄" and multi:
                react.emoji = 1
                return 1
            elif str(react.emoji) == "\U0001F5D1":
                react.emoji = "delete"
                return "delete"

    while True:
        # Wait for reaction
        try:
            reaction = await client.wait_for("reaction_add", timeout=1800,
                                             check=reactsearch)
        # Abandon check after 30 minutes
        except asyncio.TimeoutError:
            output = await message.channel.fetch_message(output.id)
            for reaction in output.reactions:
                await output.remove_reaction(str(reaction.emoji), client.user)
            break
        # Apply lookup to the new selected search term
        else:
            if reaction[0].emoji == "delete":
                await output.delete()
                await message.remove_reaction(CHECK_MARK, client.user)
                await message.add_reaction("\U0001F5D1")
                await asyncio.sleep(5)
                await message.remove_reaction("\U0001F5D1", client.user)
                break
            else:
                if reaction[0].emoji == 1 and state == 2:
                    await output.edit(embed=embed)
                    state = 1
                elif reaction[0].emoji == 1 and state == 1:
                    await output.edit(embed=embed2)
                    state = 2
                if reaction[1] != client.user:
                    if reaction[0].emoji == 1:
                        await output.remove_reaction("🔄", reaction[1])


client.run(os.environ.get("DISCORD_TOKEN"))
