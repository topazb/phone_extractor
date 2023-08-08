import os
import psycopg2
from psycopg2 import OperationalError

def test_postgres_connection():
    try:
        # Retrieve database parameters from environment variables
        db_params = {
            "host": os.environ.get("DB_HOST"),
            "database": os.environ.get("DB_NAME"),
            "user": os.environ.get("DB_USER"),
            "password": os.environ.get("DB_PASSWORD"),
            "port": os.environ.get("DB_PORT", 5432)  # Default is usually 5432
        }

        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Print PostgreSQL Connection properties
        print(connection.get_dsn_parameters(), "\n")

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print("Connected to PostgreSQL version:", db_version)

        # Close the cursor and connection
        cursor.close()
        connection.close()
        print("Connection closed.")

    except OperationalError as e:
        print("Error:", e)

if __name__ == "__main__":
    test_postgres_connection()
