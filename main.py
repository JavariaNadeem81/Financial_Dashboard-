from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env file

# Now you can use them
api_key = os.getenv("API_KEY")
username = os.getenv("USER_NAME")

print("API KEY:", api_key)
print("User:", username)
