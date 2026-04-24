import json

def get_weather(location: str) -> str:
    """
    A mock API tool to simulate fetching weather data.
    In a real scenario, this would call OpenWeatherMap or similar.
    """
    print(f"[Tool Execution] Calling get_weather for {location}...")
    
    # Mock data
    mock_db = {
        "london": {"temp": "15°C", "condition": "rainy"},
        "new york": {"temp": "22°C", "condition": "sunny"},
        "san francisco": {"temp": "18°C", "condition": "foggy"},
        "tokyo": {"temp": "25°C", "condition": "clear"}
    }
    
    loc_lower = location.lower()
    for key in mock_db:
        if key in loc_lower:
            data = mock_db[key]
            return json.dumps({"location": key.title(), "temperature": data["temp"], "condition": data["condition"]})
    
    return json.dumps({"location": location, "temperature": "unknown", "condition": "data unavailable"})

# OpenAI Tool schema definition
GET_WEATHER_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                }
            },
            "required": ["location"],
        },
    }
}
