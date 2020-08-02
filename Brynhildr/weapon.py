import discord
from bs4 import BeautifulSoup


async def weaponparse(categories: str, source: str, embed: discord.Embed) -> \
        None:
    # Generate the title of the embed
    embed.title = source[source.find("wgTitle") + 10:].split('"', 1)[0]
    await generateicons(categories, embed)
    # Get description, and change apostrophe escape characters to actual
    # apostrophes
    description = source[source.find("meta name=\"description\" content=") +
                         33:].split('"', 1)[0].replace("&#039;", "'")
    # Generate the obtain field of the embed
    obtain = await generateobtains(source)
    # Generate the CA field of the embed
    # CA = await generateca(source)
    # Find weapon image
    image = source[source.find("og:image\" content=\"") + 19:].split('"', 1)[0]
    embed.description += description
    embed.set_thumbnail(url=image)
    embed.add_field(name="Obtain", value=obtain)


async def generateicons(categories: str, embed) -> None:
    text = ""
    # Assign rarity icons
    if "SSR Weapons" in categories:
        text += " <:Rarity_SSR:730441789667934278>"
    elif "SR Weapons" in categories:
        text += " <:Rarity_SR:730441789319807009>"
    elif "R Weapons" in categories:
        text += " <:Rarity_R:730441789642768464>"
    elif "N Weapons" in categories:
        text += " <:Rarity_N:730441824954482728>"
    # Assign element icons
    if "Fire Weapons" in categories:
        text += " <:Fire:730845600484032624>"
    elif "Water Weapons" in categories:
        text += " <:Water:730845600324780151>"
    elif "Earth Weapons" in categories:
        text += " <:Earth:730845600672776202>"
    elif "Wind Weapons" in categories:
        text += " <:Wind:730845600479707157>"
    elif "Light Weapons" in categories:
        text += " <:Light:730845600915914873>"
    elif "Dark Weapons" in categories:
        text += " <:Dark:730845600613924954>"
    # Assign weapon type icon
    if "Sabre Weapons" in categories:
        text += " <:Sabre1:730454365248159855><:Sabre2:730454663941324861>"
    elif "Dagger Weapons" in categories:
        text += " <:Dagger1:730455370233020558><:Dagger2:730455370673291314>"
    elif "Spear Weapons" in categories:
        text += " <:Spear1:730456104898920458><:Spear2:730456104840200363>"
    elif "Axe Weapons" in categories:
        text += " <:Axe1:730456397942095943><:Axe2:730456397556482110>"
    elif "Staff Weapons" in categories:
        text += " <:Staff1:730456836221829173><:Staff2:730456836310040677>"
    elif "Gun Weapons" in categories:
        text += " <:Gun1:730457164552077382><:Gun2:730457164266864784>"
    elif "Melee Weapons" in categories:
        text += " <:Melee1:730457549672939621><:Melee2:730457549337264139>"
    elif "Bow Weapons" in categories:
        text += " <:Bow1:730457814627254322><:Bow2:730457814551756840>"
    elif "Harp Weapons" in categories:
        text += " <:Harp1:730458095591096420><:Harp2:730458095221997580>"
    elif "Katana Weapons" in categories:
        text += " <:Katana1:730458503742750822><:Katana2:730458504011317319>"
    elif "Boost Weapons" in categories:
        text += " <:Boost1:730458765475840091><:Boost2:730458765362593812>"
    embed.description = text + "\n"


async def generateobtains(source: str) -> str:
    # The table for obtain information is inconsistently coded. This checks
    # which coding method is being used and cleans the input accordingly.
    parsed = BeautifulSoup(source, 'html.parser')
    obtainlinks = []
    obtaintext = []
    obtain = ""
    if "class=\"obtain-list-item\">" in source:
        # Thank you BS4 very cool
        obtainraw = parsed.find_all("div", {"class": "obtain-list-item"})
        for entry in obtainraw:
            links = entry.find_all("a")
            obtainlinks.append(links[len(links) - 1]['href'])
            obtaintext.append(links[len(links) - 1].text)
    else:
        obtainraw = parsed.find_all("td", {"class": "obtain-list"})
        links = obtainraw[0].find_all("a")
        for entry in links:
            obtainlinks.append(entry['href'])
            obtaintext.append(entry.text)
    # Generate output string
    i = 0
    while i < len(obtainlinks):
        obtain += ("[" + obtaintext[i] + "](https://gbf.wiki" +
                   obtainlinks[i] + ")\n")
        i += 1
    return obtain


async def generateca(source) -> str:
    # Cutting out unneeded bits
    raw = source[source.find("<img alt=\"Skill") + 15:] \
        .split("</tr>", 1)[0]
    raw = raw[raw.find("<td class=\"skill-name\">") + 23:]
    # ...Mirage Munitions
    if "None" in raw:
        return "None"
    # Getting the name
    name = raw.split("</td>", 1)[0]
    # More cutting
    raw = raw[raw.find("<td>") + 4:]
    # Remove citations
    while "<sup" in raw:
        raw = raw[raw.find("<sup"):] + raw[:raw.find("</sup>") + 6]
    # Remove line breaks
    while "<br />" in raw:
        raw = raw[raw.find("<br />"):] + " " + raw[:raw.find("<br />") + 6]
    # Check for charge bar effects
    while "<a href=\"/Status_Effects#Charge_Bar" in raw:
        if ">Charge Bar" not in raw[raw.find
                                    ("<a href=\"/Status_Effects#Charge_Bar"):] \
                .split("</a>", 1)[0]:
            # Image, replace with emote
            raw = raw[raw.find("<a href=\"/Status_Effects#Charge_Bar"):] + \
                            "<:ChargeBar:730532683364434092> " + \
                            raw[:raw.find("</a>") + 4]
        else:
            # Text, remove wrapper
            raw = raw[raw.find("<a href=\"/Status_Effects#Charge_Bar"):] + \
                  raw[:raw[raw.find("<a href=\"/Status_Effects#Charge_Bar"):].
                      find(">")]
    # Check for Revitalize effects
    while "<a href=\"/Revitalize" in raw:
        if ">Revitalize" not in raw[raw.find
                                    ("<a href=\"/Revitalize"):] \
                .split("</a>", 1)[0]:
            # Image, replace with emote
            raw = raw[raw.find("<a href=\"/Revitalize"):] + \
                            "<:ChargeBar:730532683364434092> " + \
                            raw[:raw.find("</a>") + 4]
        else:
            # Text, remove wrapper
            raw = raw[raw.find("<a href=\"/Revitalize"):] + \
                  raw[:raw[raw.find("<a href=\"/Revitalize"):].
                      find(">")]
    output = ""
    return output
