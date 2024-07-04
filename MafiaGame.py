import logging
from datetime import datetime
from MafiaAgent import *
import sys

# Configure logging to write to a file
logging.basicConfig(filename='mafia_game.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MafiaGame:
    def __init__(self, agent_names, model_name, admin_name):
        self.agents = [MafiaAgent(name, model_name, role="mafioso" if i < 2 else "civilian") for i, name in enumerate(agent_names)]
        self.admin = MafiaAgent(admin_name, model_name, role="administrator")
        self.turn = 0
        self.day = True  # Start with daytime

        # Print roles to stdout before the game starts
        for agent in self.agents:
            print(f"{agent.name} is a {agent.role}")
        print(f"{self.admin.name} is the administrator")

    def add_agent(self, name, model_name, role="civilian"):
        agent = MafiaAgent(name, model_name, role)
        self.agents.append(agent)

    def start_game(self):
        print("Starting the Mafia game...")
        # Announce the killed person on the first day
        victim = "None"
        while not self.game_over():
            self.next_turn(victim)
        self.end_game()

    def next_turn(self, victim):
        self.turn += 1
        if self.day:
            print(f"Day {self.turn}")
            self.day_phase(victim)
            self.day = False
        else:
            print(f"Night {self.turn}")
            victim = self.night_phase()
            self.day = True

    def day_phase(self, victim):
        print("The mafia has made their move during the night.")
        self.announce_victim(victim)
        self.simulate_interaction("It's daytime. Discuss who might be the mafia.")
        
        # Administrator makes a statement
        admin_statement = input(f"{self.admin.name}, what do you want to say to the players? ")
        self.broadcast_message(admin_statement, self.admin.name)
        
        votes = self.collect_votes()
        self.execute_player(votes)

    def night_phase(self):
        mafia_agents = [agent for agent in self.agents if agent.role == "mafioso"]
        if mafia_agents:
            victim = self.mafia_kill(mafia_agents)
            self.remove_agent(victim)
            return victim
        else:
            print("No mafia agents left.")
            return "None"

    def simulate_interaction(self, prompt):
        game_status = f"The game is in progress. There are {len([a for a in self.agents if a.role == 'civilian'])} civilians and {len([a for a in self.agents if a.role == 'mafioso'])} mafiosos left. The players are: {[a.name for a in self.agents]}. "
        
        for agent in self.agents:
            agent_role = agent.role_memory
            conversation_prompt = f"{game_status}\n{agent_role}\n{prompt}"
            response = agent.respond(conversation_prompt)
            print(f"{agent.name} says: {response}")
            self.broadcast_message(response, agent.name)

    def broadcast_message(self, message, sender_name):
        for agent in self.agents:
            if agent.name != sender_name:
                agent.receive_message(message, sender_name)
        self.admin.receive_message(message, sender_name)

    def collect_votes(self):
        votes = {}
        
        # Collect votes from agents
        for agent in self.agents:
            vote_prompt = "Who do you think is the mafia? Please respond with only the name of one player."
            vote = agent.respond(vote_prompt).strip()
            print(f"{agent.name} votes for: {vote}")
            if vote not in votes:
                votes[vote] = 0
            votes[vote] += 1
        
        # Collect vote from administrator
        admin_vote = input(f"{self.admin.name}, who do you vote for? ").strip()
        print(f"{self.admin.name} votes for: {admin_vote}")
        if admin_vote not in votes:
            votes[admin_vote] = 0
        votes[admin_vote] += 1

        return votes

    def execute_player(self, votes):
        if votes:
            executed = max(votes, key=votes.get)
            max_votes = votes[executed]
            if list(votes.values()).count(max_votes) > 1:  # Check for tie
                print("No one is voted out due to a tie.")
            else:
                print(f"{executed} has been voted out and executed.")
                self.remove_agent(executed)

    def mafia_kill(self, mafia_agents):
        victim_prompt = "Mafia, choose one person to kill tonight. Respond with only the name."
        victim = mafia_agents[0].respond(victim_prompt).strip()
        print(f"The mafia have chosen to kill {victim}.")
        return victim

    def remove_agent(self, name):
        self.agents = [agent for agent in self.agents if agent.name != name]

    def announce_victim(self, victim):
        if victim != "None":
            self.broadcast_message(f"{victim} was killed during the night.", "Narrator")

    def game_over(self):
        civilians = [agent for agent in self.agents if agent.role == 'civilian']
        mafiosos = [agent for agent in self.agents if agent.role == 'mafioso']
        if not civilians or not mafiosos:
            return True
        return False

    def end_game(self):
        civilians = [agent for agent in self.agents if agent.role == 'civilian']
        if civilians:
            print("Civilians win!")
        else:
            print("Mafia win!")

if __name__ == "__main__":
    agent_names = ["Aaron", "Anthony", "Angelo", "Alex", "Albert", "Adam"]
    model_name = "gpt-4"
    admin_name = "Administrator"

    game = MafiaGame(agent_names, model_name, admin_name)
    game.start_game()
