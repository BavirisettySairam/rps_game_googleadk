# Rock-Paper-Scissors-Plus AI Referee

An AI-powered game referee built with **Google ADK** (Agent Development Kit) and **Gemini 2.5 Flash**.

## Game Rules
- Best of 3 rounds
- Moves: `rock`, `paper`, `scissors`, `bomb`
- Bomb beats everything but can only be used **once per game**
- Invalid moves count as a lost round

## Setup

1. Install dependencies:
```bash
pip install google-adk python-dotenv
```

2. Create `.env` file with your API key:
```
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=your_api_key_here
```

3. Run the game:
```bash
python main.py
```

## Project Structure
```
rps_agent/
├── agent.py   # AI agent with game tools
├── main.py    # Game loop and runner
├── .env       # API key (not committed)
└── README.md
```

## How It Works
The AI referee uses 4 tools to manage the game:
- `validate_move` - Checks if user input is valid
- `get_bot_move` - Generates bot's random move
- `resolve_round` - Determines round winner
- `update_game_state` - Tracks scores and rounds

---
*Built by Bavirisetty Sairam for upliance.ai AI Product Engineer Assignment*
