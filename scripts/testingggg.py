# import components.generate as gen

# # print(gen.generate("If you were a human how would you feel?"))
# gen.generate_yap()


import dotenv
from dotenv import find_dotenv, set_key, load_dotenv
import os 
from time import sleep
# 1. Locate the .env file path
dotenv_file = find_dotenv()
load_dotenv(dotenv_file)

os.environ["API_KEY"] = "new_super_secret_key"
print(os.environ.get("API_KEY"))  # Output: new_super_secret_key

sleep(5)
os.environ["API_KEY"] = "even_more_secret_key"
print(os.environ.get("API_KEY"))  # Output: even_more_secret_key