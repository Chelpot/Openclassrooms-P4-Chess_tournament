import json
from operator import itemgetter

SEPARATOR = ""

menu_options = {
            1: 'Créer un nouveau joueur',
            2: 'Créer un nouveau tournois',
            3: 'Générer un round pour un tournois',
            4: 'Rapport : Afficher la liste des joueurs',
            5: 'Rapport : Afficher la liste des tournois',
            6: 'Rapport : Afficher les joueurs d\'un tournois',
            7: 'Rapport : liste des rounds et matches pour un tournois',
            8: 'Quitter'
        }


def display_welcoming_message():
    print("\n*************************************************")
    print("*   Bienvenue, vous utilisez actuellement un    *")
    print("*  logiciel permettant de gérer les tournois du *")
    print("*                 club d'échec.                 *")
    print("*************************************************")


def display_action_pannel():
    print("\n*************************************************")
    print("Entrez le numéro de l'action que vous souhaitez entreprendre :")
    for option in menu_options:
        print(f"{option}: {menu_options[option]}")

    answer = input()
    if answer in str(menu_options.keys()):
        return answer
    else:
        print("\n/!\\/!\\/!\\/!\\/!\\/!\\")
        print("Réponse incorrecte")
        print("/!\\/!\\/!\\/!\\/!\\/!\\")
        return None


def ask_player_info_for_creation():
    """Ask the player with a form for informations needed to create a Player"""
    is_valid = False
    while not is_valid:
        data = {}
        print("Prénom : ")
        data['first_name'] = input()
        print("Nom : ")
        data['last_name'] = input()
        print("Date de naissance (JJ/MM/AAAA) : ")
        data['birth_date'] = input()
        print("Identifiant national d'échecs : ")
        data['national_chess_id'] = input()
        print("Validez vous les informations ? Y/N : ")
        if input().capitalize() == 'Y':
            is_valid = True
            return data
        else:
            return None


def ask_tournament_info_for_creation():
    """Ask the user informations to create a tournament"""
    is_valid = False
    while not is_valid:
        data = {}
        print("Lieu : ")
        data['place'] = input()
        print("Nom du tournois : ")
        data['name'] = input()
        print("Date de commencement : ")
        data['starting_date'] = input()
        print("Date de fin : ")
        data['ending_date'] = input()
        print("Nombre de tours : (Facultatif 4 par défaut)")
        data['number_of_rounds'] = input()
        print("Description du tournois : (Facultatif)")
        data['description'] = input()
        print("Validez vous les informations ? Y/N : ")
        if input() == 'Y':
            is_valid = True
            return data
        else:
            return None


def display_players():
    """Display a list of all players in DB sorted by alphabetical order."""
    with open("database.json", 'r+') as file:
        data = json.load(file)
        players = data["players"]
        print("\nListe des joueurs : \n")
        print("ID | Prénom | Nom | Date de naissance | Identifiant national d'échec")
        print("**********************************************************************")
        for p in players:
            print(f'{p["id"]} | {p["first_name"]} | {p["last_name"]} | {p["birth_date"]} | {p["national_chess_id"]}')
        print("**********************************************************************")


def display_tournaments():
    """Display a list of all tournaments."""
    with open("database.json", 'r+') as file:
        data = json.load(file)
        tournaments = data["tournaments"]
        print("\nListe des tournois : \n")
        print("ID | Nom | Lieu | Date de début | Date de fin | Description")
        print("**********************************************************************")
        for t in tournaments:
            print(f'{t["id"]} | {t["name"]} | {t["starting_date"]} | {t["ending_date"]} | {t["description"]}')
        print("**********************************************************************")


def display_infos_for_tournament(tournament):
    """display informations for a given tournament."""
    pass


def display_players_for_tournament():
    """display a list of all the players for a given tournament, the players will be sorted by alphabetical order."""
    with open("database.json", 'r+') as file:
        data = json.load(file)
        id = input("Saisissez l'identifiant du tournois : ")
        while not id.isnumeric():
            id = input("Saisissez l'identifiant du tournois : ")
        tournament = [t for t in data["tournaments"] if str(t["id"]) == id]
        if not tournament:
            print(f"Le tournois numéro {id} n'existe pas.")
        else:
            tournament = tournament[0]
            print(f"\nListe des joueurs du tournois \"{tournament['name']}\" : \n")
            print("ID | Prénom | Nom | Date de naissance | Identifiant national d'échec")
            print("**********************************************************************")
            players = sorted(data["players"], key=itemgetter('last_name'))
            # Display players registered in tournament
            for p in players:
                if p["id"] in tournament["list_registered_players"]:
                    print(f'{p["id"]} | {p["first_name"]} | {p["last_name"]} | {p["birth_date"]} | {p["national_chess_id"]}')


def display_matches_for_rounds_of_tournament():
    """display all rounds for a tournament, and all matches for each rounds"""
    with open("database.json", 'r+') as file:
        data = json.load(file)
        id = input("Saisissez l'identifiant du tournois : ")
        while not id.isnumeric():
            id = input("Saisissez l'identifiant du tournois : ")
        tournament = [t for t in data["tournaments"] if str(t["id"]) == id]   
        if not tournament:
            print(f"Le tournois numéro {id} n'existe pas.")
        else:
            tournament = tournament[0]
            print(f"\nListe des rounds du tournois \"{tournament['name']}\" : \n")
            print("**********************************************************************")
            rounds = tournament["list_rounds"]
            # Display players registered in tournament
            for round in rounds:
                print(f"{round['name']}, {round['starting_date_hour']} - {round['ending_date_hour']}")
                print("Résultats aprés match : ")
                for match in round["matches"]:
                    print(match)


def display_leaderboard(list_player_score):
    print("\n**********************************************************************")
    print("\nClassement : ")
    for index, rank in enumerate(list_player_score):
        print(f"{index+1} : {rank}")


def display_matches(list_matches):
    print("\nMatches de ce round : ")
    for match in list_matches:
        print(match)


def ask_player_id():
    return input("Entrez l'ID du joueur que vous voulez inscrire au tournois : \n")


def ask_tournament_id():
    print("**********************************************************************")
    return input("\nEntrez l'ID du tournois à sélectionner : \n")


def ask_match_result(match):
    print("\n**********************************************************************")
    print("Quel est le résultat de ce match ?")
    print(match)
    print("G pour victoire du joueur de gauche")
    print("D pour victoire du joueur de droite")
    print("E pour égalité")
