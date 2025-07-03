from strands import Agent, tool
from strands_tools import http_request
import os

os.environ['AWS_REGION'] = 'us-east-1'

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
    1. First get the coordinates or grid information using https://api.weather.gov/points/{latitude},{longitude} or https://api.weather.gov/points/{zipcode}
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
    callback_handler=None,
    tools=[weather_assistant, find_restaurant_assistant],
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
)

# Ask the agent a question
response = concierge_agent("Me and my friend want to have lunch outside if possible. Find a restaurant with outdoor seating in the area of Latitude 40 and longitude -73 if the weather forecast for today is warm, otherwise find me an indoor restaurant.")
print(response)