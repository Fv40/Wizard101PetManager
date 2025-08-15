"""
Breakdown of different attributes and their associated stats, from wizard101 wiki (https://wiki.wizard101central.com/wiki/Basic:Pets):
    - Strength: Affects Damage Talents, Power Pip Chance Talents, Resistance Talents, Outgoing Healing Talents, Armor Piercing Talents, and Stun Resistance Talents.
    - Intellect: Affects Mana Talents, Accuracy Talents, Power Pip Chance Talents, Critical Block Talents, Incoming Healing Talents, and Stun Resistance Talents.
    - Agility: Affects Health Talents, Accuracy Talents, Resistance Talents, Critical Talents, Incoming Healing Talents, and Armor Piercing Talents.
    - Will: Affects Damage Talents, Health Talents, Mana Talents, Critical Talents, Critical Block Talents, and Outgoing Healing Talents.
    - Power: Affects Health Talents, Mana Talents, Accuracy Talents, Damage Talents, Power Pip Chance Talents, Resistance Talents, Critical Talents, Critical Block Talents, Incoming Healing Talents, Outgoing Healing Talents, Armor Piercing Talents, and Stun Resistance Talents.
"""

from json import dump
from typing import List
from __future__ import annotations
from constants import Attribute, Stat, School, TalentRarity

class Pet:
    def __init__(
            self, 
            id: int,
            body_type: str,
            school: School,
            current_experience: int,
            parent_a_id: int | None, 
            parent_b_id: int | None, 
            name: str,
            attributes: dict[Attribute : int],
            splendor: int,
            talents: List[Talent],
    ):
        self.id = id
        self.body_type = body_type
        self.school = school
        self.current_experience = current_experience
        self.parent_a_id = parent_a_id
        self.parent_b_id = parent_b_id
        self.name = name,
        self.attributes = attributes
        self.splendor = splendor
        self.talents = talents

class Talent:
    def __init__(
            self,
            rarity: TalentRarity,
            name: str,
            card_given: str | None,
            amount_of_cards_given: int | None,
            attribute_given: Attribute | None,
            stat_is_school_specific: bool | None,
            stat_school: School | None,
            stat_given: Stat
    ):
        self.rarity = rarity
        self.name = name
        self.card_given = card_given
        self.amount_of_cards_given = amount_of_cards_given
        self.attribute_given = attribute_given
        self.name = name,
        self.stat_is_school_specific = stat_is_school_specific
        self.stat_school = stat_school
        self.stat_given = stat_given
        
def pet_to_dict(pet: Pet) -> dict:
    return {
        "id": pet.id,
        "body_type": pet.body_type,
        "school": pet.school.name,
        "current_experience": pet.current_experience,
        "parent_a_id": pet.parent_a_id,
        "parent_b_id": pet.parent_b_id,
        "name": pet.name,
        "attributes": { attr.name: value for attr, value in pet.attributes.items() },
        "splendor": pet.splendor,
        "talents": [talent_to_dict(t) for t in pet.talents],
    }

def talent_to_dict(talent: Talent) -> dict:
    return {
        "rarity": talent.rarity.name,
        "name": talent.name,
        "card_given": talent.card_given,
        "amount_of_cards_given": talent.amount_of_cards_given,
        "attribute_given": talent.attribute_given.name if talent.attribute_given else None,
        "stat_is_school_specific": talent.stat_is_school_specific,
        "stat_school": talent.stat_school.name if talent.stat_school else None,
        "stat_given": talent.stat_given.name,
    }

def save_pets_to_json(pets: list[Pet], filepath: str):
    with open(filepath, "w", encoding="utf-8") as pet_file:
        dump([pet_to_dict(pet) for pet in pets], pet_file, indent=2)