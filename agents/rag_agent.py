import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init(project="third-harbor-489817-h7", location="us-central1")

model = GenerativeModel("gemini-2.5-flash")

def get_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text if response.text else "No response generated"
    except:
        return "AI service unavailable"