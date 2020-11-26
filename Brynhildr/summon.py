import discord
from icons import iconreplace
from util import *


async def summonparse(categories: str, source: str, embed: discord.Embed,
                      simple: bool) -> None:
    parsed = BeautifulSoup(source, 'html.parser')
    # Generate the title of the embed
    embed.title = parsed.find("h1", {"id": "firstHeading"}).text
    # Generate icon line
    await generateicons(categories, embed)
    # Get description, and change apostrophe escape characters to actual
    # apostrophes
    if parsed.find("meta", {"name": "description"}):
        description = parsed.find("meta", {"name": "description"})["content"] \
            .replace("&#039;", "'")
    else:
        description = ""
    # Find summon image
    image = parsed.find("meta", {"property": "og:image"})["content"]
    # Put the basic content together
    embed.description += description
    embed.set_thumbnail(url=image)
    # Advanced lookup
    if not simple:
        # Generate the obtain field of the embed
        if embed.title == "Proto Bahamut":
            obtain = "Initial summon stone"
        else:
            obtain = await generateobtain(source)
        aura = await generateaura(source, categories)
        call = await generatecall(source)
        embed.add_field(name="Obtain", value=obtain, inline=True)
        embed.add_field(name="Aura", value=aura, inline=True)
        embed.add_field(name="Call", value=call[0], inline=False)
        i = 1
        while i < len(call):
            embed.add_field(name=call[i][0], value=call[i][1], inline=False)
            i += 1


async def generateicons(categories: str, embed: discord.Embed) \
        -> None:
    text = ""
    # Assign rarity icons
    if "SSR Summons" in categories:
        text += " <:Rarity_SSR:730441789667934278>"
    elif "SR Summons" in categories:
        text += " <:Rarity_SR:730441789319807009>"
    elif "R Summons" in categories:
        text += " <:Rarity_R:730441789642768464>"
    elif "N Summons" in categories:
        text += " <:Rarity_N:730441824954482728>"
    # Assign element icons
    if "Fire Summons" in categories:
        text += " <:Fire:730845600484032624>"
    elif "Water Summons" in categories:
        text += " <:Water:730845600324780151>"
    elif "Earth Summons" in categories:
        text += " <:Earth:730845600672776202>"
    elif "Wind Summons" in categories:
        text += " <:Wind:730845600479707157>"
    elif "Light Summons" in categories:
        text += " <:Light:730845600915914873>"
    elif "Dark Summons" in categories:
        text += " <:Dark:730845600613924954>"
    # Assign 4/5★ uncap icons
    if "4★ Summons" in categories:
        text += " <:BlueStar:739887435936301152>"
    if "5★ Summons" in categories:  # This is not a mistake
        text += "<:BlueStar:739887435936301152>"
    embed.description = text + "\n"


async def generateobtain(source: str) -> str:
    raw = source[source.find("Obtain") + 6:].split("</tr>", 1)[0]
    obtaintext = []
    obtainlinks = []
    obtain = ""
    parsed = BeautifulSoup(raw, "html.parser")
    removetooltip(parsed)
    # Generate link-text pairs
    for a in parsed.find_all("a"):
        obtainlinks.append(a["href"])
        obtaintext.append(a.text)
    # Put it all together
    i = 0
    while i < len(obtainlinks):
        obtain += ("[" + obtaintext[i] + "](https://gbf.wiki" + obtainlinks[i]
                   + ")\n")
        i += 1
    return obtain


async def generateaura(source: str, categories: str) -> str:
    output = ""
    # Check if the summon has sub auras and trim the source accordingly.
    if "Summons with Sub Auras" in categories:
        raw = source[source.find("Main Aura"):].split("</tbody>", 1)[0]
        output += "__Main Aura__\n"
    else:
        raw = source[source.find("Aura"):].split("</tbody>", 1)[0]
    parsed = BeautifulSoup(raw, "html.parser")
    # Remove tooltips
    removetooltip(parsed)
    # Icons
    iconreplace(parsed)
    for tr in parsed.find_all("tr"):
        # Main aura was already inserted in the trimming phase. This inserts
        # the sub aura separator.
        if "Aura" in tr.text:
            output += "__Sub Aura__\n"
        else:
            output += "**" + tr.find("th").text + ":** " + tr.find("td").text \
                      + "\n"
    return output

async def generatecall(source: str) -> list:
    # Empty variables to be filled later
    output = []
    outputtext = ""
    # Trim to what's needed
    raw = source[source.find("/Summons#Calls") - 25:].split("</tbody>", 1)[0]
    parsed = BeautifulSoup(raw, "html.parser")
    # Miscellaneous cleaning
    removetooltip(parsed)
    removecitation(parsed)
    iconreplace(parsed)
    # Remove cooldown text
    for th in parsed.find_all("th", {"style": "width:35px;"}):
        th.replace_with("")
    # Get call name
    output.append("Name " + parsed.find("th", {"colspan": "2"}).text.
                  split(" ", 1)[1])
    # Counters and buffer variables to be filled
    skillspan = 0
    cdspan = 0
    uncap = ""
    cd = ""
    call = ""
    for tr in parsed.find_all("tr"):
        # Check if the row has call text, or if it's just an uncap identifier
        # or uncomboable identifier
        if tr.find("td"):
            # Check if the call text covers multiple uncaps, and increment
            # skillspan accordingly
            if tr.find("td").get("rowspan"):
                skillspan = int(tr.find("td")["rowspan"])
            # Get call text
            call = tr.find("td").text
            # Check if the "call" is just an indicator that the call cannot be
            # comboed:
            if call == "Can't be included in other players' combo calls.":
                continue
        # De-increment cdspan and keep the cooldown as-is, or get the new
        # cooldown if cdspan is 1 or less
        if cdspan > 1:
            cdspan -= 1
        else:
            for td in tr.find_all("td", {"style": "text-align:center;"}):
                # If the cooldown has separate values for first call and
                # subsequent calls, the first call will be recorded, and then
                # when the tr steps to the next cooldown (for subsequent calls),
                # a slash will be inserted to split the two.
                if cd:
                    cd += "/"
                cd += td.text
                if td.get("rowspan"):
                    cdspan = int(td['rowspan'])
        # Inserts a slash between multiple uncaps with the same call text and
        # de-increments skillspan, or gets the uncap level.
        if uncap:
            uncap += "/" + tr.find("th").text
            skillspan -= 1
        else:
            if "once" not in tr.text:
                uncap = tr.find("th").text
        # If all the uncaps are covered (skillspan <=1), then the output is
        # processed and stored, and the buffer variables and counters are reset.
        if skillspan <= 1:
            skillspan = 0
            # Check for the case of single-use summons
            if "Can only be summoned once per battle." not in tr.text:
                output.append(("" + uncap, call + " (" + cd + ")"))
            else:
                output[0] += "\n**" + call + "**"
            uncap = ""
            if cdspan <= 1:
                cd = ""
    return output
