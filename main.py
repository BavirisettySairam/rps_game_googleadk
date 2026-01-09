from agent import root_agent, game_state
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import asyncio
import os
import warnings
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
warnings.filterwarnings("ignore", message=".*non-text parts.*")

USER_ID = "player_1"
SESSION_ID = "rps_game_session"

async def run_agent(runner, message: str, retries: int = 3) -> str:
    """Send message to agent and get response."""
    content = types.Content(role="user", parts=[types.Part(text=message)])
    for attempt in range(retries):
        try:
            response_text = ""
            async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            response_text = part.text
            return response_text.strip() if response_text else ""
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                wait_time = (attempt + 1) * 10
                print(f"Rate limited. Waiting {wait_time}s...")
                await asyncio.sleep(wait_time)
            else:
                raise e
    return "Error: Rate limit exceeded. Please try again later."

async def main():
    session_service = InMemorySessionService()
    runner = Runner(agent=root_agent, app_name=root_agent.name, session_service=session_service)
    await session_service.create_session(app_name=root_agent.name, user_id=USER_ID, session_id=SESSION_ID)
    
    print("=" * 50)
    print("ROCK-PAPER-SCISSORS-PLUS REFEREE")
    print("=" * 50 + "\n")
    
    print("🤖 REFEREE:")
    print(await run_agent(runner, "Hello! I'm ready to play Rock-Paper-Scissors-Plus. Please explain the rules and let's start!"))
    print()
    
    while game_state["game_active"]:
        user_input = input("👤 YOUR MOVE: ").strip()
        print()
        
        if not user_input:
            print("Please enter a move!\n")
            continue
        
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        print("🤖 REFEREE:")
        response = await run_agent(runner, user_input)
        if response:
            print(response)
        print()
        
        # End game after 3 rounds or if someone wins 2
        if game_state["round"] >= 3 or game_state["user_score"] >= 2 or game_state["bot_score"] >= 2:
            game_state["game_active"] = False
    
    print("=" * 50)
    print("Thanks for playing!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
