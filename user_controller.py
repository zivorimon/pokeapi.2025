import json
import random

user_name = input("hello, what is your name? : ")
print(f"hello {user_name} welcome to the pokemon world")
choice = input("Do you want to draw a Pokémon ? (yes/no): ").strip().lower()

if choice == "yes":
    from import_data import get_pokemon_info, random_id, pokemon_details_to_save
    drawn_pokemon = get_pokemon_info(random_id())

else :
    print("have a nice day")
    exit


print("The Pokémon details are:")
for key, value in pokemon_details_to_save.items():
    print(f"{key}: {value}")

choice = input("Do you want to add this Pokémon to your bag? (yes/no): ").strip().lower()



if choice == "yes":


    try:
        # ננסה לקרוא קובץ קיים
        with open("pokeapi/my_pokemon.json", "r") as f:
            try:
                existing_my_pokemon = json.load(f)
            except json.JSONDecodeError:
                existing_my_pokemon = []
    except FileNotFoundError:
        existing_my_pokemon = []

    existing_my_pokemon.append(pokemon_details_to_save)

    try:
        with open("pokeapi/my_pokemon.json", "w") as f:
            json.dump(existing_my_pokemon, f, indent=4, ensure_ascii=False)
            print(f"{pokemon_details_to_save['name']} was added to your personal Pokémon list!")
    except IOError as e:
        print(f"Error saving to my_pokemon.json: {e}")
else:
    print("Okay, maybe next time!")
