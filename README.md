# Multi-Agent-Games

## Research Question
How can multi-model communication be utilized to detect and combat deceptive text, particularly in the context of misinformation spread?

## Research Design
1. Construction of Multi-LM Environment: Develop a framework where multiple language models (LMs) are provided with individual profiles resembling players in a Mafia game. Simplified rules of the game will be adapted to suit the model's capabilities.
2. Training of Participant LMs: Train the LMs using transcribed Mafia game recordings. External LMs could be employed to evaluate model generations. Training will focus on learning from final consequences in game recordings, such as identifying deceptive strategies or clues.
3. Generalization to Real-life Misinformation Scenes: Transition the trained LMs to real-life misinformation scenarios. Models will aim to identify and combat misinformation, with human judgments providing supervision.
4. Evaluation Plan: Evaluate model performance by comparing final game results in recording-guided scenes. Human or other LM judgments will assess performance in other cases.

## Resources
https://www.instructables.com/How-To-Play-Mafia-with-And-Without-Cards
https://github.com/sumedhrasal/simulation
https://aclanthology.org/2023.emnlp-main.13.pdf
https://composable-models.github.io/llm_debate/
https://github.com/zjunlp/LLMAgentPapers
