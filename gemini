import google.generativeai as genai

genai.configure(api_key="AIzaSyCjgZVne--9B41qT17-dUmcXVahk0Qx1EA")

model = genai.GenerativeModel("gemini-1.5-pro-latest")

response = model.generate_content("Write a 2-line dramatic movie dialogue.")
print(response.text)
