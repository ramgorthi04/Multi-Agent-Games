from models import *
from datetime import datetime

class Memory:
    def __init__(self, content, importance=1):
        self.content = content
        self.timestamp = datetime.now()
        self.importance = importance
        self.last_accessed = self.timestamp

class FixedMemory(Memory):
    """
    Inherits from Memory class. Used for 'fixed memories' like mafia game roles, which we don't want to decay over time."""
    def __init__(self, content, importance=1):
        super().__init__(content, importance)

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
    def __init__(self, name, model_name):
        """
        Initializes the MafiaAgent object with a name and a model name.

        Parameters:
            name (str): The name of the agent.
            model_name (str): The name of the language model used by the agent.

        Returns:
            None
        """
        self.name = name
        self.model_name = model_name
        self.memory_stream = []

    def add_memory(self, memory):
        """
        Adds a memory to the memory stream and sorts the memory stream by timestamp in descending order.
        
        Parameters:
            memory: The memory object to be added to the memory stream.
        
        Returns:
            None
        """
        self.memory_stream.append(memory)
        self.memory_stream.sort(key=lambda x: x.timestamp, reverse=True)

    def retrieve_memories(self, query, max_memories=5):
        """
        Retrieves relevant memories based on a query and a maximum number of memories, sorted by relevance scores.
        
        Parameters:
            query (str): The query used to retrieve relevant memories.
            max_memories (int): The maximum number of memories to retrieve (default is 5).
        
        Returns:
            list: A list of relevant memories based on the query, limited by the maximum number specified.
        """
        now = datetime.now()
        relevance_scores = []
        
        # Retrieve the most relevant memories
        for memory in self.memory_stream:
            # For the Mafia Game, we will use a faster time decay (10 minute = 1 day)
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
        """
        Calculates the relevance score of a memory based on a query by interacting with a language model.
        
        Parameters:
            memory_content (str): The content of the memory to calculate relevance for.
            query (str): The query used to calculate the relevance score.
        
        Returns:
            float: The relevance score of the memory based on the query.
        """
        prompt = f"Memory: {memory_content}\nQuery: {query}\nRelevance score (0-1):"
        response = get_LM_response(prompt, self.model_name)
        if __debug__:
            print("Relevance score response: " + response)
        try:
            relevance_score = float(response.strip())
        except ValueError:
            relevance_score = 0.0
        return relevance_score

    def reflect(self):
        """
        Generates reflections based on recent memories and adds them to the agent's memory.
        """
        recent_memories = self.retrieve_memories("", max_memories=100)
        prompt = "Recent memories:\n" + "\n".join([m.content for m in recent_memories]) + "\nGenerate reflections:"
        response = get_LM_response(prompt, self.model_name)
        reflection_content = response.strip()
        reflection = Reflection(reflection_content, [m.content for m in recent_memories])
        self.add_memory(reflection)

    def plan(self, plan_content, start_time, duration):
        """
        Creates a plan with the given content, start time, and duration and adds it to the agent's memory.
        
        Parameters:
            plan_content (str): The content of the plan.
            start_time (datetime): The start time of the plan.
            duration (int): The duration of the plan in minutes.
        """
        plan = Plan(plan_content, start_time, duration)
        self.add_memory(plan)

    def respond(self, prompt):
        """
        Gets a response based on the provided prompt by retrieving relevant memories and using them in the final prompt for the language model response.

        Parameters:
            prompt (str): The input prompt for generating the response.

        Returns:
            str: The response generated by the language model based on the prompt.
        """
        relevant_memories = self.retrieve_memories(prompt)
        memory_context = "\n".join([m.content for m in relevant_memories])
        if __debug__:
            print(f"Memory context: {memory_context}\n\n")
        full_prompt = f"Memory: {memory_context}\n\n{prompt}"
        response = get_LM_response(full_prompt, self.model_name)
        
        # Add the prompt and response to memory
        self.add_memory(Memory(content=f"In response to this instruction \"{prompt}\", I said \"{response}\""))

        return response

    def receive_message(self, message, sender_name):
        """
        Adds a memory of the received message to the agent the function is called upon. Prints the message received.
        
        Parameters:
            message: The message received by the agent.
        
        Returns:
            None
        """
        self.add_memory(Memory(content=f"{sender_name} said: \"{message}\""))
        print(f"{self.name} received: {message}")
