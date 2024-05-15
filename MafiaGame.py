from datetime import datetime
from MafiaAgent import *

class MafiaGame:
    def __init__(self, agent_names, model_name):
        self.agents = [MafiaAgent(name, model_name) for name in agent_names]
        self.turn = 0

    def add_agent(self, name, model_name):
        agent = MafiaAgent(name, model_name)
        self.agents.append(agent)

    def start_game(self):
        print("Starting the Mafia game...")
        self.next_turn()

    def next_turn(self):
        self.turn += 1
        print(f"Turn {self.turn}")
        for agent in self.agents:
            self.simulate_interaction(agent)

    def simulate_interaction(self, agent):
        prompt = "What do you want to say to the other players?"
        response = agent.respond(prompt)
        print(f"{agent.name} says: {response}")
        for other_agent in self.agents:
            if other_agent != agent:
                other_agent.send_message(response)

if __name__ == "__main__":
    # agent_names = ["Agent1", "Agent2"]
    # model_name = "gpt-4"

    # game = MafiaGame(agent_names, model_name)
    # game.start_game()
    # game.next_turn() 

    agent1 = MafiaAgent(name="Agent1", model_name="gpt-4")
    agent2 = MafiaAgent(name="Agent2", model_name="gpt-4")

    # Initialize roles for each agent
    agent_1_init_prompt = "Introduce yourself as a video game hero of your choice"
    response1 = agent1.respond(agent_1_init_prompt)
    print("Agent 1 says: " + response1)
    agent2.receive_message(response1, agent1.name)

    agent_2_init_prompt = f"Introduce yourself as {agent1.name}'s mortal enemy"
    response2 = agent2.respond(agent_2_init_prompt)
    print("Agent 2 says: " + response2)
    agent1.receive_message(response2, agent2.name)

    response3 = agent1.respond("What do you want to say?")
    print("Agent 1 says: " + response3)
    print(response3)
