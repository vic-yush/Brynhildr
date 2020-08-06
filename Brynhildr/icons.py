from bs4 import BeautifulSoup


def iconreplace(parsed: BeautifulSoup) -> None:
    """
    Replaces all icon tags in the given parsed HTML code with their respective
    icons in emote form. I wish there was a better way to do this.

    :param parsed: Parsed HTML code in the form of a BeautifulSoup object
    :return: None, the BeautifulSoup object is directly modified
    """
    # BUFFS

    # Attack up
    for img in parsed.find_all("img", {"alt": "Status AttackUp.png"}):
        img.replace_with("<:AttackUp:730824577651048539>")
    # Bonus damage
    for img in parsed.find_all("img", {"alt": "Status Bonus Damage.png"}):
        img.replace_with("<:BonusDamage:741033069724696677>")
    # Charge bar effects
    for img in parsed.find_all("img", {"alt": "Status Uplift.png"}):
        img.replace_with("<:ChargeBar:730532683364434092>")
    # Critical up (Water)
    for img in parsed.find_all("img", {"alt": "Status CriticalUpWater.png"}):
        img.replace_with("<:CriticalUpWater:741028610433089698>")
    # Defense up
    for img in parsed.find_all("img", {"alt": "Status DefenseUp.png"}):
        img.replace_with("<:DefenseUp:730824577478950933>")
    # Double attack up
    for img in parsed.find_all("img", {"alt": "Status DoubleUp.png"}):
        img.replace_with("<:DoubleUp:730824577487208468>")
    # Heal effects (includes Refresh)
    for img in parsed.find_all("img", {"alt": "Status Heal.png"}):
        img.replace_with("<:Heal:741030651544862782>")
    # Keen
    for img in parsed.find_all("img", {"alt": "Status Keen.png"}):
        img.replace_with("<:Keen:741022857177595997>")
    # Mirror Image
    for img in parsed.find_all("img", {"alt": "Status Mirror Image.png"}):
        img.replace_with("<:MirrorImage:741033069582090402>")
    # Repel (also Unchallenged)
    for img in parsed.find_all("img", {"alt": "Status Repel.png"}):
        img.replace_with("<:Repel:741031304895791156>")
    # Revitalize
    for img in parsed.find_all("img", {"alt": "Status Revitalize.png"}):
        img.replace_with("<:Revitalize:739609067185504318>")
    # Shield
    for img in parsed.find_all("img", {"alt": "Status Shield.png"}):
        img.replace_with("<:Shield:741019009427963907>")
    # Strength
    for img in parsed.find_all("img", {"alt": "Status Strength.png"}):
        img.replace_with("<:Strength:740988555894980708>")
    # Substitute
    for img in parsed.find_all("img", {"alt": "Status Substitute.png"}):
        img.replace_with("<:Substitute:741009875127238676>")
    # Supplemental damage (The purple spiky circle)
    for img in parsed.find_all("img", {"alt": "Status DmgUp.png"}):
        img.replace_with("<:DmgUp:739971047247315025>")
    # Triple Attack up
    for img in parsed.find_all("img", {"alt": "Status TripleUp.png"}):
        img.replace_with("<:TripleUp:730824577508442132>")
    # Veil
    for img in parsed.find_all("img", {"alt": "Status Veil.png"}):
        img.replace_with("<:Veil:741033069548404819>")

    # Crests
    # Deluge
    for img in parsed.find_all("img", {"alt": "Status Deluge Crest 1.png"}):
        img.replace_with("<:Deluge:740327164364324904>")
    for img in parsed.find_all("img", {"alt": "Status Deluge Crest.png"}):
        img.replace_with("<:Deluge:740327164364324904>")
    # Hellfire
    for img in parsed.find_all("img", {"alt": "Status Hellfire Crest 1.png"}):
        img.replace_with("<:Hellfire:740327164544811038>")
    for img in parsed.find_all("img", {"alt": "Status Hellfire Crest.png"}):
        img.replace_with("<:Hellfire:740327164544811038>")
    # Typhoon
    for img in parsed.find_all("img", {"alt": "Status Typhoon Crest 1.png"}):
        img.replace_with("<:Typhoon:740327164385427557>")
    for img in parsed.find_all("img", {"alt": "Status Typhoon Crest.png"}):
        img.replace_with("<:Typhoon:740327164385427557>")

    # DEBUFFS

    # Attack down
    for img in parsed.find_all("img", {"alt": "Status AttackDown.png"}):
        img.replace_with("<:AttackDown:741034514817745006>")
    # Blind
    for img in parsed.find_all("img", {"alt": "Status Blind.png"}):
        img.replace_with("<:Blind:741033217880096820>")
    # Burned
    for img in parsed.find_all("img", {"alt": "Status Burned.png"}):
        img.replace_with("<:Burned:740989538821734470>")
    # Defense down
    for img in parsed.find_all("img", {"alt": "Status DefenseDown.png"}):
        img.replace_with("<:DefenseDown:740984047274033173>")
    # Defense down (3 turn)
    for img in parsed.find_all("img", {"alt": "Status DEF Down 3.png"}):
        img.replace_with("<:DefenseDown3:741033218014314586>")
    # Gravity
    for img in parsed.find_all("img", {"alt": "Status Gravity.png"}):
        img.replace_with("<:Gravity:740984450841575477>")
    # Petrified
    for img in parsed.find_all("img", {"alt": "Status Petrified.png"}):
        img.replace_with("<:Petrified:740988150616424581>")
    # Petrified (3 turn)
    for img in parsed.find_all("img", {"alt": "Status Petrified 3.png"}):
        img.replace_with("<:Petrified3:741033218022572062>")
