import random
import time

"""
Just the setup for the game. Need to add functionality for LLM discussion
"""

class MafiaPlayer:
    def __init__(self, name, role):
        """
        Initializes a new instance of the MafiaPlayer class with the given name and role.

        Parameters:
            name (str): The name of the player.
            role (str): The role of the player.

        Returns:
            None
        """
        self.name = name
        self.role = role

class MafiaGame:
    def __init__(self, players):
        """
        Initializes a new instance of the MafiaGame class with the given players list. 
        Sets up the initial attributes for the game including players, mafia, doctor, sheriff, civilians, and dead_players.
        
        Parameters:
            players (list): A list of MafiaPlayer instances representing the players in the game.
        
        Returns:
            None
        """
        self.players = players
        self.mafia = []
        self.doctor = None
        self.sheriff = None
        self.civilians = []
        self.dead_players = []

    def assign_roles(self):
        """
        Assigns roles to the players in the game.

        This function shuffles the list of players and assigns roles to each player based on the following criteria:
        - The number of mafia players is equal to one-fourth of the total number of players.
        - There is exactly one doctor player.
        - There is exactly one sheriff player.
        - The remaining players are considered civilian players.

        The roles are assigned as follows:
        - The mafia players are selected randomly from the shuffled list of players.
        - The doctor player is selected from the remaining players.
        - The sheriff player is selected from the remaining players.
        - The remaining players are considered civilian players.

        Parameters:
            self (MafiaGame): The current instance of the MafiaGame class.

        Returns:
            None
        """
        random.shuffle(self.players)
        num_players = len(self.players)
        num_mafia = num_players // 4
        num_doctor = 1
        num_sheriff = 1
        num_civilians = num_players - num_mafia - num_doctor - num_sheriff

        for i in range(num_mafia):
            self.mafia.append(self.players.pop())

        self.doctor = self.players.pop()
        self.sheriff = self.players.pop()

        for i in range(num_civilians):
            self.civilians.append(self.players.pop())

    def execute_night_phase(self):
        print("Night Phase")
        for mafia_member in self.mafia:
            target = random.choice(self.civilians)
            print(f"{mafia_member.name} chooses to kill {target.name}")
            self.civilians.remove(target)
            self.dead_players.append(target)

        time.sleep(1)

        print("Doctor, wake up and choose someone to save.")
        time.sleep(1)
        saved_player = random.choice(self.dead_players)
        print(f"The doctor chooses to save {saved_player.name}")
        self.dead_players.remove(saved_player)
        self.civilians.append(saved_player)

        time.sleep(1)

        print("Sheriff, wake up and investigate someone.")
        time.sleep(1)
        investigated_player = random.choice(self.players + self.dead_players)
        if investigated_player in self.mafia:
            print(f"{investigated_player.name} is mafia.")
        else:
            print(f"{investigated_player.name} is not mafia.")

    def day_phase(self):
        print("Day Phase")
        print("Discuss and vote.")
        # TODO: Add LLM discussion (this will be the most significant part of the project)
        # Add a new file, simulate_discussion.py to simulate the discussion

    def play_round(self):
        self.execute_night_phase()
        self.day_phase()

    def start_game(self):
        print("Game started.")
        self.assign_roles()
        while len(self.mafia) < len(self.civilians):
            self.play_round()
        print("Game Over. Civilians win!")

# Setup
names = ["Player1", "Player2", "Player3", "Player4", "Player5", "Player6", "Player7", "Player8"]
roles = ["Mafia", "Mafia", "Doctor", "Sheriff", "Civilian", "Civilian", "Civilian", "Civilian"]
players = [MafiaPlayer(name, role) for name, role in zip(names, roles)]

# Start game
game = MafiaGame(players)
game.start_game()
