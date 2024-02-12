import json
import copy
from tabulate import tabulate
from operator import itemgetter
import controllers.global_controller as gc

CONST_SEPARATOR = "\n*************************************************"
DB_FILE_NAME = "database.json"

menu_home = {
    1: 'Gestion',
    2: 'Rapports',
    3: 'Quitter',

}

menu_gestion = {
    1: 'Créer un nouveau joueur',
    2: 'Créer un nouveau tournois',
    3: 'Continuer un tournois',
    4: 'Quitter',

}

menu_rapport = {
    1: 'Afficher la liste des joueurs',
    2: 'Afficher la liste des tournois',
    3: 'Afficher la liste des joueurs inscrits à un tournois',
    4: 'Afficher les informations pour un tournois',
    5: 'Afficher la liste des rounds et matches pour un tournois',
    6: 'Afficher le classement pour un tournois',
    7: 'Quitter',
}


def display_welcoming_message():
    """Display a welcoming message"""
    print("\n*************************************************")
    print("*   Bienvenue, vous utilisez actuellement un    *")
    print("*  logiciel permettant de gérer les tournois du *")
    print("*                 club d'échec.                 *")
    print("*************************************************")


def display_action_pannel():
    """Display a menu to let the user choose from"""
    print(CONST_SEPARATOR)
    print("Que souhaitez vous faire ? (Entrez un chiffre correspondant à votre choix)")
    print("1: Gestion\n2: Rapport\n3: Quitter")
    menu_answer = input()
    menu_choice = "None"
    if menu_answer == "1":
        menu_choice = menu_gestion
    if menu_answer == "2":
        menu_choice = menu_rapport
    if menu_answer == "3":
        return menu_answer
    if menu_choice != "None":
        print("Entrez le numéro de l'action que vous souhaitez utiliser : ")
        for option in menu_choice:
            print(f"{option}: {menu_choice[option]}")
        answer = input()
        if answer in str(menu_choice.keys()):
            return "{}-{}".format(menu_answer, answer)
    display_incorrect_action()
    return menu_answer


def display_incorrect_action():
    """Inform the user that the input is not correct"""
    print("\n/!\\/!\\/!\\/!\\/!\\/!\\")
    print("Saisie incorrecte")
    print("/!\\/!\\/!\\/!\\/!\\/!\\")


def player_creation_issue():
    """The player was not created because of invalid inputs"""
    print("La création du joueur a été annulée car des données sont invalides.")


def tournament_creation_issue():
    """The tournament was not created because of invalid inputs"""
    print("La création du tournois a été annulée car des données sont invalides.")


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
        print("Identifiant national d'échecs (AB12345) : ")
        data['national_chess_id'] = input()
        print("Validez vous les informations ? Y/n : ")
        if input().capitalize() == 'Y':
            is_valid = True
            return data


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
        print("Validez vous les informations ? Y/n : ")
        if input().upper() == 'Y':
            is_valid = True
            return data
        else:
            return None


def display_players():
    """Display a list of all players in DB sorted by alphabetical order."""
    with open(DB_FILE_NAME, 'r+') as file:
        data = json.load(file)
        players = data["players"]
        list_players = [list(d.values()) for d in players]
        display_tabulate_players(list_players)


def display_tournaments():
    """Display a list of all tournaments."""
    with open(DB_FILE_NAME, 'r+') as file:
        data = json.load(file)
        tournaments = data["tournaments"]
        list_tournament = [list(d.values()) for d in tournaments]
        for t in list_tournament:
            if t[5] == t[6]:
                t.append("Terminé")
            else:
                t.append("En cours")
            # We exclude data we do not want to be displayed
            # Description / List of rounds / List of players registered
            t.pop(4)
            t.pop(6)
            t.pop(6)

        print("\nListe des tournois : \n")
        headers = ["Nom", "Lieu", "Date de début", "Date de fin", "Round N°", "Total round", "ID", "Statut"]
        print(CONST_SEPARATOR)
        print(tabulate(list_tournament, headers=headers, tablefmt="mixed_grid"))
        print(CONST_SEPARATOR)


def display_infos_for_tournament(id):
    """display informations for a given tournament."""
    with open(DB_FILE_NAME, 'r+') as file:
        data = json.load(file)
        if not gc.is_tournament_existing(id):
            display_tournament_do_not_exist()
        else:
            t = data["tournaments"][id]
            if t["current_round"] == t["number_of_rounds"]:
                state = "Terminé"
            else:
                state = "En cours"
            print(CONST_SEPARATOR)
            print("Informations du tournois : ")
            print("id : {} | Nom : {} | Lieu : {}".format(t["id"], t["name"], t["place"]))
            print("Date de début : {} | Date de fin : {}".format(t["starting_date"], t["ending_date"]))
            print("Round : {} / {}".format(t["current_round"], t["number_of_rounds"]))
            print("Description : {}".format(t["description"]))
            print("Statut : {}".format(state))
            print(CONST_SEPARATOR)


def display_players_for_tournament():
    """display a list of all the players for a given tournament, the players will be sorted by alphabetical order."""
    with open(DB_FILE_NAME, 'r+') as file:
        data = json.load(file)
        tournament_id = ask_tournament_id()
        if not gc.is_tournament_existing(tournament_id):
            display_tournament_do_not_exist()
            return
        tournament = [t for t in data["tournaments"] if t["id"] == tournament_id]
        if not tournament:
            display_tournament_do_not_exist()
        else:
            tournament = tournament[0]
            print(f"\nListe des joueurs du tournois \"{tournament['name']}\" : \n")
            print(CONST_SEPARATOR)
            players = sorted(data["players"], key=itemgetter('last_name'))
            # Display players registered in tournament
            for p in players:
                if p["id"] in tournament["list_registered_players"]:
                    list_players = [list(d.values()) for d in players]
            display_tabulate_players(list_players)


def display_tabulate_players(list_players):
    # We sort by alphabetical order on first name
    list_players = sorted(list_players, key=itemgetter(1))
    # We swap column to have first_name in first place
    for item in list_players:
        tmp = item[0]
        item[0] = item[1]
        item[1] = tmp
    headers = ["Nom", "Prénom", "Date de naissance", "Identifiant national d'échec", "ID"]
    print("\nListe des joueurs : \n")
    print(tabulate(list_players, headers=headers, tablefmt="mixed_grid"))


def display_matches_for_rounds_of_tournament(id):
    """display all rounds for a tournament, and all matches for each rounds"""
    with open(DB_FILE_NAME, 'r+') as file:
        data = json.load(file)
        if not gc.is_tournament_existing(id):
            display_tournament_do_not_exist()
        else:
            tournament = [t for t in data["tournaments"] if t["id"] == id]
            tournament = tournament[0]
            print(f"\nListe des rounds du tournois \"{tournament['name']}\" : \n")
            rounds = tournament["list_rounds"]
            # Display players registered in tournament
            for round in rounds:
                print(CONST_SEPARATOR)
                print(f"{round['name']}, {round['starting_date_hour']} - {round['ending_date_hour']}")
                print("\nRésultats aprés match : ")
                display_matches(round["matches"])
            if gc.is_tournament_finished(id):
                display_tournament_completed()


def display_leaderboard(id):
    """Display the leaderboard of a tournament"""
    if not gc.is_tournament_existing(id):
        display_tournament_do_not_exist()
    else:
        with open(gc.DB_FILE_NAME, 'r+') as file:
            data = json.load(file)
            tournament = data[gc.TOURNAMENTS][id]
            matches = gc.generate_leaderboard(tournament[gc.ROUND_LIST])
        print(CONST_SEPARATOR)
        print("\nClassement : ")
        for index, rank in enumerate(matches):
            name = "{} {}".format(data[gc.PLAYERS][rank[0]]["last_name"], data[gc.PLAYERS][rank[0]]["last_name"])
            print(f"{index+1} : {name} - {rank[1]} points")
        if gc.is_tournament_finished(id):
            display_tournament_completed()


def display_matches(list_matches):
    """Display some matches"""
    matches = copy.deepcopy(list_matches)
    players = gc.get_players()

    print("\nMatches de ce round : ")
    for match in matches:
        # We replace Player ID with their name for more clarity
        match[0][0] = players[match[0][0]]["last_name"]
        match[1][0] = players[match[1][0]]["last_name"]
        print(match)


def ask_player_id():
    """Ask the user a player id"""
    return input("Entrez l'ID du joueur que vous voulez inscrire au tournois"
                 "\nEntrez \"terminer\" pour cloturer les inscriptions au tournois : ")


def ask_tournament_id():
    """Ask the user a tournament id"""
    print(CONST_SEPARATOR)
    while True:
        try:
            tournament_id = int(input("\nSaisissez l'identifiant du tournois : "))
            break
        except ValueError:
            print("Vous n'avez pas saisi un identifiant valide.")
    return tournament_id


def ask_match_result(match):
    """Ask the user to score the match&"""
    print(CONST_SEPARATOR)
    print("Quel est le résultat de ce match ?")
    display_matches([match])
    print("G pour victoire du joueur de gauche.")
    print("D pour victoire du joueur de droite.")
    print("E pour égalité.")


def tournament_inscription_ended():
    """Display that inscriptions have ended"""
    print("\nInscriptions au tournois cloturées.")


def display_tournament_completed():
    """Display that the tournament is finished"""
    print("\nLe tournois est terminé.")


def ask_exit_confirmation():
    """Ask the user for a confirmation to exit program"""
    while True:
        result = input("Êtes-vous sur de vouloir quitter le logiciel ? (Y/n)")
        if result.upper() == 'Y':
            return False
        if result.upper() == 'N':
            return True


def display_tournament_do_not_exist():
    """Display that the tournament do not exist"""
    print("\nL'identifiant indiqué ne correspond pas à un tournois existant.")


def display_date_incorrect():
    """Display that the date is incorrect"""
    print("\nDate incorrecte")


def display_even_number_player():
    """Display that there must be a even number of player registered"""
    print("\nIl faut impérativement un nombre de joueur pair pour le bon déroulement du tournois.")


def display_number_of_round_minimum():
    """Display that there must be at least 1 round"""
    print('\nNombre de round doit être supérieur à 1')


def display_minimum_number_player():
    """Display that there must be at least 2 players"""
    print("\nIl doit y avoir minimum 2 joueurs inscrits pour créer le tournois")
