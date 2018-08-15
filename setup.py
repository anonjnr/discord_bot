import json


def credentials():
    with open('credentials.log') as json_file:
        data = json.load(json_file)
        for x in range(3):
            if x == 0:
                y = ("[1st Try] ")
            elif x == 1:
                y = ("[2nd Try] ")
            elif x == 2:
                y = ("[3rd Try] ")
            token_input = input(y + "Please enter your Discord Token now: ")
            if token_input != "":
                bot_author_id_input = input("Please enter the authors discord user ID now: ")
                admin_role_1_input = input("Please enter the ID of the Administrator Role now: ")
                admin_role_2_input = input(
                    "Please enter the ID of another Administrator Role now (leave blank if not needed): ")
                reddit_client_id_input = input("Please enter the Reddit client ID now (leave blank if not needed): ")
                reddit_client_secret_input = input(
                    "Please enter the Reddit client secret now (leave blank if not needed): ")
                reddit_user_agent_input = input(
                    "Please enter the Reddit client user agent info now (leave blank if not needed): ")
                goodreads_key_input = input("Please enter the Goodreads Key now (leave blank if not needed): ")
                data = {
                    'TOKEN': [
                        {
                            'value': token_input
                        }
                    ],
                    'MOD_ROLES': [
                        {
                            'value_1': admin_role_1_input,
                            'value_2': admin_role_1_input
                        }
                    ],
                    'REDDIT': [
                        {
                            'client_id': reddit_client_id_input,
                            'client_secret': reddit_client_secret_input,
                            'user_agent': reddit_user_agent_input
                        }
                    ],
                    'AUTHOR': [
                        {
                            'bot_author_id': bot_author_id_input
                        }
                    ],
                    'GOODREADS': [
                        {
                            'goodreads_key': goodreads_key_input
                        }
                    ],
                    'TOKEN': [
                        {
                            'value': token_input
                        }
                    ],
                    'MOD_ROLES': [
                        {
                            'value_1': admin_role_1_input,
                            'value_2': admin_role_2_input
                        }
                    ]
                }
                with open('credentials.log', 'w') as outfile:
                    json.dump(data, outfile)
                    print("Data successfully written to logfile.")
                    end()
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
                return
        with open('credentials.log') as json_file:
            data = json.load(json_file)
            for p in data['TOKEN']:
                TOKEN = p['value']
                if not TOKEN:
                    print("Please get your Discord Token ready and start again.")
                    end()
                else:
                    unchanged_token = input("You already have an Discord Token saved. Leave it unchanged? (y/n/exit) ")
                    if unchanged_token == "y":
                        start()
                    elif unchanged_token == "n":
                        credentials()
                    elif unchanged_token == "exit":
                        end()
                    else:
                        print("Invalid input")
                        start()


def welcome():
    print("This is the setup file for the Discord Bot.")
    print("Here you can enter, change or view all credentials needed to run it.\n")
    start()


def start():
    start_question = input("Do you want to enter your credentials or make changes? (y/n/exit) ")
    if start_question == "y":
        credentials()
    elif start_question == "n":
        with open('credentials.log') as json_file:
            data = json.load(json_file)
            for p in data['TOKEN']:
                TOKEN = p['value']
            if not TOKEN:
                print("The Discord Token is the sole thing that isn't mandatory. Please enter it!")
                credentials()
            else:
                credentials_view()
    elif start_question == "exit":
        end()
    else:
        print("Invalid input")
        start()


def credentials_view():
    start_question_no = input("Do you want to view you credentials? (y/n/exit) ")
    if start_question_no == "y":
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
        print("Token: " + TOKEN)
        print("Discord Author ID: " + json_bot_author_id)
        print("Mod Role 1: " + mod_role_1)
        print("Mod Role 2: " + mod_role_2)
        print("Reddit Client ID: " + json_client_id)
        print("Reddit Client Secret: " + json_client_secret)
        print("Reddit User Agent Info: " + json_user_agent)
        print("Goodreads Key: " + goodreads_key)
        start()
    elif start_question_no == "n":
        end()
    elif start_question_no == "exit":
        end()
    else:
        print("Invalid input. Starting over.")
        start()


def end():
    print("Ending script now.")
    return


welcome()
