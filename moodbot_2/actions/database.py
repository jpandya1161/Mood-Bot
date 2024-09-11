import mysql.connector
import yaml
import os
from path import current_dir

# Get the current directory (actions directory)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory (moodbot_2 directory)
parent_dir = os.path.dirname(current_dir)

# Construct the path to the credentials.yml file
credentials_path = os.path.join(parent_dir, 'credentials.yml')

class Database:
    def __init__(self):
        with open(credentials_path, 'r') as file:
            credentials = yaml.safe_load(file)
            db_config = credentials['db']

        # Connect to the MySQL database using the configuration
        self.connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )

    def execute_query(self, query, values=None):
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        result = cursor.fetchall()
        cursor.close()
        return result

    def close_connection(self):
        self.connection.close()
