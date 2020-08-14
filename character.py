import discord
from icons import iconreplace
from util import *


async def characterparse(categories: str, source: str, embed: discord.Embed,
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
    # Find character image
    image = parsed.find("meta", {"property": "og:image"})["content"]
    # Put the basic content together
    embed.description += description
    embed.set_thumbnail(url=image)
    # Advanced lookup
    if not simple:
        # Generate advanced information
        obtain = await generateobtain(source)
        ca = await generateca(source)
        skills = await generateskills(source)
        supskills = await generatesupskills(source)
        # Put it together
        embed.add_field(name="How to Recruit", value=obtain, inline=True)
        embed.add_field(name="Charge Attack" + ca[0], value=ca[1], inline=True)
        # See comment in generateskills
        for skill in skills:
            embed.add_field(name=skill[0], value=skill[1], inline=False)
        embed.add_field(name="Support Skills", value=supskills, inline=False)


async def generateicons(categories: str, embed: discord.Embed) \
        -> None:
    text = ""
    # Assign rarity icons
    if "SSR Characters" in categories:
        text += " <:Rarity_SSR:730441789667934278>"
    elif "SR Characters" in categories:
        text += " <:Rarity_SR:730441789319807009>"
    elif "R Characters" in categories:
        text += " <:Rarity_R:730441789642768464>"
    # Assign element icons
    if "Fire Characters" in categories:
        text += " <:Fire:730845600484032624>"
    elif "Water Characters" in categories:
        text += " <:Water:730845600324780151>"
    elif "Earth Characters" in categories:
        text += " <:Earth:730845600672776202>"
    elif "Wind Characters" in categories:
        text += " <:Wind:730845600479707157>"
    elif "Light Characters" in categories:
        text += " <:Light:730845600915914873>"
    elif "Dark Characters" in categories:
        text += " <:Dark:730845600613924954>"
    # Assign race icons. Check each race, as multirace options (unfortunately)
    # exist
    if "Draph Characters" in categories:
        text += " <:Draph1:731182416441376808><:Draph2:731182416475193464>" \
                "<:Draph3:731182416407822376><:Draph4:731182416030466070>"
    if "Erune Characters" in categories:
        text += " <:Erune1:731181941662941184><:Erune2:731181942170583060>" \
                "<:Erune3:731181941474197505><:Erune4:731181941646426133>"
    if "Harvin Characters" in categories:
        text += " <:Harvin1:731177969992859844><:Harvin2:731177970177278023>" \
                "<:Harvin3:731177970416353280><:Harvin4:731177970353569854>"
    if "Human Characters" in categories:
        text += " <:Human1:731174811774091304><:Human2:731174811518238822>" \
                "<:Human3:731174811648262155><:Human4:731174811857977384>"
    if "Other Characters" in categories:
        text += " <:Unknown1:731183072850083942>" \
                "<:Unknown2:731183073026375811><:Unknown3:731183073101742110>" \
                "<:Unknown4:731183072862666813>"
    if "Primal Characters" in categories:
        text += " <:Primal1:731173612035244052><:Primal2:731173611918065684>" \
                "<:Primal3:731173290848157696><:Primal4:731173290806214736>"
    # Assign weapon proficiency icons. Check each type, as some characters
    # (unfortunately) have multiple proficiencies
    if "Sabre Characters" in categories:
        text += " <:Sabre1:730454365248159855><:Sabre2:730454663941324861>"
    if "Dagger Characters" in categories:
        text += " <:Dagger1:730455370233020558><:Dagger2:730455370673291314>"
    if "Spear Characters" in categories:
        text += " <:Spear1:730456104898920458><:Spear2:730456104840200363>"
    if "Axe Characters" in categories:
        text += " <:Axe1:730456397942095943><:Axe2:730456397556482110>"
    if "Staff Characters" in categories:
        text += " <:Staff1:730456836221829173><:Staff2:730456836310040677>"
    if "Gun Characters" in categories:
        text += " <:Gun1:730457164552077382><:Gun2:730457164266864784>"
    if "Melee Characters" in categories:
        text += " <:Melee1:730457549672939621><:Melee2:730457549337264139>"
    if "Bow Characters" in categories:
        text += " <:Bow1:730457814627254322><:Bow2:730457814551756840>"
    if "Harp Characters" in categories:
        text += " <:Harp1:730458095591096420><:Harp2:730458095221997580>"
    if "Katana Characters" in categories:
        text += " <:Katana1:730458503742750822><:Katana2:730458504011317319>"
    # Assign 5★ uncap icons
    if "5★ Characters" in categories:
        text += " <:BlueStar:739887435936301152>"
    embed.description = text + "\n"


async def generateobtain(source: str) -> str:
    # Trim
    raw = source[source.find("How to Recruit") + 14:].split("</tbody>", 1)[0]
    parsed = BeautifulSoup(raw, 'html.parser')
    # Get information and put it together
    link = parsed.find("a")["href"]
    text = parsed.find("a").text
    obtain = "[" + text + "](https://gbf.wiki" + link + ")"
    # If the character is obtained via a recruitment weapon, get that too.
    if "Recruitment Weapon" in parsed.text:
        recruit = parsed.find("span", {"class": "image_link"})
        link = recruit.find("a")["href"]
        text = recruit.text.strip()
        obtain += "\n**Recruitment Weapon**\n[" + text + "](https://gbf.wiki" \
                  + link + ")"
    return obtain


async def generateca(source: str) -> list:
    # Empty variables to be filled later
    name = ""
    output = []
    outputtext = ""
    # Trim the source
    raw = source[source.find("/Charge_Attack"):].split("</tbody>", 1)[0]
    parsed = BeautifulSoup(raw, 'html.parser')
    # Miscellaneous cleaning
    removetooltip(parsed)
    removecitation(parsed)
    iconreplace(parsed)
    # Check if the CA eventually gets an upgrade
    if not parsed.find_all("span", {"class": "skill-upgrade-text"}):
        upgrade = False
    else:
        upgrade = True
    for tr in parsed.find_all("tr"):
        # If the row has styling, it's a dud row
        if tr.get("style"):
            continue
        if not upgrade:
            # If the CA doesn't get an upgrade, the CA name will be listed on
            # the field title
            name = " - " + tr.find("td", {"class": "skill-name"}).text
            td = tr.find("td", {"style": "text-align:left;"})
            for br in td.find_all("br"):
                br.replace_with(" ")
            outputtext = td.text
        else:
            # If the row has a "skill" upgrade, add it in mark it as such, then
            # Remove it to prevent double inclusion
            if tr.find("span", {"class": "skill-upgrade-text"}):
                outputtext += "__" + \
                              tr.find("span", {"class": "skill-upgrade-text"})\
                                  .text + "__\n"
                tr.find("span", {"class": "skill-upgrade-text"})\
                    .replace_with("")
            # Otherwise, the CA name is listed in the field body.
            td = tr.find("td", {"style": "text-align:left;"})
            for br in td.find_all("br"):
                br.replace_with(" ")
            outputtext += "**" + tr.find("td", {"class": "skill-name"}).text + \
                          ":** " + td.text + "\n"
    output.append(name)
    output.append(outputtext)
    return output


async def generateskills(source) -> list:
    # Skills are too big to put in one field, so this generates the information
    # for each skill to be displayed in its own field.
    output = []
    # Trim to what's needed
    raw = source[source.find("<span class=\"mw-headline\" id=\"Skills\">"):]\
        .split("</tbody>", 1)[0]
    parsed = BeautifulSoup(raw, "html.parser")
    parsed = parsed.find("table")
    # Miscellaneous cleaning
    removetooltip(parsed)
    removecitation(parsed)
    iconreplace(parsed)
    # Skill counter and text buffer for the skill info
    i = 1
    skillinfo = ""
    for tr in parsed.find_all("tr"):
        if tr.find_all("th"):
            continue
        if tr.get("class"):
            continue
        # Get the cell with the skill name
        td = tr.find("td", {"class": "skill-name"})
        # Handle any skill name changes
        for span in td.find_all("span", {"class": "skill-upgrade-text"}):
            for br in span.find_all("br"):
                br.replace_with(" ")
            span.replace_with("/" + span.text)
        skillname = "Skill " + str(i) + ": " + td.text.strip()
        # The next three cells don't have a class identifier, so you just have
        # to hope the table format stays consistent with all cases
        td = tr.find_all("td", {"class": None})
        # The first unmarked cell is for the cooldown, which needs handling of
        # potential cooldown reductions and linked skills
        for span in td[0].find_all("span"):
            if "Linked" not in span.text:
                span.replace_with("/" + span.text + " ")
            else:
                span.replace_with("(Linked Skill) ")
        skillinfo += "Cooldown: " + td[0].text + "\n"
        # The second unmarked cell is for the duration, which needs handling of
        # potential upgrades
        for span in td[1].find_all("span"):
            span.replace_with("/" + span.text + " ")
        skillinfo += "Duration: " + td[1].text + "\n"
        for span in td[2].find_all("span"):
            span.replace_with("/" + span.text)
        # The third unmarked cell is for the obtain level, which also includes
        # potential upgrades
        skillinfo += "Obtained: " + td[2].text + "\n"
        # The cell with skill information apparently doesn't have an identifier,
        # but it DOES always have a specific styling.
        td = tr.find("td", {"style": "text-align:left;"})
        for br in td.find_all("br"):
            br.replace_with(" ")
        for span in td.find_all("span", {"class": "skill-upgrade-text"}):
            span.replace_with("\n__" + span.text + "__")
        skillinfo += td.text + "\n"
        output.append((skillname, skillinfo))
        skillinfo = ""
        i += 1
    return output


async def generatesupskills(source: str) -> str:
    output = ""
    raw = source[source.find
                 ("<span class=\"mw-headline\" id=\"Support_Skills\">"):] \
        .split("</tbody>", 1)[0]
    parsed = BeautifulSoup(raw, "html.parser")
    parsed = parsed.find("table")
    removetooltip(parsed)
    removecitation(parsed)
    iconreplace(parsed)
    for tr in parsed.find_all("tr"):
        if tr.find_all("th"):
            continue
        if tr.get("class"):
            continue
        output += "**" + tr.find("td", {"class": "skill-name"}).text.strip() + \
                  "**\n"
        if "Extended" in tr.find("td", {"class": "skill-name"}).text:
            td = tr.find_all("td", {"style": ""})[1]
        else:
            td = tr.find_all("td", {"style": ""})[2]
        for span in td.find_all("span", {"class": "tooltip"}):
            span.replace_with("/" + span.text)
        output += "Obtained: " + td.text.strip() + "\n"
        td = tr.find("td", {"style": "text-align:left;"})
        for span in td.find_all("span", {"class": "skill-upgrade-text"}):
            span.replace_with("\n__" + span.text + "__")
        for br in td.find_all("br"):
            br.replace_with(" ")
        output += td.text + "\n"
    return output
