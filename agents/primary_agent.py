import re
import urllib.parse
import vertexai
from vertexai.generative_models import GenerativeModel

from agents.task_agent import create_task
from agents.rag_agent import get_response
from agents.memory_agent import save_memory
from agents.vision_agent import analyze_image
from agents.weather_agent import get_weather

# 👉 Initialize Vertex AI
vertexai.init(project="third-harbor-489817-h7", location="us-central1")

model = GenerativeModel("gemini-2.5-flash")


# ==================================================
# 🔥 TIME EXTRACTION FUNCTION
# ==================================================
def extract_time(query):
    query = query.lower()

    # Detect day
    if "tomorrow" in query:
        day = "Tomorrow"
    elif "today" in query:
        day = "Today"
    else:
        day = "No specific day"

    # Detect time like 5 pm, 10:30 am
    time_match = re.search(r'(\d{1,2}(:\d{2})?\s?(am|pm))', query)

    if time_match:
        time = time_match.group(1)
    else:
        # Handle natural words
        if "tonight" in query:
            time = "Tonight"
        elif "morning" in query:
            time = "Morning"
        elif "evening" in query:
            time = "Evening"
        else:
            time = "No specific time"

    return f"{day} at {time}"


# ==================================================
# 🔥 GOOGLE CALENDAR LINK GENERATOR
# ==================================================
def generate_calendar_link(task, time_info):
    base_url = "https://calendar.google.com/calendar/render?action=TEMPLATE"

    text = urllib.parse.quote(task)
    details = urllib.parse.quote(f"Scheduled via JustInAI ({time_info})")

    return f"{base_url}&text={text}&details={details}"


# ==================================================
# 🧠 MAIN HANDLER FUNCTION
# ==================================================
async def handle_request(query, file=None):

    # ==================================================
    # 🖼 IMAGE FLOW
    # ==================================================
    if file:
        image_bytes = await file.read()

        # Vision agent
        vision_result = analyze_image(image_bytes)

        # Weather agent
        weather = get_weather()

        # Decision logic
        if "rain" in weather.lower():
            decision = "Rain expected, delaying action"
            task = "Delay action due to weather conditions"
        else:
            decision = "Weather is clear, proceed with action"
            task = "Proceed with recommended action"

        create_task(task)

        return {
            "type": "image",
            "analysis": vision_result,
            "weather": weather,
            "decision": decision,
            "task": task
        }

    # ==================================================
    # 🧠 INTENT DETECTION
    # ==================================================
    intent_prompt = f"""
    Classify this request into one of:
    - task
    - general

    Request: {query}
    Return only one word.
    """

    intent = model.generate_content(intent_prompt).text.lower()

    # ==================================================
    # 📅 TASK FLOW + CALENDAR
    # ==================================================
    if "task" in intent:

        create_task(query)

        # Extract time
        time_info = extract_time(query)

        # Calendar display
        calendar_event = f"📅 {query} → {time_info}"

        # Calendar link
        calendar_link = generate_calendar_link(query, time_info)

        # Save memory
        save_memory(query, calendar_event)

        return {
            "type": "task",
            "message": f"Task created: {query}",
            "calendar": calendar_event,
            "calendar_link": calendar_link
        }

    # ==================================================
    # 💡 GENERAL QUERY FLOW
    # ==================================================
    response = get_response(query)

    save_memory(query, response)

    return {
        "type": "general",
        "response": response
    }