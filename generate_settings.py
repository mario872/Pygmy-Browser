import json

config = {
    'search_engine': 'google',
    'home_file_location': 'Home Page - Pygmy.html'
    }

config_json = json.dumps(config)

config_json_file = open("configuration.txt","w")
config_json_file.write(str(config_json))
config_json_file.close()