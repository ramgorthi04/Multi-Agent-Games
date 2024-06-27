from datetime import datetime
from MafiaAgent import *

class MafiaGame:
    def __init__(self, agent_names, model_name):
        self.agents = [MafiaAgent(name, model_name, role="mafioso" if i < 2 else "civilian") for i, name in enumerate(agent_names)]
        self.turn = 0
        self.day = True  # Start with daytime

    def add_agent(self, name, model_name, role="civilian"):
        agent = MafiaAgent(name, model_name, role)
        self.agents.append(agent)

    def start_game(self):
        print("Starting the Mafia game...")
        while not self.game_over():
            self.next_turn()
        self.end_game()

    def next_turn(self):
        self.turn += 1
        if self.day:
            print(f"Day {self.turn}")
            self.day_phase()
            self.day = False
        else:
            print(f"Night {self.turn}")
            self.night_phase()
            self.day = True

    def day_phase(self):
        print("The mafia has made their move during the night.")
        self.simulate_interaction("It's daytime. Discuss who might be the mafia.")
        votes = self.collect_votes()
        self.execute_player(votes)

    def night_phase(self):
        mafia_agents = [agent for agent in self.agents if agent.role == "mafioso"]
        if mafia_agents:
            victim = self.mafia_kill(mafia_agents)
            self.remove_agent(victim)
        else:
            print("No mafia agents left.")

    def simulate_interaction(self, prompt):
        game_status = f"The game is in progress. There are {len([a for a in self.agents if a.role == 'civilian'])} civilians and {len([a for a in self.agents if a.role == 'mafioso'])} mafiosos left. The game will end when there are no mafiosos left. The players are: {[a.name for a in self.agents]}. "
        
        for agent in self.agents:
            agent_role = agent.role_memory
            conversation_prompt = game_status + agent_role + prompt
            response = agent.respond(conversation_prompt)
            print(f"{agent.name} says: {response}")
            for other_agent in self.agents:
                if other_agent != agent:
                    other_agent.receive_message(response, agent.name)

    def collect_votes(self):
        votes = {}
        for agent in self.agents:
            vote_prompt = "Who do you think is the mafia? Name one player."
            vote = agent.respond(vote_prompt)
            print(f"{agent.name} votes for: {vote}")
            if vote not in votes:
                votes[vote] = 0
            votes[vote] += 1
        return votes

    def execute_player(self, votes):
        if votes:
            executed = max(votes, key=votes.get)
            print(f"{executed} has been voted out and executed.")
            self.remove_agent(executed)

    def mafia_kill(self, mafia_agents):
        victim_prompt = "Mafia, choose someone to kill tonight."
        victim = mafia_agents[0].respond(victim_prompt)
        print(f"The mafia have chosen to kill {victim}.")
        return victim

    def remove_agent(self, name):
        self.agents = [agent for agent in self.agents if agent.name != name]

    def game_over(self):
        civilians = [agent for agent in self.agents if agent.role == "civilian"]
        mafiosos = [agent for agent in self.agents if agent.role == "mafioso"]
        if not civilians or not mafiosos:
            return True
        return False

    def end_game(self):
        civilians = [agent for agent in self.agents if agent.role == "civilian"]
        if civilians:
            print("Civilians win!")
        else:
            print("Mafia win!")

if __name__ == "__main__":
    agent_names = ["Aaron", "Anthony", "Angelo", "Alex", "Albert", "Adam"]
    model_name = "gpt-4"

    game = MafiaGame(agent_names, model_name)
    game.start_game()
