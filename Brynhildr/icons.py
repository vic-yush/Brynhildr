from bs4 import BeautifulSoup


def iconreplace(parsed: BeautifulSoup) -> None:
    """
    Replaces all icon tags in the given parsed HTML code with their respective
    icons in emote form. I wish there was a better way to do this.

    :param parsed: Parsed HTML code
    :return: None, the parsed code is directly modified
    """
    # BUFFS

    # Charge bar effects
    for img in parsed.find_all("img", {"alt": "Status Uplift.png"}):
        img.replace_with("<:ChargeBar:730532683364434092>")
    # Revitalize
    for img in parsed.find_all("img", {"alt": "Status Revitalize.png"}):
        img.replace_with("<:Revitalize:739609067185504318>")
    # Supplemental damage (The purple spiky circle)
    for img in parsed.find_all("img", {"alt": "Status DmgUp.png"}):
        img.replace_with("<:DmgUp:739971047247315025>")
    # Triple Attack up
    for img in parsed.find_all("img", {"alt": "Status TripleUp.png"}):
        img.replace_with("<:TripleUp:730824577508442132>")

    # Crests
    # Typhoon, which apparently has two different alt texts
    for img in parsed.find_all("img", {"alt": "Status Typhoon Crest 1.png"}):
        img.replace_with("<:Typhoon:740327164385427557>")
    for img in parsed.find_all("img", {"alt": "Status Typhoon Crest.png"}):
        img.replace_with("<:Typhoon:740327164385427557>")

    # DEBUFFS

    # Blind
    for img in parsed.find_all("img", {"alt": "Status Blind.png"}):
        img.replace_with("<:Blind:740638272321093754>")
