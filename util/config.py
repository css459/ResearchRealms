import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING')
