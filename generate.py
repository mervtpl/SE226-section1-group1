import google.generativeai as genai

genai.configure(api_key="AIzaSyCjgZVne--9B41qT17-dUmcXVahk0Qx1EA")

def generate_dialogue(storyline, num_characters=2, max_words=1000):
    prompt = f"""
    Based on the following movie storyline:

    {storyline}

    Create a dialogue involving {num_characters} main characters. The dialogue should not exceed {max_words} words.
    Each character should have a name and speak naturally in turn. The tone should reflect the atmosphere of the story.
    """
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_scene_description(storyline):
    prompt = f"""
    Based on the following movie storyline:

    {storyline}

    Write a short, vivid scene description (maximum 3 sentences) that captures the atmosphere and setting of the story.
    """
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    return response.text.strip()
