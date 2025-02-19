
class Equipment:
    def __init__(self,
                 name: str,
                 basepow: int,
                 addpow: int,
                 slots: int,
                 max_charges: int,
                 charges: int,
                 effect_duration: int,
                 max_distance: int,
                 aoe: int):
        self.name = name
        self.basepow = basepow
        self.addpow = addpow
        self.slots = slots
        self.max_charges = max_charges
        self.charges = charges
        self.effect_duration = effect_duration
        self.max_distance = max_distance
        self.aoe = aoe
        self.x = None
        self.y = None

r_pouch = Equipment(name="Rune pouch", basepow=20, addpow=5, slots=1, max_charges=8, charges=8, effect_duration=0, max_distance=3, aoe=0)
m_disc = Equipment(name="Mage's discus", basepow=10, addpow=0, slots=1, max_charges=2, charges=2, effect_duration=0, max_distance=6, aoe=1)