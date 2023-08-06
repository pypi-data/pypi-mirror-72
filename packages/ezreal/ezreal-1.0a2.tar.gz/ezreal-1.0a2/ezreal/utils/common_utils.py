from os import path, makedirs
import cassiopeia as cass

# Folders utilities
base_folder = path.join(path.expanduser("~"), '.config', 'ezreal')
token_location = path.join(base_folder, 'riotapi_token.txt')

if not path.exists(base_folder):
    makedirs(base_folder)


# Riot API token acquisition
def setup_riotapi_token():
    try:
        with open(token_location) as file:
            riotapi_token = file.read()
    except FileNotFoundError:
        print(f'Riot API token not found\n'
              f'If you don’t have one, you can create it at https://developer.riotgames.com/\n'
              f'It will be saved in clear text at {path.join(base_folder, "riotapi_token.txt")}\n'
              f'Please input the Riot API token:')
        riotapi_token = input()
        with open(token_location, 'w+') as file:
            file.write(riotapi_token)
    cass.set_riot_api_key(riotapi_token)