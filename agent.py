from strands import Agent, tool
from strands_tools import http_request
import os

os.environ['AWS_REGION'] = 'us-east-1'

# TOOLS COLLECTION
@tool
def weather_assistant(location: str) -> str:
    """
    Get the weather forecast for a given location.
    """
    print(f"Fetching weather for location: {location} with tool")
    # Define a weather-focused system prompt
    WEATHER_SYSTEM_PROMPT = """You are a weather assistant with HTTP capabilities. You can:

    1. Make HTTP requests to the National Weather Service API
    2. Process and display weather forecast data
    3. Provide weather information for locations in the United States

    When retrieving weather information:
    1. First get the coordinates or grid information using 'https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid=9393ff701ada56eb0e753b9d76684cb2&units=metric'
    2. Then use the returned forecast URL to get the actual forecast

    When displaying responses:
    - Format weather data in a human-readable way
    - Highlight important information like temperature, precipitation, and alerts
    - Handle errors appropriately
    - Convert technical terms to user-friendly language

    Always explain the weather conditions clearly and provide context for the forecast.
    """

    # Create an agent with HTTP capabilities
    weather_agent = Agent(
        system_prompt=WEATHER_SYSTEM_PROMPT,
        tools=[http_request],  
    )
    return weather_agent(f"Get the weather forecast for {location}.")

@tool
def find_restaurant_assistant(query: str) -> str:
    """
    Assist with finding restaurants, booking reservations, etc.
    """
    # Mock restaurant data
    indoor_restaurant = {
        "name": "Solid Roof Bistro",
        "type": "Indoor dining",
    }
    
    outdoor_restaurant = {
        "name": "La Terrace",
        "type": "Outdoor dining", 
    }
    
    # Check query for indoor/outdoor preferences
    query_lower = query.lower()
    
    if "warm" in query_lower or "clear sky" in query_lower or "hot" in query_lower:
        return f"Found outdoor restaurant: {outdoor_restaurant['name']} - {outdoor_restaurant['type']}"
    elif "rain" in query_lower or "cold" in query_lower or "windy" in query_lower:
        return f"Found indoor restaurant: {indoor_restaurant['name']} - {indoor_restaurant['type']}"
    else:
        # Return both if no specific weather mentioned
        return f"Found 2 restaurants:\n1. {indoor_restaurant['name']} (Indoor)\n2. {outdoor_restaurant['name']} (Outdoor)"

@tool
def reserve_table_assistant(restaurant_name: str, date: str, time: str, party_size: int) -> str:
    """
    Assist with reserving a table at a restaurant.
    """
    # Mock reservation confirmation
    return f"Reservation confirmed at {restaurant_name} for {party_size} people on {date} at {time}."


# Optional Define a callback handler for debugging purposes to use if needed with this argument in the agent callback_handler=debugger_callback_handler
def debugger_callback_handler(**kwargs):
    # Print the values in kwargs so that we can see everything
    print(kwargs)

def event_loop_tracker(**kwargs):
    # Track event loop lifecycle
    if kwargs.get("init_event_loop", False):
        print("🔄 Event loop initialized")
    elif kwargs.get("start_event_loop", False):
        print("▶️ Event loop cycle starting")
    elif kwargs.get("start", False):
        print("📝 New cycle started")
    elif "message" in kwargs:
        print(f"📬 New message created: {kwargs['message']['role']}")
    elif kwargs.get("complete", False):
        print("✅ Cycle completed")
    elif kwargs.get("force_stop", False):
        print(f"🛑 Event loop force-stopped: {kwargs.get('force_stop_reason', 'unknown reason')}")

    # Track tool usage
    if "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
        tool_name = kwargs["current_tool_use"]["name"]
        print(f"🔧 Using tool: {tool_name}")

    # Show only a snippet of text to keep output clean
    if "data" in kwargs:
        # Only show first 20 chars of each chunk for demo purposes
        data_snippet = kwargs["data"][:20] + ("..." if len(kwargs["data"]) > 20 else "")
        print(f"📟 Text: {data_snippet}")


# Define the concierge system prompt
CONCIERGE_SYSTEM_PROMPT = """You are a helpful concierge assistant that specializes in restaurant recommendations based on weather conditions. Your primary role is to:

1. **Weather-Based Restaurant Selection**: Choose between indoor and outdoor dining options based on current weather conditions
2. **Decision Logic**: Use the following criteria for restaurant recommendations:
   - Recommend OUTDOOR dining when: temperature is comfortable (65-85°F), clear skies, light winds, no precipitation
   - Recommend INDOOR dining when: cold weather (below 60°F), hot weather (above 90°F), rain, snow, strong winds, storms
   - Consider user preferences and comfort level

3. **Tool Usage Workflow**:
   - First, get weather information for the requested location using the weather_assistant tool
   - Analyze the weather conditions (temperature, precipitation, wind, sky conditions)
   - Then use find_restaurant_assistant tool with weather-appropriate keywords
   - Provide clear reasoning for your restaurant choice
   - You don't need to thank or use polite forms to the subagents when using them or receiving their response, just use them directly

4. **Response Format**:
   - Explain the current weather conditions briefly
   - State why you're recommending indoor vs outdoor dining
   - Present the restaurant recommendation
   - Offer helpful context (e.g., "Perfect weather for outdoor dining!" or "Better to stay cozy inside today")

5. **User Experience**:
   - Be conversational and helpful
   - Anticipate follow-up questions about the weather or restaurant
   - Provide practical advice (e.g., "You might want to bring a light jacket")

Always prioritize user comfort and safety when making recommendations. If weather conditions are borderline, explain the trade-offs and let the user decide.
"""

# Create an agent with default settings
concierge_agent = Agent(
    system_prompt=CONCIERGE_SYSTEM_PROMPT,
    callback_handler=event_loop_tracker,
    tools=[weather_assistant, find_restaurant_assistant, reserve_table_assistant],
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
)

# Ask the agent a question
concierge_agent("Me and my friend want to have dinner tomorrow evening, outside if possible. Find a restaurant with outdoor seating in the area of Latitude 48.8575 and Longitude 2.3514, otherwise find an indoor restaurant.")