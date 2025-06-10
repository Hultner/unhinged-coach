# Weather MCP Server

This MCP server provides weather information and an unhinged AI coach.

## Available Tools

1. **get_alerts(state)** - Get weather alerts for a US state (e.g., "CA", "NY")
2. **get_forecast(latitude, longitude)** - Get weather forecast for a location
3. **unhinged_coach(message)** - Get over-the-top motivational coaching advice

## Running the Server

### As an MCP Server (stdio transport)
```bash
uv run python weather.py
```

### Testing the Tools
```bash
uv run python test_tools.py
```

## Configuration

Make sure you have a `.env` file in the parent directory with:
```
OPEN_API_KEY=your-openai-api-key-here
```

## Example Usage

The unhinged coach tool will respond with extremely enthusiastic and over-the-top motivational advice:

**Input:** "I need motivation to finish my coding project!"

**Output:** Something like:
"LISTEN UP, CODING WARRIOR! YOU'RE NOT JUST WRITING CODE, YOU'RE FORGING THE FUTURE WITH YOUR BARE HANDS AND PURE DETERMINATION! EVERY LINE OF CODE IS A VICTORY AGAINST THE FORCES OF MEDIOCRITY! FINISH THAT PROJECT LIKE THE ABSOLUTE LEGEND YOU ARE!"
