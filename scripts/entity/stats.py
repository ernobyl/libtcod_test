

class Stats:
    def __init__(self,
                 max_hp: int,
                 hp: int,
                 basepow: int,
                 addpow: int,
                 slots: int,
                 max_charges: int,
                 charges: int,
                 effect_duration: int,
                 max_distance: int,
                 aoe: int):
        self.max_hp = max_hp
        self.hp = hp
        self.basepow = basepow
        self.addpow = addpow
        self.slots = slots
        self.max_charges = max_charges
        self.charges = charges
        self.effect_duration = effect_duration
        self.max_distance = max_distance
        self.aoe = aoe

    def copy(self):
        return Stats(
            self.max_hp, self.hp, self.basepow, self.addpow, self.slots, 
            self.max_charges, self.charges, self.effect_duration, self.max_distance, self.aoe
        )

base_player = Stats(max_hp=10, hp=10, basepow=0, addpow=0, slots=0, max_charges=0, charges=0, effect_duration=0, max_distance=0, aoe=0)

enemy_melee = Stats(max_hp=50, hp=50, basepow=5, addpow=0, slots=0, max_charges=0, charges=0, effect_duration=0, max_distance=0, aoe=0)

enemy_ranged = Stats(max_hp=50, hp=50, basepow=2, addpow=0, slots=0, max_charges=0, charges=0, effect_duration=0, max_distance=7, aoe=0)