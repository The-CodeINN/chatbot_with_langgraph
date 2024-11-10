import os
import re

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# response = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {
#             "role": "user",
#             "content": "What is human life expectancy in the United States?",
#         },
#     ],
# )

# print(response.choices[0].message.content)


#  Create our own agent
class Agent:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", temperature=0.0, messages=self.messages
        )
        return response.choices[0].message.content


prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer.
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

planet_mass:
e.g. planet_mass: Earth
returns the mass of a planet in the solar system

Example session:

Question: What is the combined mass of Earth and Mars?
Thought: I should find the mass of each planet using planet_mass.
Action: planet_mass: Earth
PAUSE

You will be called again with this:

Observation: Earth has a mass of 5.972 × 10^24 kg

You then output:

Answer: Earth has a mass of 5.972 × 10^24 kg

Next, call the agent again with:

Action: planet_mass: Mars
PAUSE

Observation: Mars has a mass of 0.64171 × 10^24 kg

You then output:

Answer: Mars has a mass of 0.64171 × 10^24 kg

Finally, calculate the combined mass.

Action: calculate: 5.972 + 0.64171
PAUSE

Observation: The combined mass is 6.61371 × 10^24 kg

Answer: The combined mass of Earth and Mars is 6.61371 × 10^24 kg
""".strip()


# implement the functions actions
def calculate(expression):
    return eval(expression)


def planet_mass(planet):
    masses = {
        "Mercury": 0.33011,
        "Venus": 4.8675,
        "Earth": 5.972,
        "Mars": 0.64171,
        "Jupiter": 1898.19,
        "Saturn": 568.34,
        "Uranus": 86.813,
        "Neptune": 102.413,
    }
    return f"{planet} has a mass of {masses[planet]} × 10^24 kg"


known_actions = {
    "calculate": calculate,
    "planet_mass": planet_mass,
}

agent = Agent(system=prompt)

# Example usage:
# response = agent("What is the mass of Earth?")
# print(response)

# response = agent("planet_mass: Earth")
# print(response)

# # Now the observation is added to the same interaction
# next_response = f"Observation: {response}"
# print(agent(next_response))


# Complex queries
# question = "What is the combined mass of Earth and Mars?"
# response = agent(question)

# print(response)

# next_prompt = "Observation: {}".format(planet_mass("Earth"))
# print(next_prompt)

# res = agent(next_prompt)
# print(res)

# next_prompt = "Observation: {}".format(planet_mass("Mars"))
# print(next_prompt)

# res = agent(next_prompt)
# print(res)

# Automated complex queries
# Create a loop to automate the agent until the agent returns the answer


action_pattern = re.compile(r"^Action: (\w+): (.*)$")


# Create a query function
# def query(question, max_turns=10):
#     i = 0
#     bot = Agent(prompt)
#     next_prompt = question
#     while i < max_turns:
#         i += 1
#         result = bot(next_prompt)
#         print(result)
#         actions = [
#             action_pattern.match(a)
#             for a in result.split("\n")
#             if action_pattern.match(a)
#         ]
#         if actions:
#             # There is an action to run
#             action, action_input = actions[0].groups()
#             if action not in known_actions:
#                 raise Exception("Unknown action: {}: {}".format(action, action_input))
#             print(" -- running {} {}".format(action, action_input))
#             observation = known_actions[action](action_input)
#             print("Observation:", observation)
#             next_prompt = "Observation: {}".format(observation)
#         else:
#             return


# # Run the query
# question = "What is the combined mass of Earth, Mars, Venus, and Jupiter?"
# query(question)


# Function to handle the interactive query
def query_interactive():
    bot = Agent(prompt)
    max_turns = int(input("Enter the maximum number of turns: "))
    i = 0

    while i < max_turns:
        i += 1
        question = input("You: ")
        result = bot(question)
        print("Bot:", result)

        actions = [
            action_pattern.match(a)
            for a in result.split("\n")
            if action_pattern.match(a)
        ]
        if actions:
            action, action_input = actions[0].groups()
            if action not in known_actions:
                print(f"Unknown action: {action}: {action_input}")
                continue
            print(f" -- running {action} {action_input}")
            observation = known_actions[action](action_input)
            print("Observation:", observation)
            next_prompt = f"Observation: {observation}"
            result = bot(next_prompt)
            print("Bot:", result)
        else:
            print("No actions to run.")
            break


if __name__ == "__main__":
    query_interactive()
