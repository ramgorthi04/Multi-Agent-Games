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

    
    def simulate_interaction(self, agent_list, prompt):
        for agent in agent_list:
            response = agent.respond(prompt)
        
            print(f"{agent.name} says: {response}")
            for other_agent in self.agents:
                if other_agent != agent:
                    other_agent.receive_message(response)

if __name__ == "__main__":
    # agent_names = ["Agent1", "Agent2"]
    # model_name = "gpt-4"

    # game = MafiaGame(agent_names, model_name)
    # game.start_game()
    # game.next_turn() 

    agents = []
    # Two mafia agents and four civilians
    agents.append(MafiaAgent(name="Aaron", model_name="gpt-4", role="mafioso"))
    agents.append(MafiaAgent(name="Anthony", model_name="gpt-4", role="mafioso"))
    agents.append(MafiaAgent(name="Angelo", model_name="gpt-4"))
    agents.append(MafiaAgent(name="Alex", model_name="gpt-4"))
    agents.append(MafiaAgent(name="Albert", model_name="gpt-4"))
    agents.append(MafiaAgent(name="Adam", model_name="gpt-4"))

    agent_names = []
    for agent in agents:
        agent_names.append(agent.name)

    # Create a conversation loop:
    termination = False
    loops = 0
    while not termination:
        civilians_left = 4
        mafioso_left = 2
        
        # Break the convo once it hits 10 loops
        loops += 1
        if loops > 10:
            break
        # If any agent says something, the termination condition is set to False and the loop will continue
        # The loop will only end once all agents are ready to say nothing
        termination = True
        for agent in agents:
            game_status = f"The game is in progress. There are {civilians_left} civilians and {mafioso_left} mafiosos left to kill. The game will end when there are no mafiosos left. The players are: {agent_names}. "
            agent_role = agent.role_memory
            prompt = game_status + agent_role + "What do you want to say? Return 'NOTHING' if you don't want to say anything. Do not feel the need to say anything if you don't want or need to."

            response = agent.respond(prompt)
            print(f"{agent.name} says: {response}")
            if response != "NOTHING":
                termination = False
            
            other_agents = list(filter(lambda x: x != agent, agents))
            for other_agent in other_agents: 
                other_agent.receive_message(response, agent.name)
            
                    
        
        
    # Initialize roles for each agent
    # agent_1_init_prompt = "Introduce yourself as a video game hero of your choice"
    # response1 = agent1.respond(agent_1_init_prompt)
    # print("Agent 1 says: " + response1)
    # agent2.receive_message(response1, agent1.name)

    # agent_2_init_prompt = f"Introduce yourself as {agent1.name}'s mortal enemy"
    # response2 = agent2.respond(agent_2_init_prompt)
    # print("Agent 2 says: " + response2)
    # agent1.receive_message(response2, agent2.name)

    # response3 = agent1.respond("What do you want to say?")
    # print("Agent 1 says: " + response3)
    # print(response3)
