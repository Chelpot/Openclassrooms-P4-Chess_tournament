import json
from operator import itemgetter
import controllers.global_controller as gc

menu_home = {
            1: 'Gestion',
            2: 'Rapports',
            3: 'Quitter',

}

menu_gestion = {
            1: 'Créer un nouveau joueur',
            2: 'Créer un nouveau tournois',
            3: 'Générer un round pour un tournois',
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
    print("\n*************************************************")
    print("*   Bienvenue, vous utilisez actuellement un    *")
    print("*  logiciel permettant de gérer les tournois du *")
    print("*                 club d'échec.                 *")
    print("*************************************************")


def display_action_pannel():
    print("\n*************************************************")
    print("Que souhaitez vous faire ? (Entrez un chiffre correspondant à votre choix)")
    print("1: Gestion\n2: Rapport\n3: Quitter")
    menu_answer = input()
    menu_choice = "None"
    if menu_answer == "1":
        menu_choice = menu_gestion
    if menu_answer == "2":
        menu_choice = menu_rapport
    if menu_choice != "None":
        print("Entrez le numéro de l'action que vous souhaitez utiliser :")
        for option in menu_choice:
            print(f"{option}: {menu_choice[option]}")
        answer = input()
        if answer in str(menu_choice.keys()):
            return "{}-{}".format(menu_answer, answer)
    display_incorrect_action()
    return None

def display_incorrect_action():
    print("\n/!\\/!\\/!\\/!\\/!\\/!\\")
    print("Saisie incorrecte")
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
        print("Validez vous les informations ? Y/n : ")
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
        print("Validez vous les informations ? Y/n : ")
        if input().upper() == 'Y':
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


def display_infos_for_tournament():
    """display informations for a given tournament."""
    id = ask_tournament_id()
    with open("database.json", 'r+') as file:
        data = json.load(file)
        t = data["tournaments"][id]
        print("**********************************************************************")
        print(f'id : {t["id"]} | Nom : {t["name"]} | Date de début : {t["starting_date"]} | Date de fin : {t["ending_date"]}')
        print("**********************************************************************")
    


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


def display_leaderboard(id):
    with open(gc.DB_FILE_NAME, 'r+') as file:
            data = json.load(file)
            tournament = data[gc.TOURNAMENTS][id]
            matches = gc.generate_leaderboard(tournament[gc.ROUND_LIST][-1]["matches"])

    print("\n**********************************************************************")
    print("\nClassement : ")
    for index, rank in enumerate(matches):
        print(f"{index+1} : {rank}")




def display_matches(list_matches):
    print("\nMatches de ce round : ")
    for match in list_matches:
        print(match)


def ask_player_id():
    return input("Entrez l'ID du joueur que vous voulez inscrire au tournois : \nEntrez \"terminer\" pour cloturer les inscriptions au tournois : ")


def ask_tournament_id():
    print("**********************************************************************")
    return int(input("\nEntrez l'ID du tournois à sélectionner : \n"))


def ask_match_result(match):
    print("\n**********************************************************************")
    print("Quel est le résultat de ce match ?")
    print(match)
    print("G pour victoire du joueur de gauche")
    print("D pour victoire du joueur de droite")
    print("E pour égalité")


def tournament_inscription_ended():
    print("\nInscriptions au tournois cloturées")

def incorrect_entry():
    print("Saisie incorrecte !")

def tournament_completed():
    print("\nLe tournois est terminé")

def ask_exit_confirmation():
    while True:
        result = input("Êtes-vous sur de vouloir quitter le logiciel ? (Y/n)")
        if result.upper() == 'Y':
            return False
        if result.upper() == 'N':
            return True