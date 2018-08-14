import json

with open('credentials.log') as json_file:  
    data = json.load(json_file)
    for p in data['TOKEN']:
        TOKEN = p['value']
    for p in data['MOD_ROLES']:
        mod_role_1 = p['value_1']
        mod_role_2 = p['value_2']
    for p in data['REDDIT']:
        json_client_id = p['client_id']
        json_client_secret = p['client_secret']
        json_user_agent = p['user_agent']
    for p in data['AUTHOR']:
        json_bot_author_id = p['bot_author_id']
    for p in data['GOODREADS']:
        goodreads_key = p['goodreads_key']

role_mod = [mod_role_1, mod_role_2]
