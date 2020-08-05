import discord
from icons import iconreplace
from util import *

BIG = ["Draconic Weapons", "Ultima Weapons", "Dark Opus Weapons"]


async def weaponparse(categories: str, source: str, embed: discord.Embed,
                      simple: bool) -> None:
    parsed = BeautifulSoup(source, 'html.parser')
    # Generate the title of the embed
    embed.title = source[source.find("wgTitle") + 10:].split('"', 1)[0]
    # Generate icon line
    await generateicons(categories, embed)
    # Get description, and change apostrophe escape characters to actual
    # apostrophes
    description = parsed.find("meta", {"name": "description"})["content"] \
        .replace("&#039;", "'")
    # Find weapon image
    image = parsed.find("meta", {"property": "og:image"})["content"]
    # Put the basic content together
    embed.description += description
    embed.set_thumbnail(url=image)
    # Advanced lookup
    if not simple:
        # Generate the obtain field of the embed
        obtain = await generateobtains(parsed)
        # Generate the CA field of the embed
        chargeattack = await generateca(source)
        # Generate the skills field of the embed
        if any(x in categories for x in BIG):
            skills = await generateskills(parsed, True)
        else:
            skills = await generateskills(parsed, False)
        # Put the advanced content together
        embed.add_field(name="Obtain", value=obtain, inline=True)
        embed.add_field(name="Charge Attack: " + chargeattack[0],
                        value=chargeattack[1], inline=True)
        embed.add_field(name="Skills", value=skills, inline=False)


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
    # Assign 4/5★ uncap icons
    if "4★ Weapons" in categories:
        text += " <:BlueStar:739887435936301152>"
    elif "5★ Weapons" in categories:
        text += " <:BlueStar:739887435936301152><:BlueStar:739887435936301152>"
    embed.description = text + "\n"


async def generateobtains(parsed: BeautifulSoup) -> str:
    obtainlinks = []
    obtaintext = []
    obtain = ""
    # The table for obtain information is inconsistently coded. This checks
    # which coding method is being used and cleans the input accordingly.
    if parsed.find_all("div", {"class": "obtain-list-item"}):
        # Thank you BS4 very cool
        obtainraw = parsed.find_all("div", {"class": "obtain-list-item"})
        for entry in obtainraw:
            links = entry.find_all("a")
            obtainlinks.append(links[len(links) - 1]['href'])
            obtaintext.append(links[len(links) - 1].text)
    else:
        obtainraw = parsed.find("td", {"class": "obtain-list"})
        links = obtainraw.find_all("a")
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


async def generateca(source) -> list:
    # Cutting out unneeded bits
    raw = source[source.find("<img alt=\"Skill"):] \
        .split("</tr>", 1)[0]
    # ...Mirage Munitions
    if "None" in raw:
        return ["None", "-"]
    parsed = BeautifulSoup(raw, 'html.parser')
    # Getting the name
    name = parsed.find_all("td", {"class": "skill-name"})[0].text
    # Remove line breaks
    for br in parsed.find_all("br"):
        br.replace_with("\n")
    # Miscellaneous cleaning
    removetooltip(parsed)
    removecitation(parsed)
    iconreplace(parsed)
    for span in parsed.find_all("span", {"class": "skill-upgrade-text"}):
        span.string.replace_with("**" + span.string + "**")
    output = parsed.find_all("td", {"class": ""})[0].text
    return [name, output]


async def generateskills(parsed: BeautifulSoup, big: bool) -> str:
    # Trim to only what's needed
    parsed = parsed.find("table", {"class": "wikitable weapon-skills"})
    output = ""
    # Remove citations
    removecitation(parsed)
    # Generate the output
    for tr in parsed.find_all("tr"):
        # Nothing useful here
        if not tr.get("class"):
            pass
        # Skill information
        elif "skill" in tr["class"]:
            # Modifier type
            if "_a_" in tr.find("img")["src"] or "xeno" in \
                    tr.find("img")["src"]:
                output += "**(EX)** "
            elif "_m_" in tr.find("img")["src"]:
                output += "**(Ω)** "
            elif "job_weapon" in tr.find("img")["src"] or "hollowsky" in \
                    tr.find("img")["src"]:
                output += "**(Special)** "
            else:
                output += "**(N)** "
            # Name/description
            output += tr.find("td", {"class": "skill-name"}).text.strip() + \
                ": " + tr.find("td", {"class": "skill-desc"}).text + "\n"
        # Skill upgrade/unlock information
        elif "skill-upgrade-text" in tr["class"]:
            if "skill-unlock" in tr["class"] and big:
                output += "Remaining skills too large to display. Check the " \
                          "wiki for full details."
            else:
                output += "__" + tr.find_all("td")[1].text + "__\n"
    return output
