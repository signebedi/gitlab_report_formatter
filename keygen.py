import configparser
import uuid
import os

def generate_key():
    return str(uuid.uuid4())

def update_config(file, new_key):
    config = configparser.ConfigParser()
    
    # If config.ini file does not exist, create it and add the initial key
    if not os.path.isfile(file):
        config['API_KEYS'] = {new_key: new_key}
    else:  
        config.read(file)
        # append the new key
        if not config.has_section('API_KEYS'):
            config.add_section('API_KEYS')
        config['API_KEYS'][new_key] = new_key

    # Write changes back to file
    with open(file, 'w') as configfile:
        config.write(configfile)

    print(f'New key generated and saved: {new_key}')


new_key = generate_key()
update_config('config.ini', new_key)