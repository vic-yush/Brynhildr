from bs4 import BeautifulSoup


def iconreplace(parsed: BeautifulSoup) -> None:
    """
    Replaces all icon tags in the given parsed HTML code with their respective
    icons in emote form. As it turns out, there was a better way to do this.
    Thanks, Unc.

    :param parsed: Parsed HTML code in the form of a BeautifulSoup object
    :return: None, the BeautifulSoup object is directly modified
    """

    icon_map = {
        # BUFFS
        # "Adversity" (damage amplified)
        'Status Adversity.png': '<:Adversity:744355101417799796>',
        # Armoured
        'Status Armored.png': '<:Armored:730830371058614282>',
        # Attack up
        'Status AttackUp.png': '<:AttackUp:730824577651048539>',
        # Attack up (stackable)
        'Status AttackUpStack.png': '<:AttackUpStack:730830371045900320>',
        # Autorevive
        'Status AutoRevive.png': '<:AutoRevive:730830370886385705>',
        # Bonus damage (echoes)
        'Status Bonus Damage.png': '<:BonusDamage:741033069724696677>',
        # Chain burst damage cap up
        'Status CB DMG Cap Up.png': '<:CBCap:730830370919940106>',
        # Charge attack damage cap up
        'Status CA DMG Cap.png': '<:CACap:730830370798436353>',
        # Charge attack damage up (1 time)
        'Status C.A. DMG Boosted (1 time).png': '<:CAUp1:744316047510994964>',
        # Charge attack damage up (1 time)
        'Status C.A. Reactivation.png': '<:CARe:730830371125592114>',
        # Charge bar effects
        'Status Uplift.png': '<:ChargeBar:730532683364434092>',
        # Counter on dodge
        'Status Counter.png': '<:Counter:730830629737988186>',
        # Counter on dodge/damage
        'Status Counter DodgeDMG.png': '<:CounterDodgeDMG:745326045393059850>',
        # Damage cap up
        'Status DamageCapUp.png': '<:CapUp:730836378702839878>',
        # Debuff success up
        'Status DebuffSuccessUp.png': '<:DebuffUp:730836378287603784>',
        # Defense up
        'Status DefenseUp.png': '<:DefenseUp:730824577478950933>',
        # Defense up (stackable)
        'Status DefenseUpStack.png': '<:DefenseUpStack:745336776817639465>',
        # "Defiance" (Azir)
        'Status Defiance.png': '<:Azir:730830371049963681>',
        # Dispel cancel
        'Status Dispel Cancel.png': '<:DispelCancel:730836378367164560>',
        # Dodge
        'Status Dodge.png': '<:Dodge:730836378656571474>',
        # Dodge all (1 time)
        'Status Dodge 1.png': '<:Dodge1:744752642626158642>',
        # Double attack up
        'Status DoubleUp.png': '<:DoubleUp:730824577487208468>',
        # Double attack up
        'Status Drain.png': '<:Drain:730836378685800538>',
        # Effect on dodge
        'Status EffectOnDodge.png': '<:EffectOnDodge:744385082663370832>',
        # Heal effects (includes Refresh)
        'Status Heal.png': '<:Heal:741030651544862782>',
        # Hype (1 stack)
        'Status Hype1.png': '<:Hype1:744385939924844596>',
        # Jammed
        'Status Jammed.png': '<:Jammed:744303000516034742>',
        # Keen
        'Status Keen.png': '<:Keen:741022857177595997>',
        # Mirror Image
        'Status Mirror Image.png': '<:MirrorImage:741033069582090402>',
        # Repel (also Unchallenged)
        'Status Repel.png': '<:Repel:741031304895791156>',
        # Revitalize
        'Status Revitalize.png': '<:Revitalize:739609067185504318>',
        # Routine Step (multistrike)
        'Status Routine Step.png': '<:MultiStrike:730830371075260557>',
        # Shield
        'Status Shield.png': '<:Shield:741019009427963907>',
        # Skill damage up
        'Status SkillUp.png': '<:SkillUp:744989088507232456>',
        # Skill damage cap up
        'Status Skill DMG Cap Up.png': '<:SkillDMGCapUp:744396609768652981>',
        # Skill damage cap up (stackable)
        'Status Skill DMG Cap Up Stack.png':
            '<:SkillDMGCapUpStack:744379777321926707>',
        # Strength
        'Status Strength.png': '<:Strength:740988555894980708>',
        # Substitute
        'Status Substitute.png': '<:Substitute:741009875127238676>',
        # Supplemental damage (The purple spiky circle)
        'Status DmgUp.png': '<:DmgUp:739971047247315025>',
        # Triple Attack up
        'Status TripleUp.png': '<:TripleUp:730824577508442132>',
        # Veil
        'Status Veil.png': '<:Veil:741033069548404819>',

        # Crests
        # Aurora
        'Status Aurora Crest 1.png': '<:Aurora:740327163961540679>',
        'Status Aurora Crest.png': '<:Aurora:740327163961540679>',
        # Deluge
        'Status Deluge Crest 1.png': '<:Deluge:740327164364324904>',
        'Status Deluge Crest.png': '<:Deluge:740327164364324904>',
        # Hellfire
        'Status Hellfire Crest 1.png': '<:Hellfire:740327164544811038>',
        'Status Hellfire Crest.png': '<:Hellfire:740327164544811038>',
        # Typhoon
        'Status Typhoon Crest 1.png': '<:Typhoon:740327164385427557>',
        'Status Typhoon Crest.png': '<:Typhoon:740327164385427557>',
        # Wasteland
        'Status Wasteland Crest 1.png': '<:Wasteland:740327164389621830>',
        'Status Wasteland Crest.png': '<:Wasteland:740327164389621830>',

        # Critical up
        'Status CriticalUp.png': '<:CriticalUp:741028610697068584>',
        # Critical up (Dark)
        'Status CriticalUpDark.png': '<:CriticalUpDark:741028610432958654>',
        # Critical up (Water)
        'Status CriticalUpWater.png': '<:CriticalUpWater:741028610433089698>',

        # Damage cuts
        # 50%
        'Status Dmg Cut 50.png': '<:DC50:730870761178529862>',
        # Fire (70%)
        'Status Fire Cut 70.png': '<:FC70:730877406604296213>',
        # Water (20%)
        'Status Water Cut 20.png': '<:WC20:730879492721213500>',
        # Wind (40%)
        'Status Wind Cut 40.png': '<:GC40:730884667007434793>',

        # Element Switches
        # Wind
        'Status Wind Switch.png': '<:WindSwitch:743648516538105906>',

        # Elemental ATK up
        # Dark
        'Status DarkAtkUp.png': '<:DarkAtkUp:741720281751748660>',
        # Earth
        'Status EarthAtkUp.png': '<:EarthAtkUp:741720282384826438>',
        # Fire
        'Status FireAtkUp.png': '<:FireAtkUp:741720282414186526>',
        # Light
        'Status LightAtkUp.png': '<:LightAtkUp:741720282120847364>',
        # Water
        'Status WaterAtkUp.png': '<:WaterAtkUp:741720282640678963>',
        # Wind
        'Status WindAtkUp.png': '<:WindAtkUp:741720282472906874>',

        # Elemental DEF up
        'Status DarkResUp.png': '<:DarkResUp:730840334363525130>',  # Dark
        'Status FireResUp.png': '<:FireResUp:730840334401142874>',  # Fire

        # DEBUFFS
        # Acccuracy lowered (2 turn)
        'Status Accuracy Lowered 2.png':
            '<:AccuracyLowered2:745330950006636626>',
        # Acccuracy lowered (3 turn)
        'Status Accuracy Lowered 3.png':
            '<:AccuracyLowered3:741718281291038838>',
        # Acccuracy lowered (6 turn)
        'Status Accuracy Lowered 6.png':
            '<:AccuracyLowered6:741037392391045161>',
        # Attack down
        'Status AttackDown.png': '<:AttackDown:741034514817745006>',
        # Attack down (4 turn)
        'Status ATK Down 4.png': '<:ATKDown4:745395152939647107>',
        # Attack down (stackable)
        'Status AttackDownStack.png': '<:AttackDownStack:743649616985063424>',
        # Blind
        'Status Blind.png': '<:Blind:741033217880096820>',
        # Burned
        'Status Burned.png': '<:Burned:741708251254489129>',
        # Charmed
        'Status Charm.png': '<:Charm:744300407915806801>',
        # Charmed (3 turn)
        'Status Charm 3.png': '<:Charm3:744388963053076611>',
        # Debuff resistance down
        'Status DebuffResDown.png': '<:DebuffResDown:744752535361028176>',
        # Defense down
        'Status DefenseDown.png': '<:DefenseDown:740984047274033173>',
        # Defense down (3 turn)
        'Status DEF Down 3.png': '<:DefenseDown3:741033218014314586>',
        # Defense down (4 turn)
        'Status DEF Down 4.png': '<:DEFDown4:745395152759160903>',
        # Defense down (stackable)
        'Status DefenseDownStack.png': '<:DefenseDownStack:743649616708370513>',
        # Double Attack down (6 turn)
        'Status DoubleDown.png': '<:DoubleDown:743650508677578823>',
        # Glaciate (1 turn)
        'Status Glaciate 1.png': '<:Glaciate1:744354011683225640>',
        # Glaciate (3 turn)
        'Status Glaciate 3.png': '<:Glaciate3:744354011661991987>',
        # Double Attack down (6 turn)
        'Status DA Down 6.png': '<:DoubleDown6:741037392378462269>',
        # Gravity
        'Status Gravity.png': '<:Gravity:740984450841575477>',
        # Healing reduced
        'Status HealDown.png': '<:HealDown:741718732954402838>',
        # Hostility up
        'Status AggroUpArrow.png': '<:AggroUpArrow:744298172871868436>',
        # Lethal attack dodged
        'Status Lethal Attack Dodged.png':
            '<:LethalAttackDodged:745354955506057336>',
        # Max HP Down (stackable)
        'Status Max HP Down Stack.png': '<:MaxHPDownStack:745338049545764926>',
        # Paralysis
        'Status Paralysis.png': '<:Paralysis:745359816981217391>',
        # Petrified
        'Status Petrified.png': '<:Petrified:740988150616424581>',
        # Petrified (3 turn)
        'Status Petrified 3.png': '<:Petrified3:741033218022572062>',
        # Petrified (4 turn)
        'Status Petrified 4.png': '<:Petrified4:745395152553508956>',
        # Poison
        'Status Poison.png': '<:Poison:744744941455933462>',
        # Shorted
        'Status Sorted.png': '<:Shorted:745393290697769110>',
        # Sleep
        'Status Sleep.png': '<:Sleep:741038697323036673>',
        # Special attack damage lowered (6 turn)
        'Status SA DMG Lowered 6.png': '<:SADMGLowered6:745400447690473544>',
        # Stun
        'Status Stun.png': '<:Quack:745360657335058513>',
        # Triple Attack down
        'Status TripleDown.png': '<:TripleDown6:741037392437182524>',
        # Triple Attack down (6 turn)
        'Status TA Down 6.png': '<:TripleDown:743650508715327610>',

        # Elemental ATK down
        # Dark
        'Status DarkAtkDown.png': '<:DarkAtkDown:743944410563084389>',
        # Light
        'Status LightAtkDown.png': '<:LightAtkDown:743944410613415987>',
        # Water
        'Status WaterAtkDown.png': '<:WaterAtkDown:743944410353369129>',
        # Wind
        'Status WindAtkDown.png': '<:WindAtkDown:743944410542243951>',

        # Elemental DEF down
        # Earth
        'Status EarthResDown.png': '<:EarthResDown:744294130062196836>',
        # Dark
        'Status DarkResDown.png': '<:DarkResDown:744294129923784746>',
        # Light
        'Status LightResDown.png': '<:LightResDown:744294130028511253>',
        # Water (stackable)
        'Status WaterDEFDownStack.png':
            '<:WaterDEFDownStack:744306047426101327>',
        # Wind
        'Status WindResDown.png': '<:WindResDown:744294130183700610>'
    }

    for img in parsed.find_all("img"):
        alt = img["alt"]
        if alt in icon_map.keys():
            img.replace_with(icon_map[alt])
