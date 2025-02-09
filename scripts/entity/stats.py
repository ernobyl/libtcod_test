

class Stats:
    def __init__(self,
                 hp: int,
                 basepow: int,
                 addpow: int,
                 slots: int,
                 max_charges: int,
                 effect_duration: int,
                 max_distance: int,
                 aoe: int):
        self.hp = hp
        self.basepow = basepow
        self.addpow = addpow
        self.slots = slots
        self.max_charges = max_charges
        self.effect_duration = effect_duration
        self.max_distance = max_distance
        self.aoe = aoe

base_player = Stats(hp=50, basepow=0, addpow=0, slots=0, max_charges=0, effect_duration=0, max_distance=0, aoe=0)

enemy = Stats(hp=50, basepow=20, addpow=0, slots=0, max_charges=0, effect_duration=0, max_distance=0, aoe=0)