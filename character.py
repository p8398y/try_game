class Character:
    def __init__(self, first_name, race, archetype, level, strength, agility, speed, vitality, intelligence, wisdom, perception, talent, health, psyche, mobility, load, size, life, psyche_life):
        self.first_name = first_name
        self.race = race
        self.archetype = archetype
        self.level = level
        self.strength = strength
        self.agility = agility
        self.speed = speed
        self.vitality = vitality
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.perception = perception
        self.talent = talent
        self.health = health
        self.psyche = psyche
        self.mobility = mobility
        self.load = load
        self.size = size
        self.life = life
        self.psyche_life = psyche_life

    def __str__(self):
        return (f"Jméno: {self.first_name}, Rasa: {self.race}, Úroveň: {self.level}, "
                f"Archetyp: {self.archetype}, Síla: {self.strength}, Obratnost: {self.agility}, "
                f"Rychlost: {self.speed}, Vitalita: {self.vitality}, Inteligence: {self.intelligence}, "
                f"Moudrost: {self.wisdom}, Vnímavost: {self.perception}, Nadání: {self.talent}, "
                f"Životnost: {self.health}, Psychika: {self.psyche}, Pohyblivost: {self.mobility}, "
                f"Nosnost: {self.load}, Velikost: {self.size}, Životy: {self.life}, Psychické životy: {self.psyche_life}")