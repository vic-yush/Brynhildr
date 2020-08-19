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

        # "Adversity" (damage amplified)
        if img["alt"] == "Status Adversity.png":
            img.replace_with("<:Adversity:744355101417799796>")
        # Armoured
        elif img["alt"] == "Status Armored.png":
            img.replace_with("<:Armored:730830371058614282>")
        # Attack up
        elif img["alt"] == "Status AttackUp.png":
            img.replace_with("<:AttackUp:730824577651048539>")
        # Attack up (stackable)
        elif img["alt"] == "Status AttackUpStack.png":
            img.replace_with("<:AttackUpStack:730830371045900320>")
        # Autorevive
        elif img["alt"] == "Status AutoRevive.png":
            img.replace_with("<:AutoRevive:730830370886385705>")
        # Bonus damage
        elif img["alt"] == "Status Bonus Damage.png":
            img.replace_with("<:BonusDamage:741033069724696677>")
        # Chain burst damage cap up
        elif img["alt"] == "Status CB DMG Cap Up.png":
            img.replace_with("<:CBCap:730830370919940106>")
        # Charge attack damage cap up
        elif img["alt"] == "Status CA DMG Cap.png":
            img.replace_with("<:CACap:730830370798436353>")
        # Charge attack damage up (1 time)
        elif img["alt"] == "Status C.A. DMG Boosted (1 time).png":
            img.replace_with("<:CAUp1:744316047510994964>")
        # Charge bar effects
        elif img["alt"] == "Status Uplift.png":
            img.replace_with("<:ChargeBar:730532683364434092>")
        # Counter on dodge
        elif img["alt"] == "Status Counter.png":
            img.replace_with("<:Counter:730830629737988186>")
        # Counter on dodge/damage
        elif img["alt"] == "Status Counter DodgeDMG.png":
            img.replace_with("<:CounterDodgeDMG:745326045393059850>")
        # Damage cap up
        elif img["alt"] == "Status DamageCapUp.png":
            img.replace_with("<:CapUp:730836378702839878>")
        # Debuff success up
        elif img["alt"] == "Status DebuffSuccessUp.png":
            img.replace_with("<:DebuffUp:730836378287603784>")
        # Defense up
        elif img["alt"] == "Status DefenseUp.png":
            img.replace_with("<:DefenseUp:730824577478950933>")
        # Defense up (stackable)
        elif img["alt"] == "Status DefenseUpStack.png":
            img.replace_with("<:DefenseUpStack:745336776817639465>")
        # "Defiance" (Azir)
        elif img["alt"] == "Status Defiance.png":
            img.replace_with("<:Azir:730830371049963681>")
        # Dispel cancel
        elif img["alt"] == "Status Dispel Cancel.png":
            img.replace_with("<:DispelCancel:730836378367164560>")
        # Dodge
        elif img["alt"] == "Status Dodge.png":
            img.replace_with("<:Dodge:730836378656571474>")
        # Dodge all (1 time)
        elif img["alt"] == "Status Dodge 1.png":
            img.replace_with("<:Dodge1:744752642626158642>")
        # Double attack up
        elif img["alt"] == "Status DoubleUp.png":
            img.replace_with("<:DoubleUp:730824577487208468>")
        # Double attack up
        elif img["alt"] == "Status Drain.png":
            img.replace_with("<:Drain:730836378685800538>")
        # Effect on dodge
        elif img["alt"] == "Status EffectOnDodge.png":
            img.replace_with("<:EffectOnDodge:744385082663370832>")
        # Heal effects (includes Refresh)
        elif img["alt"] == "Status Heal.png":
            img.replace_with("<:Heal:741030651544862782>")
        # Hype (1 stack)
        elif img["alt"] == "Status Hype1.png":
            img.replace_with("<:Hype1:744385939924844596>")
        # Jammed
        elif img["alt"] == "Status Jammed.png":
            img.replace_with("<:Jammed:744303000516034742>")
        # Keen
        elif img["alt"] == "Status Keen.png":
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
        # Routine Step (multistrike)
        elif img["alt"] == "Status Routine Step.png":
            img.replace_with("<:MultiStrike:730830371075260557>")
        # Shield
        elif img["alt"] == "Status Shield.png":
            img.replace_with("<:Shield:741019009427963907>")
        # Skill damage up
        elif img["alt"] == "Status SkillUp.png":
            img.replace_with("<:SkillUp:744989088507232456>")
        # Skill damage cap up
        elif img["alt"] == "Status Skill DMG Cap Up.png":
            img.replace_with("<:SkillDMGCapUp:744396609768652981>")
        # Skill damage cap up (stackable)
        elif img["alt"] == "Status Skill DMG Cap Up Stack.png":
            img.replace_with("<:SkillDMGCapUpStack:744379777321926707>")
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
        # Wasteland
        elif img["alt"] == "Status Wasteland Crest 1.png":
            img.replace_with("<:Wasteland:740327164389621830>")
        elif img["alt"] == "Status Wasteland Crest.png":
            img.replace_with("<:Wasteland:740327164389621830>")

        # Critical up
        elif img["alt"] == "Status CriticalUp.png":
            img.replace_with("<:CriticalUp:741028610697068584>")
        # Critical up (Dark)
        elif img["alt"] == "Status CriticalUpDark.png":
            img.replace_with("<:CriticalUpDark:741028610432958654>")
        # Critical up (Water)
        elif img["alt"] == "Status CriticalUpWater.png":
            img.replace_with("<:CriticalUpWater:741028610433089698>")

        # Damage cuts
        # 50%
        elif img["alt"] == "Status Dmg Cut 50.png":
            img.replace_with("<:DC50:730870761178529862>")
        # Fire (70%)
        elif img["alt"] == "Status Fire Cut 70.png":
            img.replace_with("<:FC70:730877406604296213>")
        # Water (20%)
        elif img["alt"] == "Status Water Cut 20.png":
            img.replace_with("<:WC20:730879492721213500>")
        # Wind (40%)
        elif img["alt"] == "Status Wind Cut 40.png":
            img.replace_with("<:GC40:730884667007434793>")

        # Element Switches
        # Wind
        elif img["alt"] == "Status Wind Switch.png":
            img.replace_with("<:WindSwitch:743648516538105906>")

        # Elemental ATK up
        # Dark
        elif img["alt"] == "Status DarkAtkUp.png":
            img.replace_with("<:DarkAtkUp:741720281751748660>")
        # Earth
        elif img["alt"] == "Status EarthAtkUp.png":
            img.replace_with("<:EarthAtkUp:741720282384826438>")
        # Fire
        elif img["alt"] == "Status FireAtkUp.png":
            img.replace_with("<:FireAtkUp:741720282414186526>")
        # Light
        elif img["alt"] == "Status LightAtkUp.png":
            img.replace_with("<:LightAtkUp:741720282120847364>")
        # Water
        elif img["alt"] == "Status WaterAtkUp.png":
            img.replace_with("<:WaterAtkUp:741720282640678963>")
        # Wind
        elif img["alt"] == "Status WindAtkUp.png":
            img.replace_with("<:WindAtkUp:741720282472906874>")

        # Elemental DEF up
        # Dark
        elif img["alt"] == "Status DarkResUp.png":
            img.replace_with("<:DarkResUp:730840334363525130>")
        # Fire
        elif img["alt"] == "Status FireResUp.png":
            img.replace_with("<:FireResUp:730840334401142874>")

        # DEBUFFS

        # Acccuracy lowered (2 turn)
        elif img["alt"] == "Status Accuracy Lowered 2.png":
            img.replace_with("<:AccuracyLowered2:745330950006636626>")
        # Acccuracy lowered (3 turn)
        elif img["alt"] == "Status Accuracy Lowered 3.png":
            img.replace_with("<:AccuracyLowered3:741718281291038838>")
        # Acccuracy lowered (6 turn)
        elif img["alt"] == "Status Accuracy Lowered 6.png":
            img.replace_with("<:AccuracyLowered6:741037392391045161>")
        # Attack down
        elif img["alt"] == "Status AttackDown.png":
            img.replace_with("<:AttackDown:741034514817745006>")
        # Attack down (4 turn)
        elif img["alt"] == "Status ATK Down 4.png":
            img.replace_with("<:ATKDown4:745395152939647107>")
        # Attack down (stackable)
        elif img["alt"] == "Status AttackDownStack.png":
            img.replace_with("<:AttackDownStack:743649616985063424>")
        # Blind
        elif img["alt"] == "Status Blind.png":
            img.replace_with("<:Blind:741033217880096820>")
        # Burned
        elif img["alt"] == "Status Burned.png":
            img.replace_with("<:Burned:741708251254489129>")
        # Charmed
        elif img["alt"] == "Status Charm.png":
            img.replace_with("<:Charm:744300407915806801>")
        # Charmed (3 turn)
        elif img["alt"] == "Status Charm 3.png":
            img.replace_with("<:Charm3:744388963053076611>")
        # Debuff resistance down
        elif img["alt"] == "Status DebuffResDown.png":
            img.replace_with("<:DebuffResDown:744752535361028176>")
        # Defense down
        elif img["alt"] == "Status DefenseDown.png":
            img.replace_with("<:DefenseDown:740984047274033173>")
        # Defense down (3 turn)
        elif img["alt"] == "Status DEF Down 3.png":
            img.replace_with("<:DefenseDown3:741033218014314586>")
        # Defense down (4 turn)
        elif img["alt"] == "Status DEF Down 4.png":
            img.replace_with("<:DEFDown4:745395152759160903>")
        # Defense down (stackable)
        elif img["alt"] == "Status DefenseDownStack.png":
            img.replace_with("<:DefenseDownStack:743649616708370513>")
        # Double Attack down (6 turn)
        elif img["alt"] == "Status DoubleDown.png":
            img.replace_with("<:DoubleDown:743650508677578823>")
        # Glaciate (1 turn)
        elif img["alt"] == "Status Glaciate 1.png":
            img.replace_with("<:Glaciate1:744354011683225640>")
        # Glaciate (3 turn)
        elif img["alt"] == "Status Glaciate 3.png":
            img.replace_with("<:Glaciate3:744354011661991987>")
        # Double Attack down (6 turn)
        elif img["alt"] == "Status DA Down 6.png":
            img.replace_with("<:DoubleDown6:741037392378462269>")
        # Gravity
        elif img["alt"] == "Status Gravity.png":
            img.replace_with("<:Gravity:740984450841575477>")
        # Healing reduced
        elif img["alt"] == "Status HealDown.png":
            img.replace_with("<:HealDown:741718732954402838>")
        # Hostility up
        elif img["alt"] == "Status AggroUpArrow.png":
            img.replace_with("<:AggroUpArrow:744298172871868436>")
        # Lethal attack dodged
        elif img["alt"] == "Status Lethal Attack Dodged.png":
            img.replace_with("<:LethalAttackDodged:745354955506057336>")
        # Max HP Down (stackable)
        elif img["alt"] == "Status Max HP Down Stack.png":
            img.replace_with("<:MaxHPDownStack:745338049545764926>")
        # Paralysis
        elif img["alt"] == "Status Paralysis.png":
            img.replace_with("<:Paralysis:745359816981217391>")
        # Petrified
        elif img["alt"] == "Status Petrified.png":
            img.replace_with("<:Petrified:740988150616424581>")
        # Petrified (3 turn)
        elif img["alt"] == "Status Petrified 3.png":
            img.replace_with("<:Petrified3:741033218022572062>")
        # Petrified (4 turn)
        elif img["alt"] == "Status Petrified 4.png":
            img.replace_with("<:Petrified4:745395152553508956>")
        # Poison
        elif img["alt"] == "Status Poison.png":
            img.replace_with("<:Poison:744744941455933462>")
        # Shorted
        elif img["alt"] == "Status Sorted.png":
            img.replace_with("<:Shorted:745393290697769110>")
        # Sleep
        elif img["alt"] == "Status Sleep.png":
            img.replace_with("<:Sleep:741038697323036673>")
        # Special attack damage lowered (6 turn)
        elif img["alt"] == "Status SA DMG Lowered 6.png":
            img.replace_with("<:SADMGLowered6:745400447690473544>")
        # Stun
        elif img["alt"] == "Status Stun.png":
            img.replace_with("<:Quack:745360657335058513>")
        # Triple Attack down
        elif img["alt"] == "Status TripleDown.png":
            img.replace_with("<:TripleDown6:741037392437182524>")
        # Triple Attack down (6 turn)
        elif img["alt"] == "Status TA Down 6.png":
            img.replace_with("<:TripleDown:743650508715327610>")

        # Elemental ATK down
        # Dark
        elif img["alt"] == "Status DarkAtkDown.png":
            img.replace_with("<:DarkAtkDown:743944410563084389>")
        # Light
        elif img["alt"] == "Status LightAtkDown.png":
            img.replace_with("<:LightAtkDown:743944410613415987>")
        # Water
        elif img["alt"] == "Status WaterAtkDown.png":
            img.replace_with("<:WaterAtkDown:743944410353369129>")
        # Wind
        elif img["alt"] == "Status WindAtkDown.png":
            img.replace_with("<:WindAtkDown:743944410542243951>")

        # Elemental DEF down
        # Earth
        elif img["alt"] == "Status EarthResDown.png":
            img.replace_with("<:EarthResDown:744294130062196836>")
        # Dark
        elif img["alt"] == "Status DarkResDown.png":
            img.replace_with("<:DarkResDown:744294129923784746>")
        # Light
        elif img["alt"] == "Status LightResDown.png":
            img.replace_with("<:LightResDown:744294130028511253>")
        # Light (stackable)
        elif img["alt"] == "Status WaterDEFDownStack.png":
            img.replace_with("<:WaterDEFDownStack:744306047426101327>")
        # Wind
        elif img["alt"] == "Status WindResDown.png":
            img.replace_with("<:WindResDown:744294130183700610>")
