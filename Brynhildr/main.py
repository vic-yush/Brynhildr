import asyncio
import discord
import dateparser
import datetime
import pytz
import requests

client = discord.Client()

ERRORMESSAGE = "Sorry, I couldn't understand that. Could you try again?"


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith("Hey") or client.user in \
            message.mentions:
        if "remind me" in message.content.lower():
            await reminder(message.content.lower(), message)
        elif "remindme" in message.content.lower():
            await reminderstripped(message.content.lower(), message)
        elif "lookup" in message.content.lower():
            await lookupstripped(message.content, message)


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
        delta = endtime - now
        action = action[:action.rfind("in ")]
    else:
        endtime = dateparser.parse(action[action.rfind("at "):])
        if not endtime:
            await message.channel.send(ERRORMESSAGE)
            return
        delta = endtime - now
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
    await asyncio.sleep(delta.seconds + (delta.days * 86400))
    await message.channel.send(message.author.mention +
                               ", I'm reminding you to " + action +
                               "as you requested.")


async def lookupstripped(command: str, message) -> None:
    """
    Processes command-style input for the lookup function.
    Format: Hey bot/[mention] lookup [item]
    Currently not supporting lookup of Excalibur.
    """
    item = command[command.lower().rfind("lookup") + 7:]
    if item == "Excalibur":
        await message.channel.send("GBF lookup currently does not support "
                                   "lookup of Excalibur")
    await lookupoutput(item, message)


async def lookupoutput(item: str, message) -> None:
    url = "https://gbf.wiki/" + item.replace(" ", "_")
    page = requests.get(url)
    if "There is currently no text in this page." in page.text:
        await message.channel.send("Could not find this item. Search "
                                   "functionality will be added soon.")
        return
        # page = requests.get("https://gbf.wiki/index.php?search=" +
        #                     item.replace(" ", "+"))
        # results = [i for i in range(len(page.text)) if page.text.startswith
        #            ("mw-search-result-heading", i)]
    categoryindex = page.text.find("wgCategories")
    if "Weapons" not in page.text[categoryindex + 25:].split("]", 1)[0]:
        await message.channel.send("This is not a weapon page. I can't handle "
                                   "non-weapon pages right now.")
        return
    description = page.text[page.text.find
                            ("meta name=\"description\" content=") + 33:]\
        .split('"', 1)[0]
    obtainraw = page.text[page.text.find("class=\"obtain-list\"><div>") + 25:]\
        .split("</div>", 1)[0]
    obtainlinks = [i for i in range(len(obtainraw)) if obtainraw.startswith
                   ("<a href=", i)]
    obtaintext = [i for i in range(len(obtainraw)) if obtainraw.startswith
                  ("\">", i)]
    index = 0
    while index < len(obtaintext) and obtaintext[index] < len(obtainraw):
        if obtainraw[obtaintext[index] + 2: obtaintext[index] + 6] == "<img":
            del obtainlinks[index]
            del obtaintext[index]
        index += 1
    obtain = ""
    i = 0
    while i < len(obtainlinks):
        obtain += ("[" + obtainraw[obtaintext[i] + 2:].split('<', 1)[0] +
                   "](https://gbf.wiki" +
                   obtainraw[obtainlinks[i] + 9:].split('"', 1)[0] + ")\n")
        i += 1
    image = page.text[page.text.find("flex-direction:row;\">") + 21:].split(
        "</a>", 1)[0]
    image = "https://gbf.wiki" + \
            image[image.find("/images/thumb"):].split('"', 1)[0]
    embed = discord.Embed()
    embed.title = page.text[page.text.find("wgTitle") + 10:].split('"', 1)[0]
    embed.url = url
    embed.set_author(name="GBF Wiki Lookup",
                     icon_url="https://gbf.wiki/images/1/18/Vyrnball.png?0704c")
    embed.description = description
    embed.add_field(name="Obtain", value=obtain)
    embed.set_thumbnail(url=image)
    embed.set_footer(text="Brynhildr Bot is not associated with the GBF Wiki.")
    await message.channel.send(embed=embed)

client.run("NzI5MzkyNDIwNzA1NDAzMDEw.XwNE5Q.MQE4Nk24i4N9-kG_wa8AIvsAsV8")
