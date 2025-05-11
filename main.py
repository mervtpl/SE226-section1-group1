from vertexai.preview.vision_models import ImageGenerationModel
import vertexai
from PIL import Image
import io

PROJECT_ID = "se226-459316"  
LOCATION = "us-central1"

vertexai.init(project=PROJECT_ID, location=LOCATION)
imagen_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")

def generate_image(scene_description, location, style):
    prompt = f"{scene_description}, set in {location}, in {style} style"
    print("Generating image with prompt:", prompt)
    result = imagen_model.generate_images(prompt=prompt, number_of_images=1)
    return result[0]._image_bytes

if __name__ == "__main__":
    scene = "A dramatic battlefield at dusk, smoke and fire in the background"
    loc = "Ancient Rome"
    style = "Realistic"

    try:
        img_bytes = generate_image(scene, loc, style)
        img = Image.open(io.BytesIO(img_bytes))
        img.show()
        print("Image generated and displayed successfully.")
    except Exception as e:
        print("Failed to generate image:", e)