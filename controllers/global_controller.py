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
    if choice == "1-1":
        create_player()
    if choice == "1-2":
        create_tournament()
    if choice == "1-3":
        v.display_tournaments()
        resume_tournament_scoring()
    if choice == "2-1":
        v.display_players()
    if choice == "2-2":
        v.display_tournaments()
    if choice == "2-3":
        v.display_tournaments()
        v.display_players_for_tournament()
    if choice == "2-4":
        v.display_tournaments()
        v.display_infos_for_tournament()
    if choice == "2-5":
        v.display_tournaments()
        v.display_matches_for_rounds_of_tournament()
    if choice == "2-6":
        v.display_tournaments()
        v.display_leaderboard(v.ask_tournament_id())
    # Exit
    if choice == "1-4" or choice == "2-7" or choice =="3":
        return v.ask_exit_confirmation()
    return True

def resume_tournament_scoring():
    id = v.ask_tournament_id()
    if not is_tournament_finished(id):
        if is_last_round_scoring_saved(id):
            generate_next_round_for_tournament(id)
        resume_match_scoring(id)
    else:
        v.tournament_completed()
        v.display_leaderboard(id)
        

def is_tournament_finished(id):
    with open(DB_FILE_NAME, 'r+') as file:
        data = json.load(file)
        tournament = data[TOURNAMENTS][id]
    if (tournament["current_round"] >= tournament["number_of_rounds"] and
        tournament[ROUND_LIST][-1]["ending_date_hour"] != UNDEFINED):
        return True
    return False


def is_birthdate_correct(birthdate: str):
    """Check if birthdate follow the layout DD/MM/YYYY and is a valid date"""
    is_correct = True
    if len(birthdate) == 10 and birthdate.count("/") == 2:
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
    if len(data['first_name']) < 2:
        print("Prénom trop court (2 lettre minimum)")
        return
    # Check if last name is long enough
    if len(data['last_name']) < 2:
        print("Nom trop court (2 lettre minimum)")
        return
    # Check if birthdate is correct
    if is_birthdate_correct(data['birth_date']):
        print("Date de naissance incorrecte")
        return
    # Check if national chess id is correct
    if is_national_chess_id_correct(data['national_chess_id']):
        try:
            player = Player(data['first_name'],
                            data['last_name'],
                            data['birth_date'],
                            data['national_chess_id'])
            save(PLAYERS, player)
            return
        except TypeError as error:
            print(error)
        except Exception as error:
            print(error)
    else:
        print("Identifiant national d'échecs incorrect.")
    v.player_creation_issue()


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
        return item_to_save.id


def create_tournament():
    """Create a tournament"""
    data = v.ask_tournament_info_for_creation()
    try:
        tournament = Tournament(data['name'],
                                data['place'],
                                data['starting_date'],
                                data['ending_date'],
                                int(data['number_of_rounds']),
                                data['description'])
        adding_players = True
        # Players registration
        while adding_players:
            v.display_players()
            player_id = v.ask_player_id()
            if player_id.isnumeric():
                player_id = int(player_id)
                if is_player_valid_for_registration(player_id, tournament):
                    tournament.list_registered_players.append(player_id)
            else:
                if player_id.lower() == "terminer":
                    adding_players = False
                    v.tournament_inscription_ended()
                else:
                    v.display_incorrect_action()
        id = save(TOURNAMENTS, tournament)
        generate_next_round_for_tournament(id)
        resume_match_scoring(id)
    except TypeError as error:
        v.display_incorrect_action()
    except Exception as error:
        print(error)

def is_last_round_scoring_saved(id):
    with open(DB_FILE_NAME, 'r+') as file:
        data = json.load(file)
        tournament = data[TOURNAMENTS][id]
        if len(tournament[ROUND_LIST]) > 1:
            current_round = tournament[ROUND_LIST][-1]
            # We can't have 2 similar match, so if it appear it mean score were not saved
            if current_round["ending_date_hour"] == UNDEFINED:
                return False
            else:
                return True
        else:
            #If first match score are 0 vs 0 then it was not saved
            first_match = tournament[ROUND_LIST][0]["matches"][0]
            if first_match[0][1] == 0 == first_match[1][1]:
                return False
            else:
                return True
            

def resume_match_scoring(id):
    with open(DB_FILE_NAME, 'r+') as file:
        data = json.load(file)
        tournament = data[TOURNAMENTS][id]
        list_matches = tournament[ROUND_LIST][-1]["matches"]
        get_round_results(list_matches)
        data[TOURNAMENTS][id][ROUND_LIST][-1]["matches"] = list_matches
        # Change ending date for last round of this tournament
        file.seek(0)
        json.dump(data, file, indent=4)
        file.close()
    save_ending_hour_for_round(id)


def save_ending_hour_for_round(tournament_id):
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

def generate_next_round_for_tournament(tournament_id = None):
    try:
        if not tournament_id:
            tournament_id = v.ask_tournament_id()
    except ValueError:
        print("Veuillez entrer l'identifiant du tournois !")
    try:
        # Generate next round
        with open(DB_FILE_NAME, 'r+') as file:
            data = json.load(file)
            tournaments = data[TOURNAMENTS]
            if is_tournament_existing(tournament_id, tournaments):
                if is_tournament_finished(tournament_id):
                    v.tournament_completed()
                    v.display_leaderboard(tournament_id)
                else:
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

def generate_first_matches(list_players, availables_players):
    list_matches = []
    for i in range(0, len(list_players)//2):
                    first_player = random.choice(availables_players)
                    availables_players.remove(first_player)
                    second_player = random.choice(availables_players)
                    availables_players.remove(second_player)
                    match = ([first_player, 0], [second_player, 0])
                    list_matches.append(match)
    return list_matches
    

def generate_matchups_list(list_players, round_list):
    dict_matchups = {key: [] for key in list_players}
    for round in round_list:
        # Generate list of matchups by players id
        matches = round["matches"]
        print(f"matches pour le round {round['name']}")
        for match in matches:
            print(match)
            dict_matchups[match[0][0]].append(match[1][0])
            dict_matchups[match[1][0]].append(match[0][0])
    return dict_matchups


def generate_leaderboard(matches):
    list_tuples_player_score = []
    for match in matches:
        list_tuples_player_score.append(match[0])
        list_tuples_player_score.append(match[1])
    list_tuples_player_score.sort(key=sort_player_scores, reverse=True)
    return list_tuples_player_score


def generate_match(availables_players, list_tuples_player_score, dict_matchups):
    list_matches = []
    score_index_list_of_player_id = {}
    # Init a dict where each key is a score, and player are attributed by score
    for line in list_tuples_player_score:
        score_index_list_of_player_id.setdefault(line[1], []).append(line[0])
    for player in list_tuples_player_score:
        if len(availables_players) == 0:
            break
        player_id = player[0]
        if player_id in availables_players:
            availables_players.remove(player_id)
            # Remove every player from potential opponent in next matches
            score_index_list_of_player_id[player[1]].remove(player[0])
            for opponent in list_tuples_player_score:
                # Check if opponent have other players with same score
                # If there is more than 1 potential opponent
                if len(score_index_list_of_player_id[player[1]]) > 1:
                    for confronted_opponent in dict_matchups[opponent[0]]:
                        # Make remove past contestants
                        if confronted_opponent in score_index_list_of_player_id[player[1]]:
                            score_index_list_of_player_id[player[1]].remove(confronted_opponent)
                    # If there is no potential opponnent, we take the next available by descending score
                    if len(score_index_list_of_player_id[player[1]]) > 0:
                        choice = random.choice(score_index_list_of_player_id[player[1]])
                        availables_players.remove(choice)
                        final_opponent = [t for t in list_tuples_player_score if t[0] == choice][0]
                        match = (player, final_opponent)
                        print(match)
                        list_matches.append(match)
                        break
                    
                opponent_id = opponent[0]
                # Default match association with next in leaderboard by descending score
                if (opponent_id not in dict_matchups[player_id] and opponent_id in availables_players):
                    availables_players.remove(opponent_id)
                    match = (player, opponent)
                    list_matches.append(match)
                    break
    return list_matches

        
def generate_matches(tournament_id):
    with open(DB_FILE_NAME, 'r+') as file:
        data = json.load(file)
        tournament = data[TOURNAMENTS][tournament_id]
        list_players = tournament["list_registered_players"]
        availables_players = [int(i) for i in list_players]
        list_matches = []
        list_rounds = [ r for r in tournament[ROUND_LIST]]
        dict_matchups = generate_matchups_list(list_players, tournament[ROUND_LIST])
        # Generate matches for the first round
        if len(list_rounds) == 0:
            list_matches = generate_first_matches(list_players, availables_players)
        # Generate matches for other rounds
        else:
            # Generate list of players with their score sorted by score
            last_round_matches = list_rounds[-1]["matches"]
            list_tuples_player_score = generate_leaderboard(last_round_matches)
            # Generate next match
            list_matches = generate_match(availables_players, list_tuples_player_score, dict_matchups)
            v.display_leaderboard(tournament_id)
        v.display_matches(list_matches)
        data[TOURNAMENTS][tournament_id]["current_round"] += 1
        file.seek(0)
        json.dump(data, file, indent=4)
        file.close()
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
                v.display_incorrect_action()
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
    if (not os.path.isfile(DB_FILE_NAME)):
        with open(DB_FILE_NAME, 'w') as fp:
            json.dump(INIT_DB_JSON, fp, indent=4)

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

