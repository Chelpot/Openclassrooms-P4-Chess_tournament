import json
import copy
from tabulate import tabulate
from operator import attrgetter, itemgetter
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


def display_players(list_players):
    """Display a list of all players in DB sorted by alphabetical order."""
    # We sort by alphabetical order on first name
    clean_list = []
    for p in list_players:
        clean_list.append([
            p.last_name,
            p.first_name,
            p.birth_date,
            p.national_chess_id,
            p.id
        ])

    headers = ["Nom", "Prénom", "Date de naissance", "Identifiant national d'échec", "ID"]
    print("\nListe des joueurs : \n")
    print(tabulate(clean_list, headers=headers, tablefmt="mixed_grid"))


def display_tournaments(list_tournament):
    """Display a list of all tournaments sorted by ID."""
    clean_list = []

    for t in list_tournament:
        status = "Terminé" if t.current_round == t.number_of_rounds else "En cours"
        clean_list.append([
            t.name,
            t.place,
            t.starting_date,
            t.ending_date,
            t.current_round,
            t.number_of_rounds,
            t.id,
            status,
        ])

    print("\nListe des tournois : \n")
    headers = ["Nom", "Lieu", "Date de début", "Date de fin", "Round N°", "Total round", "ID", "Statut"]
    print(CONST_SEPARATOR)
    print(tabulate(clean_list, headers=headers, tablefmt="mixed_grid"))
    print(CONST_SEPARATOR)


def display_infos_for_tournament(t):
    """display informations for a given tournament."""
    status = "Terminé" if t.current_round == t.number_of_rounds else "En cours"
    tournament = [
        ["ID", t.id],
        ["Nom", t.name],
        ["Lieu", t.place],
        ["Date de début/Fin", f"{t.starting_date} ------ {t.ending_date}"],
        ["Round", f"{t.current_round} / {t.number_of_rounds}"],
        ["Statut", status],
        ["Description", t.description],
    ]
    print("\nInformations du tournoi :\n")
    print(tabulate(tournament, tablefmt="mixed_grid"))


def display_players_for_tournament(tournament, players):
    """display a list of all the players for a given tournament, the players will be sorted by alphabetical order."""
    print(f"\nListe des joueurs du tournois \"{tournament.name}\" : \n")
    print(CONST_SEPARATOR)
    display_players(players)


def display_matches_for_rounds_of_tournament(tournament, players):
    """display all rounds for a tournament, and all matches for each rounds"""
    print(f"\nListe des rounds du tournois \"{tournament.name}\" : \n")
    rounds = tournament.list_rounds
    # Display players registered in tournament
    for round in rounds:
        print(CONST_SEPARATOR)
        clean_list = [
            ["Nom", round.name],
            ["Heure de début", round.starting_date_hour],
            ["Heure de fin", round.ending_date_hour],
        ]
        print(tabulate(clean_list, tablefmt="mixed_grid"))
        print("\nRésultats aprés match : ")
        display_matches(round.matches, players)


def display_leaderboard(ranks):
    """Display the leaderboard of a tournament"""
    print(CONST_SEPARATOR)
    print("\nClassement : ")
    for line in ranks:
        print(line)


def display_matches(list_matches, players):
    """Display some matches"""
    matches = copy.deepcopy(list_matches)
    print("\nMatches de ce round : ")
    players_by_id = {p.id: p for p in players}
    clean_list = []
    for i, match in enumerate(matches, start=1):
        p1 = players_by_id.get(match[0][0])
        p2 = players_by_id.get(match[1][0])
        name1 = f"{p1.last_name} {p1.first_name}"
        name2 = f"{p2.last_name} {p2.first_name}"
        score1 = match[0][1]
        score2 = match[1][1]

        clean_list.append([
            f"Match {i}",
            name1,
            score1,
            name2,
            score2
        ])

    headers = ["#", "Joueur 1", "Gain au score", "Joueur 2", "Gain au score"]
    print(tabulate(clean_list, headers=headers, tablefmt="mixed_grid"))


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


def ask_exit_confirmation():
    """Ask the user for a confirmation to exit program"""
    while True:
        result = input("Êtes-vous sur de vouloir quitter le logiciel ? (Y/n)")
        if result.upper() == 'Y':
            return False
        if result.upper() == 'N':
            return True


def tournament_inscription_ended():
    """Display that inscriptions have ended"""
    print("\nInscriptions au tournois cloturées.")


def display_tournament_completed():
    """Display that the tournament is finished"""
    print("\nLe tournois est terminé.")


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
