import logging
from models import *
from datetime import datetime

# Configure logging to write to a file
logging.basicConfig(filename='mafia_game.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Memory:
    def __init__(self, content, importance=1):
        self.content = content
        self.timestamp = datetime.now()
        self.importance = importance
        self.last_accessed = self.timestamp

class Reflection(Memory):
    def __init__(self, content, evidence, importance=1):
        super().__init__(content, importance)
        self.evidence = evidence

class Plan(Memory):
    def __init__(self, content, start_time, duration, importance=1):
        super().__init__(content, importance)
        self.start_time = start_time
        self.duration = duration

class MafiaAgent:
    def __init__(self, name, model_name, role="civilian"):
        self.name = name
        self.model_name = model_name
        self.memory_stream = []
        self.role = role
        role_prompt = f"In the game of mafia, you are a {role}. There are two roles: mafioso and civilian. You are playing to win the game. If you are killed, you lose. Everything you say is broadcasted to all players. You will be referred to as '{name}.' "
        self.role_memory = role_prompt

    def add_memory(self, memory):
        self.memory_stream.append(memory)
        self.memory_stream.sort(key=lambda x: x.timestamp, reverse=True)

    def retrieve_memories(self, query, max_memories=5):
        now = datetime.now()
        relevance_scores = []
        for memory in self.memory_stream:
            time_decay = (now - memory.timestamp).total_seconds() / (60 * 10)
            recency_score = 1 / (1 + time_decay)
            importance_score = memory.importance
            relevance_score = self.calculate_relevance(memory.content, query) * recency_score * importance_score
            relevance_scores.append((relevance_score, memory))
        
        relevance_scores.sort(reverse=True, key=lambda x: x[0])
        relevant_memories = [memory for score, memory in relevance_scores[:max_memories]]
        
        for memory in relevant_memories:
            memory.last_accessed = now
        
        return relevant_memories

    def calculate_relevance(self, memory_content, query):
        prompt = f"Memory: {memory_content}\nQuery: {query}\nRelevance score (0-1):"
        response = get_LM_response(prompt, self.model_name)
        try:
            relevance_score = float(response.strip())
        except ValueError:
            relevance_score = 0.0
        return relevance_score

    def reflect(self):
        recent_memories = self.retrieve_memories("", max_memories=100)
        prompt = "Recent memories:\n" + "\n".join([m.content for m in recent_memories]) + "\nGenerate reflections:"
        response = get_LM_response(prompt, self.model_name)
        reflection_content = response.strip()
        reflection = Reflection(reflection_content, [m.content for m in recent_memories])
        self.add_memory(reflection)

    def plan(self, plan_content, start_time, duration):
        plan = Plan(plan_content, start_time, duration)
        self.add_memory(plan)

    def respond(self, prompt):
        relevant_memories = self.retrieve_memories(prompt)
        memory_context = "\n".join([m.content for m in relevant_memories])
        full_prompt = f"{prompt}\n\nYour memories:\n{memory_context}"
        response = get_LM_response(full_prompt, self.model_name)
        self.add_memory(Memory(content=f"In response to this instruction \"{prompt}\", you said \"{response}\""))
        return response

    def receive_message(self, message, sender_name):
        self.add_memory(Memory(content=f"{sender_name} said: \"{message}\""))
        logging.info(f"{self.name} received: {message}")
