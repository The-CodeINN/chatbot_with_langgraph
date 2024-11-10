import os
import re
from dataclasses import dataclass
from typing import Dict, List, Callable, Optional
from dotenv import load_dotenv
from openai import OpenAI


@dataclass
class Message:
    role: str
    content: str


class Agent:
    def __init__(
        self,
        system_prompt: str = "",
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.0,
    ):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.temperature = temperature
        self.messages: List[Message] = []

        if system_prompt:
            self.messages.append(Message("system", system_prompt))

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        self.messages.append(Message(role, content))

    def execute(self) -> str:
        """Execute the conversation with the AI model."""
        formatted_messages = [
            {"role": m.role, "content": m.content} for m in self.messages
        ]
        response = self.client.chat.completions.create(
            model=self.model, temperature=self.temperature, messages=formatted_messages
        )
        return response.choices[0].message.content

    def __call__(self, message: str) -> str:
        """Process a new user message and get the AI's response."""
        self.add_message("user", message)
        result = self.execute()
        self.add_message("assistant", result)
        return result


class AgentEnvironment:
    def __init__(self):
        self.actions: Dict[str, Callable] = {
            "calculate": self.calculate,
            "planet_mass": self.planet_mass,
        }
        self.planet_masses = {
            "Mercury": 0.33011,
            "Venus": 4.8675,
            "Earth": 5.972,
            "Mars": 0.64171,
            "Jupiter": 1898.19,
            "Saturn": 568.34,
            "Uranus": 86.813,
            "Neptune": 102.413,
        }
        self.action_pattern = re.compile(r"^Action: (\w+): (.*)$")

    @staticmethod
    def calculate(expression: str) -> float:
        """Safely evaluate a mathematical expression."""
        try:
            return eval(expression, {"__builtins__": {}}, {})
        except Exception:
            return float("nan")  # Return NaN (Not a Number) in case of an error

    def planet_mass(self, planet: str) -> str:
        """Get the mass of a planet."""
        if planet not in self.planet_masses:
            return f"Error: {planet} not found in database"
        return f"{planet} has a mass of {self.planet_masses[planet]} × 10^24 kg"

    def parse_action(self, response: str) -> Optional[tuple]:
        """Parse the agent's response for actions."""
        for line in response.split("\n"):
            if match := self.action_pattern.match(line):
                return match.groups()
        return None

    def execute_action(self, action: str, action_input: str) -> str:
        """Execute an action if it exists."""
        if action not in self.actions:
            return f"Unknown action: {action}: {action_input}"
        return str(self.actions[action](action_input))


def create_interactive_session(system_prompt: str):
    """Create an interactive session with the AI agent."""
    agent = Agent(system_prompt)
    env = AgentEnvironment()

    def run_session():
        while True:
            question = input("You: ")
            if question.lower() in ["quit", "exit"]:
                print("Goodbye!")
                break

            response = agent(question)
            print("Bot:", response)

            if action_tuple := env.parse_action(response):
                action, action_input = action_tuple
                print(f" -- running {action} {action_input}")
                observation = env.execute_action(action, action_input)
                print("Observation:", observation)
                next_response = agent(f"Observation: {observation}")
                print("Bot:", next_response)

    return run_session


# Example usage
if __name__ == "__main__":
    system_prompt = """
    You run in a loop of Thought, Action, PAUSE, Observation.
    At the end of the loop you output an Answer.
    Use Thought to describe your thoughts about the question asked.
    Use Action to run available actions - then return PAUSE.
    Observation will be the result of running those actions.

    Available actions:
    1. calculate: e.g. calculate: 4 * 7 / 3
    2. planet_mass: e.g. planet_mass: Earth
    """

    session = create_interactive_session(system_prompt)
    session()
