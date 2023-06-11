import os
import datetime as dt
import json

from view import global_view as v
from models.player import Player
from models.tournament import Tournament
from models.round import Round

DB_FILE_NAME = "database.json"
TOURNAMENTS = "tournaments"
ROUND_LIST = "list_rounds"
PLAYERS = "players"
ROUNDS = "rounds"
UNDEFINED = "Non defini"
INIT_DB_JSON = """
{
    "players": [
    
    ],
    "tournaments": [
    
    ],
    "rounds": [
    
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
    if choice == "5":
        add_player_to_tournament()
    if choice == "6":
        generate_next_round_for_tournament()
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
                        player = Player(data['first_name'], data['last_name'], data['birth_date'], data['national_chess_id'])
                        save(PLAYERS, player)
                    except TypeError as error:
                        print(error)
                    except Exception as error:
                        print(error)


def save(model_name, item_to_save):
    """Save a given object in a given category of the Json database with a unique incremental ID"""
    with open(DB_FILE_NAME, 'r+') as file:
            data = json.load(file)
            #We take the last gived ID and add 1 to it to make sure no object from the same class are equal by id
            if len(data[model_name]) == 0:
                item_to_save.id = 0
            else:
                item_to_save.id = data[model_name][-1]["id"]+1
            data[model_name].append(item_to_save.__dict__)
            file.seek(0)
            json.dump(data, file, indent=4)



def create_tournament():
    """Create a tournament"""
    data = v.ask_tournament_info_for_creation()
    try:
        tournament = Tournament(data['name'], data['place'], data['starting_date'], data['ending_date'], data['description'])
        save(TOURNAMENTS, tournament)
    except TypeError as error:
        print(error)
    except Exception as error:
        print(error)


def generate_next_round_for_tournament():
    try:
        tournament_id = int(v.ask_tournament_id())
    except ValueError:
        print("Veuillez entrer un nombre correspondant à l'identifiant du tournois !")

    try:

        #Change ending date for last round of this tournament
        with open("database.json", 'r+') as file:
                data = json.load(file)
                tournaments = data[TOURNAMENTS]
                list_rounds = data[TOURNAMENTS][tournament_id][ROUND_LIST]
                # >1 because we check it after adding a round to the tournament
                if len(list_rounds) > 0: 
                    round = tournaments[tournament_id]["list_rounds"][-1]
                    print(round["ending_date_hour"])
                    round["ending_date_hour"] = dt.datetime.now().strftime("%d-%d-%Y %H:%M")
                    file.seek(0)
                    json.dump(data, file, indent=4)

        with open("database.json", 'r+') as file:
                data = json.load(file)
                tournaments = data[TOURNAMENTS]
                if is_tournament_existing(tournament_id, tournaments):
                    next_round_number = len(tournaments[tournament_id]["list_rounds"]) + 1 
                    round_id = create_round(next_round_number, tournament_id)

        

            
    except UnboundLocalError as e:
        print(e)
        print("Le tournois choisi n'existe pas !")
    

def create_round(round_number, tournament_id):
    """Create a round for a given tournament"""
    matches = []
    try:
        round = Round(f"Round {round_number}", dt.datetime.now().strftime("%d-%d-%Y %H:%M"), UNDEFINED, matches)
        save_round_in_tournament(round, tournament_id)
    except TypeError as error:
        print(error)
    except Exception as error:
        print(error)


def save_round_in_tournament(item_to_save, tournament_id):
    with open(DB_FILE_NAME, 'r+') as file:
            data = json.load(file)
            round_list = data[TOURNAMENTS][tournament_id][ROUND_LIST]
            #We take the last gived ID and add 1 to it to make sure no object from the same class are equal by id
            if len(round_list) == 0:
                item_to_save.id = 0
            else:
                item_to_save.id = round_list[-1]["id"]+1
            round_list.append(item_to_save.__dict__)
            file.seek(0)
            json.dump(data, file, indent=4)



def init_database(): 
    isFile = os.path.isfile(DB_FILE_NAME)
    if (not isFile):
        with open(DB_FILE_NAME, 'w') as fp:
            json.dump(INIT_DB_JSON, fp, indent=4)
    else:
        print(f'The {DB_FILE_NAME} file is already initialized.')

def is_player_existing(player_id, players):
    return any(p['id'] == player_id for p in players)

def is_tournament_existing(tournament_id, tournaments):
    return any(t['id'] == tournament_id for t in tournaments)
    
def add_player_to_tournament():
    """Add a player to a tournament in in database"""
    tournament_id = int(v.ask_tournament_id())
    player_id = int(v.ask_player_id())
    with open("database.json", 'r+') as file:
            data = json.load(file)
            players = data[PLAYERS]
            tournaments = data[TOURNAMENTS]
            #Check if players and tournaments id are real and stored in database
            if  is_player_existing(player_id, players) and is_tournament_existing(tournament_id, tournaments):
                #Check if player is already present in the tournament
                selected_tournament = tournaments[tournament_id]
                if any(registred_player == player_id for registred_player in selected_tournament['list_registered_players']):
                    print(f"Player with id {player_id} already added to this tournament with id {tournament_id}")
                else:
                    selected_tournament['list_registered_players'].append(player_id)
                    file.seek(0)
                    json.dump(data, file, indent=4)
                    print(f"Player with id {player_id} has been added to this tournament with id {tournament_id}")
