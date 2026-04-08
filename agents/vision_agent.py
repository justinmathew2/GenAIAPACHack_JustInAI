import vertexai
from vertexai.generative_models import GenerativeModel, Part

vertexai.init(project="third-harbor-489817-h7", location="us-central1")

model = GenerativeModel("gemini-2.5-flash")

def analyze_image(image_bytes):
    image = Part.from_data(image_bytes, mime_type="image/jpeg")

    prompt = """
    Analyze this image and give output in this format:

    1. Issue (1 line)
    2. Cause (1 line)
    3. Recommended Action (3 bullet points only)

    Keep it very short and practical.
    """

    response = model.generate_content([prompt, image])

    return response.text