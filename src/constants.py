from enum import Enum

class TalentRarity(Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    ULTRA_RARE = "Ultra-Rare"
    EPIC = "Epic"
        
class School(Enum):
    FIRE = "Fire"
    ICE = "Ice"
    STORM = "Storm"
    LIFE = "Life"
    DEATH = "Death"
    MYTH = "Myth"
    BALANCE = "Balance"

class Attribute(Enum):
    STRENGTH = "Strength"
    INTELLECT = "Intellect"
    AGILITY = "Agility"
    WILL = "Will"
    POWER = "Power"

class Stat(Enum):
    DAMAGE = "Damage"
    RESISTANCE = "Resistance"
    ACCURACY = "Accuracy"
    PIP_CHANCE = "Pip Chance"
    HEALTH = "Health"
    MANA = "Mana"
    CRITICAL = "Critical Rating"

class Rank(Enum):
    BABY = "Baby"
    TEEN = "Teen"
    ADULT = "Adult"
    ANCIENT = "Ancient"
    EPIC = "Epic"
    MEGA = "Mega"
    ULTRA = "Ultra"