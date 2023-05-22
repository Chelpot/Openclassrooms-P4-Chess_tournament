
import datetime as dt

from view import global_view as v
from models.player import Player
from models.tournament import Tournament
from models.turn import Turn

def launch():
    running = True
    v.display_welcoming_message()
    while running:
        v.display_action_pannel()
        choice = input()
        running = call_function(choice)


def call_function(choice):
    if choice == "1":
        create_player()
    if choice == "2":
        create_tournament()
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
    if len(data[0]) >= 3:
        #Check if last name is long enough
        if len(data[1]) >= 3:
            #Check if birthdate is correct
            if is_birthdate_correct(data[2]):
                #Check if national chess id is correct
                if is_national_chess_id_correct(data[3]):
                    try:
                        Player(data[0], data[1], data[2], data[3])
                    except TypeError as error:
                        print(error)


def create_tournament():
    """Create a tournament"""
    data = v.ask_tournament_info_for_creation()
    try:
        Tournament(data['name'], data['place'], data['starting_date'], data['ending_date'], data['description'])
    except TypeError as error:
        print(error)