from enum import Enum

from worlds.generic.Rules import forbid_item
from rule_builder.rules import (Has, HasAny, HasAll, True_)
from .Locations import (SPHERE, BUILDING, CHECK_TYPE, SPELLS, PLANTS, locations)



class BUILDING_NAME(Enum):
    CURSOR = "Cursor"
    # GRANDMA = "Grandma"
    FARM = "Farm"
    MINE = "Mine"
    FACTORY = "Factory"
    BANK = "Bank"
    TEMPLE = "Temple"
    WIZARD_TOWER = "Wizard Tower"
    SHIPMENT = "Shipment"
    ALCHEMY_LAB = "Alchemy Lab"
    PORTAL = "Portal"
    TIME_MACHINE = "Time Machine"
    ANTIMATTER_CONDENSER = "Antimatter Condenser"
    PRISM = "Prism"
    CHANCEMAKER = "Chancemaker"
    FRACTAL_ENGINE = "Fractal Engine"
    JAVASCRIPT_CONSOLE = "Javascript Console"
    IDLEVERSE = "Idleverse"
    CORTEX_BAKER = "Cortex Baker"
    YOU = "You"

    def to_building_id(self):
        return BUILDING[self.name].value

    def unlock_item(self):
        return "Unlock " + self.value

    def progressive_item(self):
        return "Progressive " + self.value
        
class SPELL_NAME(Enum):
    CONJURE = "Conjure Baked Goods"
    FORCE = "Force the Hand of Fate"
    STRETCH = "Stretch Time"
    EDIFICE = "Spontaneous Edifice"
    HAGGLER = "Haggler's Charm"
    PIXIES = "Summon Crafty Pixies"
    GAMBLER = "Gambler's Fever Dream"
    RESURRECT = "Resurrect Abomination"
    DIMINISH = "Diminish Ineptitude"

    def unlock_item(self):
        return "Unlock " + self.value

    def progressive_item(self):
        return "Progressive " + self.value
        
class PLANT_NAME(Enum):
    BAKERS_WHEAT = "Baker's Wheat"
    THUMBCORN = "Thumbcorn"
    CRONERICE = "Cronerice"
    GILDMILLET = "Gildmillet"
    ORDINARY_CLOVER = "Ordinary Clover"
    GOLDEN_CLOVER = "Golden Clover"
    SHIMMERLILY = "Shimmerlily"
    ELDERWORT = "Elderwort"
    BAKEBERRY = "Bakeberry"
    CHOCOROOT = "Chocoroot"
    WHITE_CHOCOROOT = "White Chocoroot"
    WHITE_MILDEW = "White Mildew"
    BROWN_MOLD = "Brown Mold"
    MEDDLEWEED = "Meddleweed"
    WHISKERBLOOM = "Whiskerbloom"
    CHIMEROSE = "Chimerose"
    NURSETULIP = "Nursetulip"
    DROWSYFERN = "Drowsyfern"
    WARDLICHEN = "Wardlichen"
    KEENMOSS = "Keenmoss"
    QUEENBEET = "Queenbeet"
    JUICY_QUEENBEET = "Juicy Queenbeet"
    DUKETATER = "Duketater"
    CRUMBSPORE = "Crumbspore"
    DOUGHSHROOM = "Doughshroom"
    GLOVEMOREL = "Glovemorel"
    CHEAPCAP = "Cheapcap"
    FOOLS_BOLETE = "Fool's Bolete"
    WRINKLEGILL = "Wrinklegill"
    GREEN_ROT = "Green Rot"
    SHRIEKBULB = "Shriekbulb"
    TIDYGRASS = "Tidygrass"
    EVERDAISY = "Everdaisy"
    ICHORPUFF = "Ichorpuff"

    def unlock_item(self):
        return "Unlock " + self.value

    def progressive_item(self):
        return "Progressive " + self.value
        
SPELL_GATE = HasAny(
    BUILDING_NAME.WIZARD_TOWER.unlock_item(),
    BUILDING_NAME.WIZARD_TOWER.progressive_item()
)

PLANT_GATE = HasAny(
    BUILDING_NAME.FARM.unlock_item(),
    BUILDING_NAME.FARM.progressive_item()
)

def set_rules(self: "CookieClicker"):
    world = self.multiworld
    player = self.player

    # 1) Prevent each “Unlock Building” item from ever appearing in any of that building’s own-achievement locations.
    for building in BUILDING_NAME:
        for location in locations['by_building'][BUILDING[building.name]]:
            cclocation = world.get_location(location.name, player)
            forbid_item(cclocation, building.unlock_item(), player)
            forbid_item(cclocation, building.progressive_item(), player)

        # handle spell and plant logic
        for achv in locations['valid']:
        loc = world.get_location(achv.name, player)

        if achv.check_type == CHECK_TYPE.SPELL.value:
            loc.access_rule = SPELL_GATE & Has(
                SPELL_NAME(SPELLS(achv.building)).progressive_item()
            )

        elif achv.check_type == CHECK_TYPE.PLANT.value:
            loc.access_rule = PLANT_GATE & Has(
                PLANT_NAME(PLANTS(achv.building)).progressive_item()
            )

    # 2) Make the “sphere 0” achievements always available
    # 3) Rough sphere implementation. Don't ask how it's balanced

    # INFO : step 2 & 3 are handled directly during Region creation.


    # 4) Standard completion check. Due to AP limitations, the achievement count check is done client-side
    #    and a special Victory item is unlocked if conditions are met
    self.multiworld.completion_condition[player] = lambda state: state.has("Victory", self.player)


RULES = {
    SPHERE.ZERO: True_(),
    SPHERE.ONE: HasAny(BUILDING_NAME.TEMPLE.unlock_item(), BUILDING_NAME.TEMPLE.progressive_item(),
                       BUILDING_NAME.WIZARD_TOWER.unlock_item(), BUILDING_NAME.WIZARD_TOWER.progressive_item()),
    SPHERE.TWO: HasAny(BUILDING_NAME.ALCHEMY_LAB.unlock_item(), BUILDING_NAME.ALCHEMY_LAB.progressive_item(),
                       BUILDING_NAME.PORTAL.unlock_item(), BUILDING_NAME.PORTAL.progressive_item()),
    SPHERE.THREE: HasAny(BUILDING_NAME.FRACTAL_ENGINE.unlock_item(), BUILDING_NAME.FRACTAL_ENGINE.progressive_item()),
    SPHERE.FOUR: HasAny(BUILDING_NAME.IDLEVERSE.unlock_item(), BUILDING_NAME.IDLEVERSE.progressive_item()),
    SPHERE.FIVE: HasAny(BUILDING_NAME.CORTEX_BAKER.unlock_item(), BUILDING_NAME.CORTEX_BAKER.progressive_item()),
    SPHERE.LATEGAME: HasAny(BUILDING_NAME.YOU.unlock_item(), BUILDING_NAME.YOU.progressive_item()),
    SPHERE.ENDGAME: Has("A crumbly egg") &
                    (HasAll(*[b.unlock_item() for b in BUILDING_NAME])
                     | HasAll(*[b.progressive_item() for b in BUILDING_NAME])),
    SPHERE.GRANDMA: HasAny("One Mind", "Communal brainsweep", "Elder Pact")
}
