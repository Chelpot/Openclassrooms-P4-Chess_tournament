def display_welcoming_message():
    print("*************************************************")
    print("*   Bienvenue, vous utilisez actuellement un    *")
    print("*  logiciel permettant de gérer les tournois du *")
    print("*                 club d'échec.                 *")
    print("*************************************************")

def display_action_pannel():
    print("*************************************************")
    print("Entrez le numéro de l'action que vous souhaitez entreprendre :")
    print("1. Créer un joueur")


def ask_player_info_for_creation():
    """Ask the player with a form for informations needed to create a Player"""
    is_valid = False
    while not is_valid:
        data=[]
        print("Prénom : ")
        data.append(input())
        print("Nom : ")
        data.append(input())
        print("Date de naissance (JJ/MM/AAAA) : ")
        data.append(input())
        print("Identifiant national d'échecs : ")
        data.append(input())
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