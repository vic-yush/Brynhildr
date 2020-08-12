from bs4 import BeautifulSoup


def iconreplace(parsed: BeautifulSoup) -> None:
    """
    Replaces all icon tags in the given parsed HTML code with their respective
    icons in emote form. I wish there was a better way to do this.

    :param parsed: Parsed HTML code in the form of a BeautifulSoup object
    :return: None, the BeautifulSoup object is directly modified
    """

    for img in parsed.find_all("img"):
        # BUFFS

        # Attack up
        if img["alt"] == "Status AttackUp.png":
            img.replace_with("<:AttackUp:730824577651048539>")
        # Bonus damage
        elif img["alt"] == "Status Bonus Damage.png":
            img.replace_with("<:BonusDamage:741033069724696677>")
        # Charge bar effects
        elif img["alt"] == "Status Uplift.png":
            img.replace_with("<:ChargeBar:730532683364434092>")
        # Critical up (Water)
        elif img["alt"] == "Status CriticalUpWater.png":
            img.replace_with("<:CriticalUpWater:741028610433089698>")
        # Defense up
        elif img["alt"] == "Status DefenseUp.png":
            img.replace_with("<:DefenseUp:730824577478950933>")
        # Double attack up
        elif img["alt"] == "Status DoubleUp.png":
            img.replace_with("<:DoubleUp:730824577487208468>")
        # Heal effects (includes Refresh)
        elif img["alt"] == "Status Heal.png":
            img.replace_with("<:Heal:741030651544862782>")
        # Keen
        elif img["alt"] == "Status Heal.png":
            img.replace_with("<:Keen:741022857177595997>")
        # Mirror Image
        elif img["alt"] == "Status Mirror Image.png":
            img.replace_with("<:MirrorImage:741033069582090402>")
        # Repel (also Unchallenged)
        elif img["alt"] == "Status Repel.png":
            img.replace_with("<:Repel:741031304895791156>")
        # Revitalize
        elif img["alt"] == "Status Revitalize.png":
            img.replace_with("<:Revitalize:739609067185504318>")
        # Shield
        elif img["alt"] == "Status Shield.png":
            img.replace_with("<:Shield:741019009427963907>")
        # Strength
        elif img["alt"] == "Status Strength.png":
            img.replace_with("<:Strength:740988555894980708>")
        # Substitute
        elif img["alt"] == "Status Substitute.png":
            img.replace_with("<:Substitute:741009875127238676>")
        # Supplemental damage (The purple spiky circle)
        elif img["alt"] == "Status DmgUp.png":
            img.replace_with("<:DmgUp:739971047247315025>")
        # Triple Attack up
        elif img["alt"] == "Status TripleUp.png":
            img.replace_with("<:TripleUp:730824577508442132>")
        # Veil
        elif img["alt"] == "Status Veil.png":
            img.replace_with("<:Veil:741033069548404819>")

        # Elemental ATK up
        # Water
        elif img["alt"] == "Status WaterAtkUp.png":
            img.replace_with("<:WaterAtkUp:741720282640678963>")
        # Light
        elif img["alt"] == "Status LightAtkUp.png":
            img.replace_with("<:LightAtkUp:741720282120847364>")

        # Crests
        # Deluge
        elif img["alt"] == "Status Deluge Crest 1.png":
            img.replace_with("<:Deluge:740327164364324904>")
        elif img["alt"] == "Status Deluge Crest.png":
            img.replace_with("<:Deluge:740327164364324904>")
        # Hellfire
        elif img["alt"] == "Status Hellfire Crest 1.png":
            img.replace_with("<:Hellfire:740327164544811038>")
        elif img["alt"] == "Status Hellfire Crest.png":
            img.replace_with("<:Hellfire:740327164544811038>")
        # Typhoon
        elif img["alt"] == "Status Typhoon Crest 1.png":
            img.replace_with("<:Typhoon:740327164385427557>")
        elif img["alt"] == "Status Typhoon Crest.png":
            img.replace_with("<:Typhoon:740327164385427557>")

        # Damage cuts
        # Fire (70%)
        elif img["alt"] == "Status Fire Cut 70.png":
            img.replace_with("<:FC70:730877406604296213>")

        # DEBUFFS

        # Acccuracy lowered (3 turn)
        elif img["alt"] == "Status Accuracy Lowered 3.png":
            img.replace_with("<:AccuracyLowered3:741718281291038838>")
        # Acccuracy lowered (6 turn)
        elif img["alt"] == "Status Accuracy Lowered 6.png":
            img.replace_with("<:AccuracyLowered6:741037392391045161>")
        # Attack down
        elif img["alt"] == "Status AttackDown.png":
            img.replace_with("<:AttackDown:741034514817745006>")
        # Blind
        elif img["alt"] == "Status Blind.png":
            img.replace_with("<:Blind:741033217880096820>")
        # Burned
        elif img["alt"] == "Status Burned.png":
            img.replace_with("<:Burned:741708251254489129>")
        # Defense down
        elif img["alt"] == "Status DefenseDown.png":
            img.replace_with("<:DefenseDown:740984047274033173>")
        # Defense down (3 turn)
        elif img["alt"] == "Status DEF Down 3.png":
            img.replace_with("<:DefenseDown3:741033218014314586>")
        # Double Attack down (6 turn)
        elif img["alt"] == "Status DA Down 6.png":
            img.replace_with("<:DoubleDown6:741037392378462269>")
        # Gravity
        elif img["alt"] == "Status Gravity.png":
            img.replace_with("<:Gravity:740984450841575477>")
        elif img["alt"] == "Status HealDown.png":
            img.replace_with("<:HealDown:741718732954402838>")
        # Petrified
        elif img["alt"] == "Status Petrified.png":
            img.replace_with("<:Petrified:740988150616424581>")
        # Petrified (3 turn)
        elif img["alt"] == "Status Petrified 3.png":
            img.replace_with("<:Petrified3:741033218022572062>")
        # Sleep
        elif img["alt"] == "Status Sleep.png":
            img.replace_with("<:Sleep:741038697323036673>")
        # Triple Attack down (6 turn)
        elif img["alt"] == "Status TA Down 6.png":
            img.replace_with("<:TripleDown6:741037392437182524>")
