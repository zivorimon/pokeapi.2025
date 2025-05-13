import requests
import json
import random

base_url = "https://pokeapi.co/api/v2/"

def random_id():

  return random.randint(1, 1000)

#print(f"the id that is drown is {random_ID}")

#Pull info from the link with random id
def get_pokemon_info(randon_ID):
    url = f"{base_url}/pokemon/{randon_ID}"
    response = requests.get(url)
    #print(response)

    try: # deny the scrip from failed if the there is a problem
        response = requests.get(url)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"error: {e}")
        return None

random_ID=random_id()    
pokemon_data = get_pokemon_info(random_ID)

if pokemon_data:
    try:
        with open("pokeapi/pokadex.json", "r") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = [] # אם הקובץ ריק או לא תקין JSON
    except FileNotFoundError:
        existing_data = []


    pokemon_details_to_save = {
    "name": pokemon_data.get("name"),
    "id": pokemon_data.get("id"),
    "height": pokemon_data.get("height"),
    "weight": pokemon_data.get("weight")
    }
    existing_data.append(pokemon_details_to_save)

    try:
        with open("pokeapi/pokadex.json", "w") as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False) # כותב בחזרה לקובץ עם indent וקידוד utf-8
        print(f"You pulled the Pokémon named: {pokemon_data['name']} from the deck. he added to your pokadex!")
    except IOError as e:
        print(f"error {e}")
