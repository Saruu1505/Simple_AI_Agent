from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os

load_dotenv()
#print("API KEY:", os.environ.get("OPENAI_API_KEY"))  # Skriv ut variabelen her

@tool
def calculator (a: float, b: float) -> str:
    """ Brukbart for utføring av matematiske kalkuleringer"""
    print("Tool har bltt kalt")
    return f"Summen av {a} og {b} er {a+b}"

@tool
def si_hallo(navn:str) -> str:
    """Sier hei til brukeren"""
    return f"Hei, {navn}! Hvordan har du det i idag?"

@tool
def si_hade_bra(navn:str) -> str:
    """Denne sier hade til brukeren"""
    return f"Hade bra, {navn}! Ha en fin dag videre."

def main ():
    model = ChatOpenAI(temperature=0)

    tools = [calculator, si_hallo, si_hade_bra]
    agent_executor = create_react_agent(model, tools)

    print("Velkommer, Jeg er din AI Assistent. Trykk 'quit' for å avslutte")
    print("Du kan bruke meg som kalkulator eller bare ha en vanlig samtale med")

    while True:
        bruker_input = input("\nYou: ").strip()

        if bruker_input == "quit":
            break

        print("\nAssistant:", end="")
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=bruker_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")
        print()

if __name__ == "__main__":
    main()