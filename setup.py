import json

def credentials():
    with open('config.json') as json_file:
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
                prefix_input = input("Please set a command prefix now: ")
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
                    'REDDIT': [
                        {
                            'client_id': reddit_client_id_input,
                            'client_secret': reddit_client_secret_input,
                            'user_agent': reddit_user_agent_input
                        }
                    ],
                    'PREFIX': [
                        {
                            'prefix': prefix_input
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
                    ]
                }
                with open('config.json', 'w') as outfile:
                    json.dump(data, outfile)
                    print("Data successfully written to logfile.")
                    end()
                with open('config.json') as json_file:
                    data = json.load(json_file)
                    for p in data['TOKEN']:
                        TOKEN = p['value']
                    for p in data['REDDIT']:
                        json_client_id = p['client_id']
                        json_client_secret = p['client_secret']
                        json_user_agent = p['user_agent']
                    for p in data['PREFIX']:
                        prefix_input = p['prefix']
                    for p in data['GOODREADS']:
                        goodreads_key = p['goodreads_key']
                return
        with open('config.json') as json_file:
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
        with open('config.json') as json_file:
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
        with open('config.json') as json_file:
            data = json.load(json_file)
            for p in data['TOKEN']:
                TOKEN = p['value']
            for p in data['REDDIT']:
                json_client_id = p['client_id']
                json_client_secret = p['client_secret']
                json_user_agent = p['user_agent']
            for p in data['PREFIX']:
                prefix_input = p['prefix']
            for p in data['GOODREADS']:
                goodreads_key = p['goodreads_key']
        print("Token: " + TOKEN)
        print("Prefix: " + prefix_input)
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
    print("Ending script now.\n\nStart bot with `sudo python3 discord_bot_3.6.py`\n\n")
    return

welcome()