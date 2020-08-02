import asyncio
import discord
import dateparser
import datetime
import pytz
import requests
from weapon import weaponparse
from character import characterparse
from summon import summonparse

client = discord.Client()

ERRORMESSAGE = "<:despair:376080252754984960> Sorry, I couldn't understand th" \
               "at. Could you try again?"
MENTIONS = ("hey bryn", "hey brynhildr", "hey brynhild", "hi bryn",
            "hi brynhildr", "hi brynhild", "okay bryn", "okay brynhildr",
            "okay brynhild")
GBF = ["lookup gbf", "look up gbf"]
LEAGUE = ["lookup lol", "look up lol"]
VERSION = "v1.07"
AVATAR = "https://cdn.discordapp.com/avatars/729790460175843368/c6c040e37004c" \
         "30ea82c1d3280792e98.png"
TOKEN = "NzI5NzkwNDYwMTc1ODQzMzY4.XwON_A.sXcW5jkXUSr3o3jvRTXXljBvZzg"


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching,
                                  name="the stars"))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith(MENTIONS) or client.user in \
            message.mentions:
        if "remind me" in message.content.lower():
            await reminder(message.content.lower(), message)
        elif "remindme" in message.content.lower():
            await reminderstripped(message.content.lower(), message)
        elif "lookup" in message.content.lower():
            await lookup(message.content, message)
        elif "help" in message.content.lower():
            await manual(message)
        elif "changelog" in message.content.lower():
            await changelog(message)
        elif "zeta" in message.content.lower():
            await zeta(message)
    elif message.content.lower() == "bad bot":
        await message.channel.send("Bad human")
    elif message.content.lower() == "good bot":
        await message.channel.send("Good human")


async def changelog(message) -> None:
    """
    Change log. Manually typed because file I/O is effort.
    """
    embed = discord.Embed()
    embed.title = "Change Log"
    embed.add_field(name="v1.01", value="- Added change log\n- Added warning "
                                        "for users attempting to set long "
                                        "reminders\n- Added help command "
                                        "functionality")
    embed.add_field(name="v1.02", value="- Fixed weapon lookups with edge cases"
                                        "\n- Minor help page reformatting")
    embed.add_field(name="v1.03", value="- Fixed Luminiera weapon lookups "
                                        "crashing the bot\n- Apostrophes in "
                                        "descriptions display properly now")
    embed.add_field(name="v1.04", value="- Added weapon category icons and"
                                        " retrieval timestamps to weapon "
                                        "lookups")
    embed.add_field(name="v1.05", value="- Replaced element icons with higher-"
                                        "resolution versions\n- Clarity pass"
                                        "on help text")
    embed.add_field(name="v1.06", value="- Added character and summon "
                                        "lookup functionality\n- Moved icons "
                                        "below titles")
    embed.add_field(name="v1.07", value="- Migrated HTML parsing to "
                                        "BeautifulSoup4. This has no effect on"
                                        " what you see, but it saves vic a lot"
                                        " of sanity.")
    embed.set_footer(icon_url=AVATAR, text="Brynhildr " + VERSION +
                                           " • Made with ♥ by vicyush#4018")
    await message.channel.send(embed=embed)
    return


async def manual(message) -> None:
    """
    Help page. That's really it.
    """
    embed = discord.Embed()
    embed.set_footer(icon_url=AVATAR, text="Brynhildr " + VERSION +
                                           " • Made with ♥ by vicyush#4018")
    embed.set_author(name="Help")
    embed.add_field(name="Reminder", value="**@Brynhildr remindme \"[action]\" "
                                           "[time]** | Basic reminder function."
                                           " Warning: the bot is in active "
                                           "development and constant reboots "
                                           "mean that reminders over a longer "
                                           "time period may be lost.",
                    inline=False)
    embed.add_field(name="GBF Lookup", value="**@Brynhildr lookup [item]** | "
                                             "Lookup of pages from the GBF wiki"
                                             ". Currently, only weapon "
                                             "lookup is supported.",
                    inline=False)
    await message.channel.send(embed=embed)
    return


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
                                   "in constant development and will reboot "
                                   "to implement new changes, losing any "
                                   "reminders that have been set.")
    await asyncio.sleep(delta.seconds + (delta.days * 86400))
    await message.channel.send(message.author.mention +
                               ", I'm reminding you to " + action +
                               "as you requested.")


async def lookup(command: str, message) -> None:
    """
    Processes command-style input for the lookup function.
    Format: Hey bot/[mention] lookup [item]
    """
    item = command[command.lower().rfind("lookup") + 7:]
    await lookupgbf(item, message)


async def lookupgbf(item: str, message) -> None:
    # Get a page with the given input
    url = "https://gbf.wiki/" + item.replace(" ", "_")
    page = requests.get(url)
    # Check if the input returns a valid page
    if "There is currently no text in this page." in page.text:
        await message.channel.send("<:despair:376080252754984960> "
                                   "Could not find this item. Search "
                                   "functionality will be added soon.")
        return
        # TODO: Add search functionality
        # page = requests.get("https://gbf.wiki/index.php?search=" +
        #                     item.replace(" ", "+"))
        # results = [i for i in range(len(page.text)) if page.text.startswith
        #            ("mw-search-result-heading", i)]
    # Create embed
    embed = discord.Embed()
    # Get page categories
    categories = page.text[page.text.find("wgCategories") +
                           15:].split("]", 1)[0]
    if "\"Weapons\"" in categories:
        await weaponparse(categories, page.text, embed)
    elif "\"Characters\"" in categories:
        await characterparse(categories, page.text, embed)
    elif "\"Summons\"" in categories:
        await summonparse(categories, page.text, embed)
    else:
        await message.channel.send("<:despair:376080252754984960> This is not a"
                                   " weapon, summon or playable character page."
                                   " I can't handle those pages right now.")
        return
    embed.url = url
    embed.set_author(name="GBF Wiki Lookup",
                     icon_url="https://gbf.wiki/images/1/18/Vyrnball.png?0704c")
    embed.set_footer(text="Brynhildr Bot is not affiliated with the GBF Wiki."
                          " • Brynhildr " + VERSION)
    embed.timestamp = datetime.datetime.utcnow()
    try:
        await message.channel.send(embed=embed)
    except:
        await message.channel.send("Something went wrong. Please let the bot"
                                   " owner know so this can be fixed.")


async def lookuplol() -> None:
    # I'm working on it, I swear.
    return


client.run(TOKEN)
