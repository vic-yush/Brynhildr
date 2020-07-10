import discord


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
    if source.find("class=\"obtain-list-item\">") > 0:
        # Here's the headache...
        obtainraw = source[source.find("class=\"obtain-list-item\">") + 25:] \
            .split("</td", 1)[0]
        # Remove tooltip spans
        while "<span class=\"tooltip\"" in obtainraw:
            obtainraw = obtainraw[:obtainraw.find("<span class=\"tooltip\"")] \
                        + obtainraw[obtainraw.find("</span>") + 7:]
            obtainraw = obtainraw[:obtainraw.find("</span>")] \
                        + obtainraw[obtainraw.find("</span>") + 7:]
        # If both images and image spans are in the remainder, remove the
        # first occurrence of either until there are no images left
        while "<span class=\"image_link\">" in obtainraw and \
                "<img" in obtainraw:
            if obtainraw.find("<span class=\"image_link\">") < \
                    obtainraw.find("<img"):
                obtainraw = obtainraw[:obtainraw.find
                                      ("<span class=\"image_link\">")] + \
                            obtainraw[obtainraw.find("/>") + 2:]
            else:
                obtainraw = obtainraw[:obtainraw.find("<img")] + \
                            obtainraw[obtainraw.find("/>") + 2:]
        # If there are image spans left over, remove them
        while "<span class=\"image_link\">" in obtainraw:
            obtainraw = obtainraw[:obtainraw.find
                                  ("<span class=\"image_link\">")] + \
                        obtainraw[obtainraw.find("/>") + 2:]
        # Remove this div because it breaks parsing
        while "<div class=\"obtain-list-item\">" in obtainraw:
            obtainraw = obtainraw[:obtainraw.find
                                  ("<div class=\"obtain-list-item\">")] + \
                        obtainraw[obtainraw.find
                                  ("<div class=\"obtain-list-item\">")
                                  + 30:]
        # Hardcoded case because Arcarum creates an empty line.
        if "<a href=\"/Arcarum\" title=\"Arcarum\">" in obtainraw:
            obtainraw = obtainraw[:obtainraw.find
                                  ("<a href=\"/Arcarum\" title=\"Arcarum\">")] \
                        + obtainraw[obtainraw.find
                                    ("<a href=\"/Arcarum\" title=\"Arcarum\">")
                                    + 35:]
    # The easy case
    else:
        obtainraw = source[source.find("class=\"obtain-list\">") + 20:] \
            .split("</td>", 1)[0]
    # Find all links
    obtainlinks = [i for i in range(len(obtainraw)) if obtainraw.startswith
                   ("<a href=", i)]
    # Find all display text corresponding to the links
    obtaintext = [i for i in range(len(obtainraw)) if obtainraw.startswith
                  ("\">", i)]
    index = 0
    # Remove images
    while index < len(obtaintext) and obtaintext[index] < len(obtainraw):
        if obtainraw[obtaintext[index] + 2: obtaintext[index] + 6] == "<img":
            del obtainlinks[index]
            del obtaintext[index]
        index += 1
    obtain = ""
    i = 0
    # Generate output string
    while i < len(obtainlinks):
        obtain += ("[" + obtainraw[obtaintext[i] + 2:].split('<', 1)[0] +
                   "](https://gbf.wiki" +
                   obtainraw[obtainlinks[i] + 9:].split('"', 1)[0] + ")\n")
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
