

menu_options = {
            1: 'Créer un nouveau joueur',
            2: 'Créer un nouveau tournois',
            8: 'Quitter'
        }

def display_welcoming_message():
    print("*************************************************")
    print("*   Bienvenue, vous utilisez actuellement un    *")
    print("*  logiciel permettant de gérer les tournois du *")
    print("*                 club d'échec.                 *")
    print("*************************************************")

def display_action_pannel():
    print("*************************************************")
    print("Entrez le numéro de l'action que vous souhaitez entreprendre :")
    for option in menu_options:
        print(f"{option}: {menu_options[option]}")

def ask_player_info_for_creation():
    """Ask the player with a form for informations needed to create a Player"""
    is_valid = False
    while not is_valid:
        data={}
        print("Prénom : ")
        data['first_name'] = input()
        print("Nom : ")
        data['last_name'] = input()
        print("Date de naissance (JJ/MM/AAAA) : ")
        data['birth_date'] = input()
        print("Identifiant national d'échecs : ")
        data['national_chess_id'] = input()
        print("Validez vous les informations ? Y/N : ")
        if input() == 'Y':
            is_valid = True
            return data
        else:
            return None
        
def ask_tournament_info_for_creation():
    """Ask the user informations to create a tournament"""
    is_valid = False
    while not is_valid:
        data={}
        print("Lieu : ")
        data['place'] = input()
        print("Nom du tournois : ")
        data['name'] = input()
        print("Date de commencement : ")
        data['starting_date'] = input()
        print("Date de fin : ")
        data['ending_date'] = input()
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
    pass

def display_tournaments():
    """Display a list of all tournaments."""
    pass

def display_infos_for_tournament(tournament):
    """display the name and dates for a given tournament."""
    pass

def display_players_for_tournament():
    """display a list of all the players for a given tournament, the players will be sorted by alphabetical order."""
    pass

def display_matches_for_turns_of_tournament():
    """display all turns for a tournament, and all matches for each turns"""
    pass