import os
import datetime as dt
import json
import random

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
INIT_DB_JSON = {"players": [], "tournaments": []}


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
        v.display_players_for_tournament()
    if choice == "6":
        generate_next_round_for_tournament()
    # Exit
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
            # Check if the date is a correct one
            try:
                dt.datetime(year_date, month_date, day_date)
            except ValueError:
                is_correct = False
    return is_correct


def is_national_chess_id_correct(id: str):
    """Check if id follow the layout AB12345"""
    return id[:2].isalpha() and id[5:].isnumeric() and len(id) == 7


def create_player():
    """Create a player"""
    data = v.ask_player_info_for_creation()
    # Check if first name is long enough
    if len(data['first_name']) >= 3:
        # Check if last name is long enough
        if len(data['last_name']) >= 3:
            # Check if birthdate is correct
            if is_birthdate_correct(data['birth_date']):
                # Check if national chess id is correct
                if is_national_chess_id_correct(data['national_chess_id']):
                    try:
                        player = Player(data['first_name'],
                                        data['last_name'],
                                        data['birth_date'],
                                        data['national_chess_id'])
                        save(PLAYERS, player)
                    except TypeError as error:
                        print(error)
                    except Exception as error:
                        print(error)


def save(model_name, item_to_save):
    """Save an object in a Json database with a unique ID"""
    with open(DB_FILE_NAME, 'r+') as file:
        data = json.load(file)
        """
        We take the last gived ID and add 1 to it to make sure no object
        from the same class are equal by id
        """
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
        tournament = Tournament(data['name'],
                                data['place'],
                                data['starting_date'],
                                data['ending_date'],
                                data['number_of_rounds'],
                                data['description'])
        adding_players = True
        while adding_players:
            player_id = v.ask_player_id()
            if player_id.isnumeric():
                player_id = int(player_id)
                if is_player_valid_for_registration(player_id, tournament):
                    tournament.list_registered_players.append(player_id)
                print("******************************************************")
                if input("Voulez vous inscrire un autre joueur au tournois"
                         + f"\"{tournament.name}\" ? " +
                         "(N pour clôturer) : ").capitalize() == "N":
                    adding_players = False
                    print("Inscriptions au tournois cloturées")
            else:
                print("Saisie incorrecte !")

        save(TOURNAMENTS, tournament)

    except TypeError as error:
        print(error)
    except Exception as error:
        print(error)


def generate_next_round_for_tournament():
    try:
        tournament_id = int(v.ask_tournament_id())
    except ValueError:
        print("Veuillez entrer l'identifiant du tournois !")

    try:

        # Change ending date for last round of this tournament
        with open(DB_FILE_NAME, 'r+') as file:
            data = json.load(file)
            tournaments = data[TOURNAMENTS]
            list_rounds = data[TOURNAMENTS][tournament_id][ROUND_LIST]
            # >1 because we check it after adding a round to the tournament
            if len(list_rounds) > 0:
                round = tournaments[tournament_id][ROUND_LIST][-1]
                round["ending_date_hour"] = dt.datetime.now().strftime("%d-%d-%Y %H:%M")
                file.seek(0)
                json.dump(data, file, indent=4)

        # Generate next round
        with open(DB_FILE_NAME, 'r+') as file:
            data = json.load(file)
            tournaments = data[TOURNAMENTS]
            if is_tournament_existing(tournament_id, tournaments):
                next_round_number = len(tournaments[tournament_id][ROUND_LIST]) + 1
                create_round(next_round_number, tournament_id)
    except UnboundLocalError as e:
        print(e)
        print("Le tournois choisi n'existe pas !")


def create_round(round_number, tournament_id):
    """Create a round for a given tournament"""
    matches = []
    try:
        now = dt.datetime.now().strftime("%d-%d-%Y %H:%M")
        round = Round(f"Round {round_number}", now, UNDEFINED, matches)
        matches = generate_matches(tournament_id)
        round.matches = matches
        save_round_in_tournament(round, tournament_id)
    except TypeError as error:
        print(error)
    except Exception as error:
        print(error)


def generate_matches(tournament_id):
    with open(DB_FILE_NAME, 'r+') as file:
        data = json.load(file)
        tournament = data[TOURNAMENTS][tournament_id]
        list_players = tournament["list_registered_players"]
        availables_players = [int(i) for i in list_players]
        list_matches = []
        list_rounds = []
        last_round_matches = []
        dict_matchups = {key: [] for key in list_players}
        for round in tournament[ROUND_LIST]:
            list_rounds.append(round)
            # Generate list of matchups by players id
            matches = round["matches"]
            print(f"matches pour le round {round['name']}")
            for match in matches:
                print(match)
                dict_matchups[match[0][0]].append(match[1][0])
                dict_matchups[match[1][0]].append(match[0][0])
        # Generate matches for the first round
        if len(list_rounds) == 0:
            for i in range(0, len(list_players)//2):
                first_player = random.choice(availables_players)
                availables_players.remove(first_player)
                second_player = random.choice(availables_players)
                availables_players.remove(second_player)
                match = ([first_player, 0], [second_player, 0])
                list_matches.append(match)
        # Generate matches for other rounds
        else:
            last_round_matches = list_rounds[-1]["matches"]
            # Generate list of players with their score sorted by score
            list_tuples_player_score = []
            for match in last_round_matches:
                list_tuples_player_score.append(match[0])
                list_tuples_player_score.append(match[1])
            list_tuples_player_score.sort(key=sort_player_scores, reverse=True)
            # Generate next match
            for player in list_tuples_player_score:
                if len(availables_players) != 0:
                    player_id = player[0]
                    if player_id in availables_players:
                        availables_players.remove(player_id)
                        for opponent in list_tuples_player_score:
                            opponent_id = opponent[0]
                            if (opponent_id not in dict_matchups[player_id] and
                                    opponent_id in availables_players):
                                availables_players.remove(opponent_id)
                                match = (player, opponent)
                                list_matches.append(match)
                                break
            v.display_leaderboard(list_tuples_player_score)
            v.display_matches(list_matches)
        list_matches = get_round_results(list_matches)
        return list_matches


def sort_player_scores(elem):
    return elem[1]


def get_round_results(list_matches):
    for match in list_matches:
        v.ask_match_result(match)
        answer_correct = False
        while not answer_correct:
            answer = input("Resultat : ")
            if answer.capitalize() in "GDE":
                answer_correct = True
                if answer.capitalize() == "G":
                    match[0][1] += 1
                if answer.capitalize() == "D":
                    match[1][1] += 1
                if answer.capitalize() == "E":
                    match[0][1] += 0.5
                    match[1][1] += 0.5
            else:
                print("Saisie incorrecte")
    return list_matches


def save_round_in_tournament(item_to_save, tournament_id):
    with open(DB_FILE_NAME, 'r+') as file:
        data = json.load(file)
        round_list = data[TOURNAMENTS][tournament_id][ROUND_LIST]
        # We take the last gived ID and add 1 to it to make sure no object
        # from the same class are equal by id
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


def is_player_valid_for_registration(player_id, tournament):
    """Check if the player id is existing and if it's not already registered"""
    with open(DB_FILE_NAME, 'r+') as file:
        data = json.load(file)
        players = data[PLAYERS]
        # Check if players is real and stored in database
        if is_player_existing(player_id, players):
            if player_id in tournament.list_registered_players:
                print(f"Player with id {player_id} already added")
            else:
                print(f"Player with id {player_id} has been added")
                return True
        else:
            print(f"Player with id {player_id} doesn\'t exist")
        file.close()
    return False
