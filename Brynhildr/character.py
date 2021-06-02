import discord
import copy
from icons import iconreplace
from util import *

EMP = "Extended Mastery Support Skill"
DOMAIN = "Domain Bonus Ability"


async def characterparse(categories: list, source: str, embed: discord.Embed,
                         simple: bool) -> discord.Embed():
    parsed = BeautifulSoup(source, 'html.parser')
    embed2 = discord.Embed()
    # Generate the title of the embed
    embed.title = source[source.find("wgTitle") + 10:].split('"', 1)[0]
    # Generate icon line
    await generateicons(categories, embed)
    # Get description, and change apostrophe escape characters to actual
    # apostrophe
    if parsed.find("meta", {"name": "description"}):
        description = parsed.find("meta", {"name": "description"})["content"] \
            .replace("&#039;", "'")
    else:
        description = ""
    # Find character image
    image = parsed.find("meta", {"property": "og:image"})["content"]
    # Put the basic content together
    embed.description += description
    embed.set_thumbnail(url=image)
    # Advanced lookup
    if not simple:
        # Generate advanced information
        obtain = await generateobtain(source)
        multiskill = False
        tables = parsed.find_all("table", {"style": "width:100%; "
                                 "text-align:center; text-size-adjust: none;"})
        if len(tables) > 3:
            multiskill = True
        ca = await generateca(tables[0])
        if multiskill:
            skills = await generateskills(tables[1], True)
            skills2 = await generateskills(tables[2], True)
            supskills = await generatesupskills(tables[3])
        else:
            skills = await generateskills(tables[1], False)
            supskills = await generatesupskills(tables[2])
        # Put it together
        embed.add_field(name="How to Recruit", value=obtain, inline=True)
        embed.add_field(name="Charge Attack" + ca[0], value=ca[1], inline=True)
        # See comment in generateskills on how skill generation is handled
        if multiskill:
            embed2 = copy.deepcopy(embed)
            for skill in skills2:
                embed2.add_field(name=skill[0], value=skill[1], inline=False)
        for skill in skills:
            embed.add_field(name=skill[0], value=skill[1], inline=False)
        embed.add_field(name="Support Skills", value=supskills, inline=False)
        if multiskill:
            embed2.add_field(name="Support Skills", value=supskills,
                             inline=False)
            return embed2
        return None


async def generateicons(categories: list, embed: discord.Embed) \
        -> None:
    text = ""
    cat_map = {
        # Rarity icons
        "SSR Characters": " <:Rarity_SSR:730441789667934278>",
        "SR Characters": " <:Rarity_SR:730441789319807009>",
        "R Characters": " <:Rarity_R:730441789642768464>",
        # Element icons
        "Fire Characters": " <:Fire:730845600484032624>",
        "Water Characters": " <:Water:730845600324780151>",
        "Earth Characters": " <:Earth:730845600672776202>",
        "Wind Characters": " <:Wind:730845600479707157>",
        "Light Characters": " <:Light:730845600915914873>",
        "Dark Characters": " <:Dark:730845600613924954>",
        # Category icons
        "Summer Characters": " <:Summer:793505682250661929>",
        "Yukata Characters": " <:Yukata:793506721817034763>",
        "Valentine Characters": " <:Valentine:793507530185768980>",
        "Halloween Premium Draw Characters": " <:Halloween:793508939723309058>",
        "Holiday Premium Draw Characters": " <:Holiday:793509924922720287>",
        "Zodiac Characters": " <:Zodiac:793510822282133565>",
        "Grand Series Characters": " <:Grand:793511553026359316>",
        "Fantasy Characters": " <:Fantasy:793511553134624788>",
        "Collaboration Characters": " <:TieIn:793504971173527582>",
        "The Eternals": " <:Eternals:793503906347876362>",
        "Arcarum Evokers": " <:Evokers:793501266054479913>",
        # Race icons
        "Draph Characters":
            " <:Draph1:731182416441376808><:Draph2:731182416475193464>"
            "<:Draph3:731182416407822376><:Draph4:731182416030466070>",
        "Erune Characters":
            " <:Erune1:731181941662941184><:Erune2:731181942170583060>"
            "<:Erune3:731181941474197505><:Erune4:731181941646426133>",
        "Harvin Characters":
            " <:Harvin1:731177969992859844><:Harvin2:731177970177278023>"
            "<:Harvin3:731177970416353280><:Harvin4:731177970353569854>",
        "Human Characters":
            " <:Human1:731174811774091304><:Human2:731174811518238822>"
            "<:Human3:731174811648262155><:Human4:731174811857977384>",
        "Other Characters":
            " <:Unknown1:731183072850083942><:Unknown2:731183073026375811>"
            "<:Unknown3:731183073101742110><:Unknown4:731183072862666813>",
        "Primal Characters":
            " <:Primal1:731173612035244052><:Primal2:731173611918065684>"
            "<:Primal3:731173290848157696><:Primal4:731173290806214736>",
        # Weapon proficiency icons
        "Sabre Characters":
            " <:Sabre1:730454365248159855><:Sabre2:730454663941324861>",
        "Dagger Characters":
            " <:Dagger1:730455370233020558><:Dagger2:730455370673291314>",
        "Spear Characters":
            " <:Spear1:730456104898920458><:Spear2:730456104840200363>",
        "Axe Characters":
            " <:Axe1:730456397942095943><:Axe2:730456397556482110>",
        "Staff Characters":
            " <:Staff1:730456836221829173><:Staff2:730456836310040677>",
        "Gun Characters":
            " <:Gun1:730457164552077382><:Gun2:730457164266864784>",
        "Melee Characters":
            " <:Melee1:730457549672939621><:Melee2:730457549337264139>",
        "Bow Characters":
            " <:Bow1:730457814627254322><:Bow2:730457814551756840>",
        "Harp Characters":
            " <:Harp1:730458095591096420><:Harp2:730458095221997580>",
        "Katana Characters":
            " <:Katana1:730458503742750822><:Katana2:730458504011317319>",
        # 5★ uncap icons
        "5★ Characters": " <:BlueStar:739887435936301152>",
    }

    for cat in categories:
        if cat in cat_map.keys():
            text += cat_map[cat]
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


# I have no idea what the hell the BS4 search result for a table is so I'm just
# not going to define the parameter type, please don't break it
async def generateca(source) -> list:
    # Empty variables to be filled later
    name = ""
    output = []
    outputtext = ""
    # Miscellaneous cleaning
    removetooltip(source)
    removecitation(source)
    iconreplace(source)
    # Check if the CA eventually gets another name
    if len(source.find_all("td", {"class": "skill-name"})) > 1:
        namechange = True
    else:
        namechange = False
    for tr in source.find_all("tr"):
        # If the row has styling, it's a dud row
        if tr.find("th") is not None:
            continue
        # If the row has a "skill" upgrade, add it in mark it as such, then
        # Remove it to prevent double inclusion
        if tr.find("td", {"class": "skill-name"}) and not namechange:
            name = " - " + tr.find("td", {"class": "skill-name"}).text
            tr.find("td", {"class": "skill-name"}).replace_with("")
        if tr.find("span", {"class": "skill-upgrade-text"}):
            if namechange:
                outputtext += "__" + tr.find("span", {"class":
                                             "skill-upgrade-text"}).text + \
                              "__\n"
                tr.find("span", {"class": "skill-upgrade-text"})\
                    .replace_with("")
            else:
                tr.find("span", {"class": "skill-upgrade-text"}) \
                    .replace_with("\n__" + tr.find("span", {"class":
                                  "skill-upgrade-text"}).text + "__\n")
        td = tr.find("td", {"style": "text-align:left;"})
        for br in td.find_all("br"):
            br.replace_with(" ")
        if namechange:
            outputtext += "**" + tr.find("td", {"class": "skill-name"}).text + \
                      ":** " + td.text + "\n"
        else:
            outputtext += td.text

    output.append(name)
    output.append(outputtext)
    return output


async def generateskills(source, multiskill: bool) -> list:
    # Skills are too big to put in one field, so this generates the information
    # for each skill to be displayed in its own field.
    output = []
    # Miscellaneous cleaning
    removetooltip(source)
    removecitation(source)
    iconreplace(source)
    # Skill counter and text buffer for the skill info
    i = 1
    skillinfo = ""
    for tr in source.find_all("tr"):
        if tr.find_all("th") or tr.get("class"):
            if multiskill and tr.find("th", {"colspan": "6"}):
                output.append((tr.find("th", {"colspan": "6"}).text, "Press "
                              "the :arrows_counterclockwise: reaction to see "
                               "this character's other skills"))
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


async def generatesupskills(source) -> str:
    output = ""
    removetooltip(source)
    removecitation(source)
    iconreplace(source)
    for tr in source.find_all("tr"):
        if tr.find_all("th"):
            continue
        if tr.get("class"):
            continue
        output += "**" + tr.find("td", {"class": "skill-name"}).text.strip() + \
                  "**\n"
        # I don't know why this check is actually needed but it doesn't work
        # without it
        if EMP or DOMAIN in tr.find("td", {"class": "skill-name"}).text:
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
