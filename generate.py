import google.generativeai as genai
from vertexai.preview.vision_models import ImageGenerationModel
import vertexai
from PIL import Image
import io
import fetching_data

genai.configure(api_key="AIzaSyCjgZVne--9B41qT17-dUmcXVahk0Qx1EA")

def generate_dialogue(storyline, num_characters, max_words):
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


vertexai.init(project="se226-459316", location="us-central1")
imagen_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")


def generate_image(storyline, location, style):
    full_prompt = f"generate image based in {storyline}, set in {location}, in {style} style"
    result = imagen_model.generate_images(prompt=full_prompt, number_of_images=1)
    return result[0]._image_bytes


if __name__ == "__main__":
    location = "Tokyo"
    style = "Futuristic"

    img_bytes = generate_image(fetching_data.get_movie_storyline(), location, style)
    img = Image.open(io.BytesIO(img_bytes))
    img.show()
