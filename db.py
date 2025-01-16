import os
from dotenv import load_dotenv

import pymysql

load_dotenv()

# Database connection configuration
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')

def get_db_connection():
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database="music_management",
          port=3305
    )
    return connection
