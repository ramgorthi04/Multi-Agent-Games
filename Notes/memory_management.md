## Memory Management Notes

### 1. Initial Setup
- Each agent is provided with an initial profile including background, role in the mafia game, and initial relationships with other agents.
- Initial memories are created from these profiles and stored in the memory stream.

### 2. Game Dynamics
- **Observations:** Agents record their actions and perceived actions of others (e.g., accusations, defenses, eliminations).
- **Interactions:** Agents engage in dialogues based on their roles and objectives (e.g., mafia members strategizing, villagers debating).

### 3. Memory Retrieval in Game
- During each turn, retrieve memories relevant to the current discussion or action.
- Use a combination of recency, importance, and relevance to ensure that agents have the necessary context for their decisions.

### Edge Cases
- **Memory Overload:** Implement mechanisms to manage the memory stream size, such as forgetting less relevant memories over time.
- **Contradictory Information:** Develop strategies to resolve conflicts in memory retrieval, prioritizing more reliable sources.
- **Real-Time Adaptation:** Ensure agents can dynamically adapt plans and strategies based on real-time interactions and new information.
