import pandas as pd
import random
import numpy as np
from faker import Faker
from character import Character
from character_manager import CharacterManager

fake = Faker()

class RaceStats:
    def __init__(self, filename="races.csv"):
        self.race_stats = self.load_race_stats(filename)

    def load_race_stats(self, filename):
        try:
            df = pd.read_csv(filename)
            races = {}
            for _, row in df.iterrows():
                race = row["Rasa"]
                stats = {
                    "Síla": (int(row["Síla_min"]), int(row["Síla_max"])),
                    "Obratnost": (int(row["Obratnost_min"]), int(row["Obratnost_max"])),
                    "Rychlost": (int(row["Rychlost_min"]), int(row["Rychlost_max"])),
                    "Vitalita": (int(row["Vitalita_min"]), int(row["Vitalita_max"])),
                    "Inteligence": (int(row["Inteligence_min"]), int(row["Inteligence_max"])),
                    "Moudrost": (int(row["Moudrost_min"]), int(row["Moudrost_max"])),
                    "Vnímavost": (int(row["Vnímavost_min"]), int(row["Vnímavost_max"])),
                    "Nadání": (int(row["Nadání_min"]), int(row["Nadání_max"])),
                    "Životnost": int(row["Životnost"]),
                    "Psychika": int(row["Psychika"]),
                    "Pohyblivost": int(row["Pohyblivost"]),
                    "Nosnost": int(row["Nosnost"]),
                    "Velikost": row["Velikost"],
                    "Životy": int(row["Životy"]),
                    "Psychické životy": int(row["Psychické životy"])
                }
                races[race] = stats
            return races
        except FileNotFoundError:
            print(f"Soubor {filename} nenalezen.")
            return {}

def generate_character(race_stats, random_generation=True, total_points=8):
    first_name = fake.first_name() if random_generation else input("Zadejte jméno postavy: ")
    race = random.choice(list(race_stats.keys())) if random_generation else select_race(race_stats)
    archetype = random.choice(['Archetyp těla', 'Archetyp mysli', 'Archetyp souznění']) if random_generation else select_archetype()
    level = random.randint(1, 20) if random_generation else int(input("Zadejte úroveň postavy: "))

    stats = race_stats[race]
    chosen_stats = distribute_points(stats, total_points, random_generation)

    # Přidání bonusových bodů pro určité rasy
    # Například: Člověk +1 bod do libovolného statu navíc
    if race == "Člověk":
        random_stat = random.choice(list(chosen_stats.keys()))
        chosen_stats[random_stat] += 1  # Přidá 1 bod do náhodného statu

    health, psyche, mobility, load, size_description = get_race_specific_stats(stats)
    life = calculate_life(chosen_stats, health)
    psyche_life = calculate_psyche_life(chosen_stats, psyche)

    return Character(first_name, race, archetype, level, chosen_stats["Síla"], chosen_stats["Obratnost"],
                     chosen_stats["Rychlost"], chosen_stats["Vitalita"], chosen_stats["Inteligence"],
                     chosen_stats["Moudrost"], chosen_stats["Vnímavost"], chosen_stats["Nadání"], health, psyche,
                     mobility, load, size_description, life, psyche_life)



    health, psyche, mobility, load, size_description = get_race_specific_stats(stats)
    life = calculate_life(chosen_stats, health)
    psyche_life = calculate_psyche_life(chosen_stats, psyche)

    return Character(first_name, race, archetype, level, chosen_stats["Síla"], chosen_stats["Obratnost"],
                     chosen_stats["Rychlost"], chosen_stats["Vitalita"], chosen_stats["Inteligence"],
                     chosen_stats["Moudrost"], chosen_stats["Vnímavost"], chosen_stats["Nadání"], health, psyche,
                     mobility, load, size_description, life, psyche_life)

def select_race(race_stats):
    print("Dostupné rasy:")
    for idx, race in enumerate(race_stats.keys(), 1):
        print(f"{idx}: {race}")
    race_key = int(input("Vyberte rasu (číslo): "))
    return list(race_stats.keys())[race_key - 1]

def select_archetype():
    archetypes = {1: 'Archetyp těla', 2: 'Archetyp mysli', 3: 'Archetyp souznění'}
    print("Dostupné archetypy:")
    for key, value in archetypes.items():
        print(f"{key}: {value}")
    archetype_key = int(input("Vyberte archetyp (číslo): "))
    return archetypes.get(archetype_key, 'Archetyp těla')

def distribute_points(stats, total_points, random_generation):
    chosen_stats = {}
    attributes = ["Síla", "Obratnost", "Rychlost", "Vitalita", "Inteligence", "Moudrost", "Vnímavost", "Nadání"]
    for attribute in attributes:
        max_points = min(total_points, stats[attribute][1])
        value = random.randint(stats[attribute][0], max_points) if random_generation else int(input(f"Zadejte {attribute} hodnotu (-1 až 3): "))
        while value < -1 or value > 3 or total_points - value < 0:
            print("Neplatná hodnota. Zkuste to znovu.")
            value = int(input(f"Zadejte {attribute} hodnotu (-1 až 3): ")) if not random_generation else random.randint(stats[attribute][0], max_points)
        chosen_stats[attribute] = value
        total_points -= value
        if total_points <= 0:
            break
    for attribute in attributes:
        if attribute not in chosen_stats:
            chosen_stats[attribute] = 0
    return chosen_stats

def get_race_specific_stats(stats):
    health = stats["Životnost"]
    psyche = stats["Psychika"]
    mobility = stats["Pohyblivost"]
    load = stats["Nosnost"]
    size = stats["Velikost"]
    size_description = {
        'A': "do 130cm",
        'B': "130 - 180cm",
        'C': "180cm - 210cm",
        'D': "210cm - 300cm",
        'E': "300cm +"
    }.get(size, "Neznámá velikost")
    return health, psyche, mobility, load, size_description

def calculate_life(chosen_stats, health):
    return int(chosen_stats["Vitalita"] + chosen_stats["Síla"] + chosen_stats["Obratnost"] + chosen_stats["Rychlost"] + health)

def calculate_psyche_life(chosen_stats, psyche):
    return int(chosen_stats["Inteligence"] + chosen_stats["Moudrost"] + chosen_stats["Vnímavost"] + chosen_stats["Nadání"] + psyche)

def save_characters_to_csv(manager, filename="characters.csv"):
    data = {
        "Jméno": [char.first_name for char in manager.characters],
        "Rasa": [char.race for char in manager.characters],
        "Archetyp": [char.archetype for char in manager.characters],
        "Úroveň": [char.level for char in manager.characters],
        "Síla": [char.strength for char in manager.characters],
        "Obratnost": [char.agility for char in manager.characters],
        "Rychlost": [char.speed for char in manager.characters],
        "Vitalita": [char.vitality for char in manager.characters],
        "Inteligence": [char.intelligence for char in manager.characters],
        "Moudrost": [char.wisdom for char in manager.characters],
        "Vnímavost": [char.perception for char in manager.characters],
        "Nadání": [char.talent for char in manager.characters],
        "Životnost": [char.health for char in manager.characters],
        "Psychika": [char.psyche for char in manager.characters],
        "Pohyblivost": [char.mobility for char in manager.characters],
        "Nosnost": [char.load for char in manager.characters],
        "Velikost": [char.size for char in manager.characters],
        "Životy": [char.life for char in manager.characters],
        "Psychické životy": [char.psyche_life for char in manager.characters]
    }
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data uložena do {filename}")
def load_characters_from_csv(filename="characters.csv"):
    try:
        df = pd.read_csv(filename)
        print("Názvy sloupců v CSV souboru:", df.columns.tolist())
        characters = []
        for _, row in df.iterrows():
            character = Character(
                row["Jméno"], row["Rasa"], row["Archetyp"], row["Úroveň"],
                row["Síla"], row["Obratnost"], row["Rychlost"], row["Vitalita"], row["Inteligence"],
                row["Moudrost"], row["Vnímavost"], row["Nadání"], row["Životnost"], row["Psychika"],
                row["Pohyblivost"], row["Nosnost"], row["Velikost"], row["Životy"], row["Psychické životy"]
            )
            characters.append(character)
        return characters
    except FileNotFoundError:
        print(f"Soubor {filename} nenalezen.")
        return []
    except KeyError as e:
        print(f"Chyba: Sloupec {e} nebyl nalezen v CSV souboru.")
        return []


def main():
    print("Načítám postavy...")  # Debug výpis
    manager = CharacterManager()
    manager.characters = load_characters_from_csv()
    print("Načítám statistiky ras...")  # Debug výpis
    race_stats = RaceStats()
    print("Vítejte v aplikaci pro správu postav!")  # Přidán uvítací výpis
    while True:
        print("\n1. Přidat novou postavu")
        print("2. Zobrazit všechny postavy")
        print("3. Vytvořit náhodnou postavu")
        print("4. Uložit postavy")
        print("5. Smazat postavu")
        print("6. Ukončit")
        choice = input("Vyberte akci: ")

        if choice == '1':
            print("Přidávám novou postavu...")  # Debug výpis
            character = generate_character(race_stats.race_stats, random_generation=False)
            if character:
                # Nastavení statů určených rasově
                race_specific_stats = race_stats.race_stats[character.race]
                character.health = race_specific_stats["Životnost"]
                character.psyche = race_specific_stats["Psychika"]
                character.mobility = race_specific_stats["Pohyblivost"]
                character.load = race_specific_stats["Nosnost"]
                manager.add_character(character)
                print(f"Postava {character.first_name} přidána.")  # Debug výpis
        elif choice == '2':
            print("Zobrazování všech postav...")  # Debug výpis
            manager.list_characters()
        elif choice == '3':
            print("Vytvářím náhodnou postavu...")  # Debug výpis
            character = generate_character(race_stats.race_stats)
            if character:
                manager.add_character(character)
                print("Náhodná postava vytvořena:")
                print(character)
        elif choice == '4':
            print("Ukládání postav...")  # Debug výpis
            save_characters_to_csv(manager)
        elif choice == '5':
            first_name = input("Zadejte jméno postavy, kterou chcete smazat: ")
            if manager.remove_character(first_name):
                print(f"Postava {first_name} byla úspěšně smazána.")
            else:
                print(f"Postava {first_name} nebyla nalezena.")
        elif choice == '6':
            print("Ukončuji program...")  # Debug výpis
            save_characters_to_csv(manager)
            break
        else:
            print("Neplatná volba. Zkuste to znovu.")

if __name__ == "__main__":
    print("Spouštím hlavní program...")  # Debug výpis
    main()
