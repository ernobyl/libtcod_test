
class Equipment:
    def __init__(self,
                 basepow: int,
                 addpow: int,
                 slots: int,
                 max_charges: int,
                 effect_duration: int,
                 max_distance: int,
                 aoe: int):
        self.basepow = basepow
        self.addpow = addpow
        self.slots = slots
        self.max_charges = max_charges
        self.charges = max_charges
        self.effect_duration = effect_duration
        self.max_distance = max_distance
        self.aoe = aoe

r_pouch = Equipment(basepow=20, addpow=5, slots=1, max_charges=6, effect_duration=0, max_distance=3, aoe=0)