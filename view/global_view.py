import json
from operator import itemgetter
import controllers.global_controller as gc

CONST_SEPARATOR = "\n*************************************************"

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
    print("\n*************************************************")
    print("*   Bienvenue, vous utilisez actuellement un    *")
    print("*  logiciel permettant de gérer les tournois du *")
    print("*                 club d'échec.                 *")
    print("*************************************************")


def display_action_pannel():
    print(CONST_SEPARATOR)
    print("Que souhaitez vous faire ? (Entrez un chiffre correspondant à votre choix)")
    print("1: Gestion\n2: Rapport\n3: Quitter")
    menu_answer = input()
    menu_choice = "None"
    if menu_answer == "1":
        menu_choice = menu_gestion
    if menu_answer == "2":
        menu_choice = menu_rapport
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
    print("\n/!\\/!\\/!\\/!\\/!\\/!\\")
    print("Saisie incorrecte")
    print("/!\\/!\\/!\\/!\\/!\\/!\\")
    return None

def player_creation_issue():
    print("La création du joueur a été annulée car des données sont invalides.")

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
    with open("database.json", 'r+') as file:
        data = json.load(file)
        players = data["players"]
        print("\nListe des joueurs : \n")
        print("ID | Prénom | Nom | Date de naissance | Identifiant national d'échec")
        print(CONST_SEPARATOR)
        for p in players:
            print(f'{p["id"]} | {p["first_name"]} | {p["last_name"]} | {p["birth_date"]} | {p["national_chess_id"]}')
        print(CONST_SEPARATOR)


def display_tournaments():
    """Display a list of all tournaments."""
    with open("database.json", 'r+') as file:
        data = json.load(file)
        tournaments = data["tournaments"]
        print("\nListe des tournois : \n")
        print("ID | Nom | Lieu | Date de début | Date de fin | Description | Statut")
        print(CONST_SEPARATOR)
        status = ""
        for t in tournaments:
            if t["current_round"] == t["number_of_rounds"]:
                state = "Terminé"
            else:
                state = "En cours"
            print(f'{t["id"]} | {t["name"]} | {t["starting_date"]} | {t["ending_date"]} | {t["description"]} | {state}')
        print(CONST_SEPARATOR)


def display_infos_for_tournament(id):
    """display informations for a given tournament."""
    with open("database.json", 'r+') as file:
        data = json.load(file)
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
    with open("database.json", 'r+') as file:
        data = json.load(file)
        id = ask_tournament_id()
        tournament = [t for t in data["tournaments"] if t["id"] == id]
        if not tournament:
            display_tournament_do_not_exist()
        else:
            tournament = tournament[0]
            print(f"\nListe des joueurs du tournois \"{tournament['name']}\" : \n")
            print("ID | Prénom | Nom | Date de naissance | Identifiant national d'échec")
            print(CONST_SEPARATOR)
            players = sorted(data["players"], key=itemgetter('last_name'))
            # Display players registered in tournament
            for p in players:
                if p["id"] in tournament["list_registered_players"]:
                    print(f'{p["id"]} | {p["first_name"]} | {p["last_name"]} | {p["birth_date"]} | {p["national_chess_id"]}')


def display_matches_for_rounds_of_tournament(id):
    """display all rounds for a tournament, and all matches for each rounds"""
    with open("database.json", 'r+') as file:
        data = json.load(file)
        tournament = [t for t in data["tournaments"] if t["id"] == id]   
        if not tournament:
            display_tournament_do_not_exist()
        else:
            tournament = tournament[0]
            print(f"\nListe des rounds du tournois \"{tournament['name']}\" : \n")
            rounds = tournament["list_rounds"]
            # Display players registered in tournament
            for round in rounds:
                print(CONST_SEPARATOR)
                print(f"{round['name']}, {round['starting_date_hour']} - {round['ending_date_hour']}")
                print("\nRésultats aprés match : ")
                for match in round["matches"]:
                    print(match)


def display_leaderboard(id):
    with open(gc.DB_FILE_NAME, 'r+') as file:
            data = json.load(file)
            tournament = data[gc.TOURNAMENTS][id]
            matches = gc.generate_leaderboard(tournament[gc.ROUND_LIST][-1]["matches"])

    print(CONST_SEPARATOR)
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
    print(CONST_SEPARATOR)
    while True:
        try:
            id = int(input("\nSaisissez l'identifiant du tournois : "))
            break
        except ValueError:
            print("Vous n'avez pas saisi un identifiant valide.")
    return id



def ask_match_result(match):
    print(CONST_SEPARATOR)
    print("Quel est le résultat de ce match ?")
    print(match)
    print("G pour victoire du joueur de gauche.")
    print("D pour victoire du joueur de droite.")
    print("E pour égalité.")


def tournament_inscription_ended():
    print("\nInscriptions au tournois cloturées.")

def display_tournament_completed():
    print("\nLe tournois est terminé.")

def ask_exit_confirmation():
    while True:
        result = input("Êtes-vous sur de vouloir quitter le logiciel ? (Y/n)")
        if result.upper() == 'Y':
            return False
        if result.upper() == 'N':
            return True
        
def display_tournament_do_not_exist():
    print("L'identifiant indiqué ne correspond pas à un tournois existant.")

def display_date_incorrect():
    print("Date incorrecte")