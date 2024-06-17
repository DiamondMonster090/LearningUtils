from dotenv import dotenv_values
import google.generativeai as genai

config = dotenv_values(".env")
API_KEY = config["API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])
while True:
    message = input()
    if message == 'exit':
        break
    response = chat.send_message(message)
    for chunk in response:
        print(chunk.text)
        print("_")