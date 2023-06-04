import os
import datetime as dt
import json

from view import global_view as v
from models.player import Player
from models.tournament import Tournament
from models.turn import Turn

DB_FILE_NAME = "database.json"
TOURNAMENT = "tournaments"
PLAYERS = "players"
TURN = "turns"
INIT_DB_JSON = """
{
    "players": [
    
    ],
    "tournaments": [
    
    ],
    "turns": [
    
    ],
}
"""

def launch():
    running = True
    v.display_welcoming_message()
    init_database()
    while running:
        choice = v.display_action_pannel()
        running = call_function(choice)


def call_function(choice):
    if choice == "1":
        create_player()
    if choice == "2":
        create_tournament()
    if choice == "3":
        v.display_players()
    if choice == "4":
        v.display_tournaments()
    #Exit
    if choice == "8":
        return False
    return True

def is_birthdate_correct(birthdate: str):
    """Check if birthdate follow the layout DD/MM/YYYY and is a valid date"""
    is_correct = True
    if len(birthdate) == 10:
        if birthdate.count("/") == 2:
            splited_birthdate = birthdate.split("/")
            day_date = int(splited_birthdate[0])
            month_date = int(splited_birthdate[1])
            year_date = int(splited_birthdate[2])
            #Check if the date is a correct one
            try:
                dt.datetime(year_date, month_date, day_date)
            except ValueError:
               is_correct = False
    return is_correct

def is_national_chess_id_correct(id: str):
    """Check if id follow the layout AB12345"""
    return id[:2].isalpha() and id[5:].isnumeric() and len(id)==7
    

def create_player():
    """Create a player"""
    data = v.ask_player_info_for_creation()
    #Check if first name is long enough
    if len(data['first_name']) >= 3:
        #Check if last name is long enough
        if len(data['last_name']) >= 3:
            #Check if birthdate is correct
            if is_birthdate_correct(data['birth_date']):
                #Check if national chess id is correct
                if is_national_chess_id_correct(data['national_chess_id']):
                    try:
                        a = Player(data['first_name'], data['last_name'], data['birth_date'], data['national_chess_id'])
                        save(PLAYERS, a, data)
                        print(a)
                    except TypeError as error:
                        print(error)
                    except Exception as error:
                        print(error)


def save(model_name, item_to_save, data):
    """Save a given object in a given category of the Json database with a unique incremental ID"""
    with open(DB_FILE_NAME, 'r+') as file:
            data = json.load(file)
            #We take the last gived ID and add 1 to it to make sure no object from the same class are equal by id
            item_to_save.id = data[model_name][-1]["id"]+1
            data[model_name].append(item_to_save.__dict__)
            file.seek(0)
            json.dump(data, file, indent=4)

def create_tournament():
    """Create a tournament"""
    data = v.ask_tournament_info_for_creation()
    try:
        t = Tournament(data['name'], data['place'], data['starting_date'], data['ending_date'], data['description'])
        save(TOURNAMENT, t, data)
    except TypeError as error:
        print(error)
    except Exception as error:
        print(error)


def init_database(): 
    isFile = os.path.isfile(DB_FILE_NAME)
    if (not isFile):
        with open(DB_FILE_NAME, 'w') as fp:
            json.dump(INIT_DB_JSON, fp, indent=4)
    else:
        print(f'The {DB_FILE_NAME} file is already initialized.')