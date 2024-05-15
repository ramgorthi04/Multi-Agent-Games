## Implementation

This document outlines the implementation of the Mafia game simulation using multiple language models (LMs) to manage agent interactions and memory.

### Class: Memory

The `Memory` class represents a basic unit of memory for the agents. It stores the content, timestamp, importance, and last accessed time of the memory.

#### Attributes:
- `content`: The content of the memory.
- `timestamp`: The time the memory was created.
- `importance`: The importance score of the memory (default is 1).
- `last_accessed`: The last time the memory was accessed.

#### Methods:
- `__init__(self, content, importance=1)`: Initializes the memory with content and importance.

### Class: Reflection

The `Reflection` class extends `Memory` to include reflections, which are higher-level thoughts generated from multiple observations.

#### Attributes:
- Inherits all attributes from `Memory`.
- `evidence`: List of supporting memories that contributed to the reflection.

#### Methods:
- `__init__(self, content, evidence, importance=1)`: Initializes the reflection with content, evidence, and importance.

### Class: Plan

The `Plan` class extends `Memory` to manage future actions and plans for the agents.

#### Attributes:
- Inherits all attributes from `Memory`.
- `start_time`: The start time of the plan.
- `duration`: The duration of the plan.

#### Methods:
- `__init__(self, content, start_time, duration, importance=1)`: Initializes the plan with content, start time, duration, and importance.

### Class: MafiaAgent

The `MafiaAgent` class represents an agent in the Mafia game. Each agent has a name, a language model, and a memory stream to manage interactions and responses.

#### Attributes:
- `name`: The name of the agent.
- `model_name`: The name of the language model used by the agent.
- `memory_stream`: A list of memories stored by the agent.

#### Methods:
- `__init__(self, name, model_name)`: Initializes the agent with a name and language model.
- `add_memory(self, memory)`: Adds a new memory to the memory stream.
- `retrieve_memories(self, query, max_memories=5)`: Retrieves relevant memories based on the query.
- `calculate_relevance(self, memory_content, query)`: Calculates the relevance of a memory to the query using the language model.
- `reflect(self)`: Generates reflections from recent memories.
- `plan(self, plan_content, start_time, duration)`: Adds a future plan to the memory stream.
- `respond(self, prompt)`: Generates a response based on relevant memories and the current prompt.
- `send_message(self, message)`: Adds received messages to memory and prints them.

### Class: MafiaGame

The `MafiaGame` class manages the overall game, including initializing agents, managing turns, and facilitating communication between agents.

#### Attributes:
- `agents`: A list of `MafiaAgent` instances participating in the game.
- `turn`: The current turn number in the game.

#### Methods:
- `__init__(self, agent_names, model_name)`: Initializes the game with a list of agent names and the language model.
- `add_agent(self, name)`: Adds a new agent to the game.
- `start_game(self)`: Starts the Mafia game and manages the turns.
- `next_turn(self)`: Advances the game to the next turn.
- `simulate_interaction(self, agent1, agent2, prompt)`: Simulates an interaction between two agents based on a prompt.

### Example Usage

```python
# Example usage of the MafiaAgent class
if __name__ == "__main__":
    agent1 = MafiaAgent(name="Agent1", model_name="gpt-3.5-turbo")
    agent2 = MafiaAgent(name="Agent2", model_name="gpt-3.5-turbo")

    initial_prompt = "Who do you think is the Mafia in this game?"
    response1 = agent1.respond(initial_prompt)
    agent2.send_message(response1)

    response2 = agent2.respond("Do you agree or disagree?")
    agent1.send_message(response2)

    print(f"{agent1.name} says: {response1}")
    print(f"{agent2.name} says: {response2}")
```