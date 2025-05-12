from vertexai.preview.vision_models import ImageGenerationModel
import vertexai
from PIL import Image
import io

vertexai.init(project="se226-459316", location="us-central1")
imagen_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")

def generate_image(prompt, location, style):
    full_prompt = f"{prompt}, set in {location}, in {style} style"
    result = imagen_model.generate_images(prompt=full_prompt, number_of_images=1)
    return result[0]._image_bytes

if __name__ == "__main__":
    prompt = "A futuristic city at night, full of neon lights and flying cars"
    location = "Tokyo"
    style = "Futuristic"

    img_bytes = generate_image(prompt, location, style)
    img = Image.open(io.BytesIO(img_bytes))
    img.show()
