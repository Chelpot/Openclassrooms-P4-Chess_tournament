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
    """Main loop running the program"""
    running = True
    v.display_welcoming_message()
    init_database()
    while running:
        choice = v.display_action_pannel()
        running = call_function(choice)


def call_function(choice):
    """Call corresponding function depending of the argument."""
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
        v.display_infos_for_tournament(v.ask_tournament_id())
        
    if choice == "2-5":
        v.display_tournaments()
        id = v.ask_tournament_id()
        v.display_matches_for_rounds_of_tournament(id)
        if is_tournament_finished(id):
            v.display_tournament_completed()
    if choice == "2-6":
        v.display_tournaments()
        id = v.ask_tournament_id()
        v.display_leaderboard(id)
        if is_tournament_finished(id):
            v.display_tournament_completed()
    # Exit
    if choice == "1-4" or choice == "2-7" or choice =="3":
        return v.ask_exit_confirmation()
    return True

def resume_tournament_scoring():
    """resume tournament scoring where it was left
    
    will generate next round if tournament not finished
    """
    id = v.ask_tournament_id()
    if is_tournament_existing(id):
        if not is_tournament_finished(id):
            if is_last_round_scoring_saved(id):
                generate_next_round_for_tournament(id)
            finalize_round_scoring(id)
        else:
            v.display_leaderboard(id)
            v.display_tournament_completed()
    else:
        v.display_tournament_do_not_exist

def is_tournament_finished(id):
    with open(DB_FILE_NAME, 'r+') as file:
        data = json.load(file)
        tournament = data[TOURNAMENTS][id]
    if (tournament["current_round"] >= tournament["number_of_rounds"] and
        tournament[ROUND_LIST][-1]["ending_date_hour"] != UNDEFINED):
        return True
    return False


def is_date_correct(date: str):
    """Check if date follow the layout DD/MM/YYYY and is a valid date. Return True if correct"""
    is_correct = True
    if len(date) == 10 and date.count("/") == 2:
        splited_date = date.split("/")
        day_date = int(splited_date[0])
        month_date = int(splited_date[1])
        year_date = int(splited_date[2])
        # Check if the date is a correct one
        try:
            dt.datetime(year_date, month_date, day_date)
        except ValueError:
            is_correct = False
    else:
        is_correct = False
    return is_correct


def is_national_chess_id_correct(id: str):
    """Check if id follow the layout AB12345"""
    return id[:2].isalpha() and id[5:].isnumeric() and len(id) == 7


def create_player():
    """Create a player while checking if arguments for creation are correct"""
    data = v.ask_player_info_for_creation()
    nb_error = 0
    # Check if first name is long enough
    if len(data['first_name']) < 2:
        print("Prénom trop court (2 lettre minimum)")
        nb_error+=1
    # Check if last name is long enough
    if len(data['last_name']) < 2:
        print("Nom trop court (2 lettre minimum)")
        nb_error+=1
    # Check if birthdate is correct
    if not is_date_correct(data['birth_date']):
        v.display_date_incorrect()
        nb_error+=1
    # Check if national chess id is correct
    if not is_national_chess_id_correct(data['national_chess_id']):
        print("Identifiant national d'échecs incorrect")
        nb_error+=1
    if nb_error == 0:
        player = Player(data['first_name'],
                        data['last_name'],
                        data['birth_date'],
                        data['national_chess_id'])
        save(PLAYERS, player)
        return

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
    """Create a tournament
    
     Register players, generate first round, then ask for scoring
    """
    data = v.ask_tournament_info_for_creation()
    if not is_date_correct(data["starting_date"]) or not is_date_correct(data["ending_date"]):
        display_incorrect_action

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
    finalize_round_scoring(id)

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
            

def finalize_round_scoring(id):
    with open(DB_FILE_NAME, 'r+') as file:
        data = json.load(file)
        tournament = data[TOURNAMENTS][id]
        list_matches = tournament[ROUND_LIST][-1]["matches"]
        list_matches = get_round_results(list_matches)
        # Change ending date for last round of this tournament
        file.seek(0)
        json.dump(data, file, indent=4)
        file.close()
    save_ending_hour_for_round(id)


def save_ending_hour_for_round(tournament_id):
    with open(DB_FILE_NAME, 'r+') as file:
            data = json.load(file)
            tournament = data[TOURNAMENTS][tournament_id]
            list_rounds = tournament[ROUND_LIST]
            if len(list_rounds) > 0:
                list_rounds[-1]["ending_date_hour"] = dt.datetime.now().strftime("%d-%m-%Y %H:%M")
                file.seek(0)
                json.dump(data, file, indent=4)

def generate_next_round_for_tournament(tournament_id = None):
    if not tournament_id:
        tournament_id = v.ask_tournament_id()
    # Generate next round
    tournaments = get_tournaments()
    if is_tournament_existing(tournament_id):
        if is_tournament_finished(tournament_id):
            v.display_leaderboard(tournament_id)
            v.display_tournament_completed()
        else:
            next_round_number = tournaments[tournament_id]["current_round"] + 1
            create_round(next_round_number, tournament_id)

def create_round(round_number, tournament_id):
    """Create a round for a given tournament"""
    matches = []
    try:
        now = dt.datetime.now().strftime("%d-%m-%Y %H:%M")
        round = Round(f"Round {round_number}", now, UNDEFINED, matches)
        matches = generate_round(tournament_id)
        round.matches = matches
        save_round_in_tournament(round, tournament_id)
    except TypeError as error:
        print(error)
    except Exception as error:
        print(error)

def generate_first_matches(availables_players):
    """Generate first round of matches randomly and return a list of matches"""
    list_matches = []
    for i in range(0, len(availables_players)//2):
        first_player = random.choice(availables_players)
        availables_players.remove(first_player)
        second_player = random.choice(availables_players)
        availables_players.remove(second_player)
        match = ([first_player, 0], [second_player, 0])
        list_matches.append(match)
    return list_matches
    

def generate_matchups_list(list_2players, round_list):
    """Return a dict where each player id have a list of opponent already faced in previous rounds"""
    dict_matchups = {key: [] for key in list_players}
    for round in round_list:
        # Generate list of matchups by players id
        matches = round["matches"]
        print(f"résultats des matchs à l'issue du round {round['name']}")
        for match in matches:
            print(match)
            dict_matchups[match[0][0]].append(match[1][0])
            dict_matchups[match[1][0]].append(match[0][0])
    return dict_matchups


def generate_leaderboard(matches):
    """Generate a list of players with their score sorted by score in descending order"""
    list_tuples_player_score = []
    for match in matches:
        list_tuples_player_score.append(match[0])
        list_tuples_player_score.append(match[1])
    #Sort the list of [players, scores] by score and descending order
    list_tuples_player_score.sort(key=sort_player_scores, reverse=True)
    return list_tuples_player_score

def sort_player_scores(elem):
    return elem[1]

def generate_round_matches(leaderboard, dict_matchups):
    """generate all matches for the round. Return a list of match"""
    list_matches = []
    list_player_already_matched = []
    for player in leaderboard:
        if player not in list_player_already_matched:
            for opponent in leaderboard:
                if opponent not in list_player_already_matched and player!=opponent:
                    if opponent[0] not in dict_matchups[player[0]]:
                        list_player_already_matched.append(player)
                        list_player_already_matched.append(opponent)
                        list_matches.append((player, opponent))
                        break
    #If there is some player that can't be matched with a not already met opponent
    for player in leaderboard:
        for opponent in leaderboard:
            if player != opponent and len([match for match in list_matches if player in match or opponent in match]) == 0:
                list_matches.append((player, opponent))
                break
    return list_matches

        
def generate_round(tournament_id):
    """Generate and save the matches for the next round to play. Return a list of matches"""
    with open(DB_FILE_NAME, 'r+') as file:
        data = json.load(file)
        tournament = data[TOURNAMENTS][tournament_id]
        list_players_id = tournament["list_registered_players"].copy()
        list_matches = []
        list_rounds = [ r for r in tournament[ROUND_LIST]]
        dict_matchups = generate_matchups_list(list_players_id, tournament[ROUND_LIST])
        # Generate matches for the first round
        if len(list_rounds) == 0:
            list_matches = generate_first_matches(list_players_id)
        # Generate matches for other rounds
        else:
            # Generate list of players with their score sorted by score
            last_round_matches = list_rounds[-1]["matches"]
            leaderboard = generate_leaderboard(last_round_matches)
            # Generate next matches
            list_matches = generate_round_matches(leaderboard, dict_matchups)
            v.display_leaderboard(tournament_id)
        v.display_matches(list_matches)
        data[TOURNAMENTS][tournament_id]["current_round"] += 1
        file.seek(0)
        json.dump(data, file, indent=4)
        file.close()
        return list_matches




def get_round_results(list_matches):
    """ask the user for the scoring and return a list of matches with score updated"""
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

def is_player_existing(player_id):
    players = get_players()
    return any(p['id'] == player_id for p in players)


def is_tournament_existing(tournament_id):
    tournaments = get_tournaments()
    return any(t['id'] == tournament_id for t in tournaments)

def get_tournaments():
    with open(DB_FILE_NAME, 'r+') as file:
        data = json.load(file)
        tournaments = data[TOURNAMENTS]
        return tournaments
    
def get_players():
    with open(DB_FILE_NAME, 'r+') as file:
        data = json.load(file)
        players = data[PLAYERS]
        return players


def is_player_valid_for_registration(player_id, tournament):
    """Check if the player id is existing and if it's not already registered"""
    # Check if players is real and stored in database
    if is_player_existing(player_id):
        if player_id in tournament.list_registered_players:
            print(f"Le joueur avec l'id \"{player_id}\" est déja inscrit.")
        else:            
            print(f"Le joueur avec l'id \"{player_id}\" est maintenant inscrit.")
            return True
    else:
        print(f"Le joueur avec l'id \"{player_id}\" n'existe pas.")
    return False

