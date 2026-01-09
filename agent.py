from google.adk.agents import Agent
import random

# Game state
game_state = {
    "round": 0,
    "user_score": 0,
    "bot_score": 0,
    "user_bomb_used": False,
    "bot_bomb_used": False,
    "game_active": True
}

def update_game_state(round_num: int = None, user_score: int = None, bot_score: int = None,
                     user_bomb_used: bool = None, bot_bomb_used: bool = None,
                     game_active: bool = None) -> str:
    """Update game state values."""
    if round_num is not None:
        game_state["round"] = round_num
    if user_score is not None:
        game_state["user_score"] = user_score
    if bot_score is not None:
        game_state["bot_score"] = bot_score
    if user_bomb_used is not None:
        game_state["user_bomb_used"] = user_bomb_used
    if bot_bomb_used is not None:
        game_state["bot_bomb_used"] = bot_bomb_used
    if game_active is not None:
        game_state["game_active"] = game_active
    return f"State updated: Round {game_state['round']}, Score: User {game_state['user_score']} - Bot {game_state['bot_score']}"

def validate_move(move: str, bomb_used: bool) -> str:
    """Check if user's move is valid. Returns VALID:[move] or INVALID:[error]."""
    valid_moves = ["rock", "paper", "scissors", "bomb"]
    move_lower = move.lower().strip()
    
    if move_lower not in valid_moves:
        return "INVALID:Invalid move. Please use: rock, paper, scissors, or bomb"
    if move_lower == "bomb" and bomb_used:
        return "INVALID:You've already used your bomb this game"
    return f"VALID:{move_lower}"

def resolve_round(user_move: str, bot_move: str) -> str:
    """Determine round winner. Returns WINNER:[user/bot/draw]|EXPLANATION:[text]."""
    # Bomb beats everything
    if user_move == "bomb" and bot_move == "bomb":
        return "WINNER:draw|EXPLANATION:Both used bomb - it's a draw!"
    if user_move == "bomb":
        return "WINNER:user|EXPLANATION:Bomb destroys everything - you win!"
    if bot_move == "bomb":
        return "WINNER:bot|EXPLANATION:Bomb destroys everything - I win!"
    
    # Standard RPS
    if user_move == bot_move:
        return "WINNER:draw|EXPLANATION:Same move - it's a draw!"
    
    wins = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
    if wins[user_move] == bot_move:
        return f"WINNER:user|EXPLANATION:{user_move.capitalize()} beats {bot_move} - you win!"
    return f"WINNER:bot|EXPLANATION:{bot_move.capitalize()} beats {user_move} - I win!"

def get_bot_move(round_num: int, bomb_used: bool) -> str:
    """Generate bot's move for the round."""
    moves = ["rock", "paper", "scissors"]
    # Maybe use bomb in round 3
    if not bomb_used and round_num == 3 and random.random() > 0.5:
        return "bomb"
    return random.choice(moves)

# Create the agent with game referee capabilities
root_agent = Agent(
    model='gemini-2.5-flash',
    name='rps_referee',
    description='An AI referee for Rock-Paper-Scissors-Plus game',
    instruction="""You are a game referee for Rock-Paper-Scissors-Plus. Your role is to:

1. GREETING & RULES (first message only):
   - Greet the user warmly
   - Explain the rules in 5 lines or less: Best of 3 rounds, use rock/paper/scissors/bomb, bomb beats all (once per game), invalid moves waste your round
   - Ask for their first move

2. GAME FLOW (each turn):
   - Extract the user's move from their message
   - Call validate_move(move, user_bomb_used) - returns "VALID:[move]" or "INVALID:[error]"
   - If INVALID: increment round, explain error, ask for next move (or end if round=3)
   - If VALID:
     * Call get_bot_move(current_round, bot_bomb_used) to get bot's choice
     * Call resolve_round(user_move, bot_move) - returns "WINNER:[user/bot/draw]|EXPLANATION:[text]"
     * Update scores based on winner
     * Call update_game_state() with new round number, scores, bomb usage flags
     * Display round results
     * If round < 3: ask for next move
     * If round == 3: call update_game_state(game_active=False) and announce final winner

3. OUTPUT FORMAT (each round):
   === ROUND X ===
   Your move: [move]
   My move: [move]
   Result: [explanation]
   Score: You [X] - Me [X]
   
4. FINAL RESULT (after round 3):
   === GAME OVER ===
   Final Score: You [X] - Me [X]
   [Winner announcement]

CRITICAL RULES:
- ALWAYS use tools for state management, NEVER track state yourself
- Game MUST end after exactly 3 rounds
- Be concise, friendly, and clear""",
    tools=[update_game_state, validate_move, resolve_round, get_bot_move]
)