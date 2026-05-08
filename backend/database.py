import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def get_connection():
    """Establishes a connection to the Neon PostgreSQL database."""
    if not DATABASE_URL or "YOUR_CONNECTION_STRING" in DATABASE_URL:
        raise ValueError("DATABASE_URL not found or not set in .env file. Please add your Neon connection string.")
    return psycopg2.connect(DATABASE_URL)

def init_db():
    """Initializes the database and creates the users table."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        ''')
        
        # Check if empty and seed with initial data
        cursor.execute('SELECT COUNT(*) FROM users')
        if cursor.fetchone()[0] == 0:
            initial_users = [
                ("admin@example.com", "password123"),
                ("user@techpark.com", "securepass"),
                ("test@test.com", "123456"),
                ("abc", "123")
            ]
            for user in initial_users:
                cursor.execute('INSERT INTO users (email, password) VALUES (%s, %s)', user)
            conn.commit()
            print("Database initialized and seeded.")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        cursor.close()
        conn.close()

def get_user(email):
    """Retrieves a user's password by email."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE email = %s', (email,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

def add_user(email, password):
    """Adds a new user to the database. Returns True if successful, False if user exists."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (email, password) VALUES (%s, %s)', (email, password))
        conn.commit()
        return True
    except psycopg2.IntegrityError:
        return False
    except Exception as e:
        print(f"Error adding user: {e}")
        return False
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    try:
        init_db()
    except ValueError as e:
        print(f"\n[!] Configuration Error: {e}")
        print("1. Go to your Neon.tech dashboard.")
        print("2. Copy your Connection String.")
        print("3. Paste it into the .env file in your project root.\n")
