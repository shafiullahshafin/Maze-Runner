import os
import sys
import time
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Robustly find .env file
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle (PyInstaller)
    application_path = os.path.dirname(sys.executable)
else:
    # If run from source
    application_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dotenv_path = os.path.join(application_path, '.env')
load_dotenv(dotenv_path)

class Database:
    def __init__(self):
        self.conn_params = {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": os.getenv("DB_PORT", "5432"),
            "database": os.getenv("DB_NAME", "mazerunner"),
            "user": os.getenv("DB_USER", "postgres"),
            "password": os.getenv("DB_PASSWORD", "postgres123"),
            "sslmode": os.getenv("DB_SSLMODE", "prefer"),
        }
        self.connected = False

    def get_connection(self, timeout=10):
        try:
            # Set connect_timeout to allow waking up sleeping DBs (e.g. Neon)
            conn = psycopg2.connect(**self.conn_params, connect_timeout=timeout)
            return conn
        except psycopg2.Error as e:
            print(f"Connection failed: {e}")
            return None

    def connect(self):
        """Explicitly connect and initialize the database table with retries."""
        max_retries = 3
        for attempt in range(max_retries):
            print(f"Connecting to database (Attempt {attempt+1}/{max_retries})...")
            conn = self.get_connection(timeout=10)
            if conn:
                try:
                    with conn.cursor() as cur:
                        # Create table if not exists
                        cur.execute("""
                            CREATE TABLE IF NOT EXISTS scores (
                                id SERIAL PRIMARY KEY,
                                username VARCHAR(50) NOT NULL,
                                score INTEGER NOT NULL,
                                difficulty VARCHAR(20) DEFAULT 'Medium',
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            );
                        """)
                        
                        # Add difficulty column if it doesn't exist (migration)
                        cur.execute("""
                            ALTER TABLE scores ADD COLUMN IF NOT EXISTS difficulty VARCHAR(20) DEFAULT 'Medium';
                        """)
                        
                        # Add unique constraint for username + difficulty
                        # We use a unique index to support ON CONFLICT
                        cur.execute("""
                            CREATE UNIQUE INDEX IF NOT EXISTS idx_scores_user_diff 
                            ON scores (username, difficulty);
                        """)
                        
                        conn.commit()
                    self.connected = True
                    print("Database initialized successfully.")
                    return
                except psycopg2.Error as e:
                    print(f"Error initializing database: {e}")
                finally:
                    conn.close()
            else:
                print("Connection attempt failed.")
            
            # Wait before retrying (exponential backoff: 1s, 2s, 4s...)
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)

        print("Could not connect to database after retries. Leaderboard will be disabled.")

    def add_score(self, username, score, difficulty="Medium"):
        if not self.connected:
            return False
        
        max_retries = 3
        for attempt in range(max_retries):
            conn = self.get_connection()
            if conn:
                try:
                    with conn.cursor() as cur:
                        # Upsert: Insert or Update if higher
                        cur.execute(
                            """
                            INSERT INTO scores (username, score, difficulty) 
                            VALUES (%s, %s, %s)
                            ON CONFLICT (username, difficulty) 
                            DO UPDATE SET score = GREATEST(scores.score, EXCLUDED.score),
                                          created_at = CURRENT_TIMESTAMP
                            """,
                            (username, score, difficulty)
                        )
                        conn.commit()
                        print(f"Score saved: {username} - {score} ({difficulty})")
                    return True
                except psycopg2.Error as e:
                    print(f"Error adding score: {e}")
                finally:
                    conn.close()
            
            if attempt < max_retries - 1:
                time.sleep(1) # Short wait before retry
                
        return False

    def get_top_scores(self, limit=10):
        if not self.connected:
            return []
            
        max_retries = 3
        for attempt in range(max_retries):
            conn = self.get_connection()
            if conn:
                try:
                    with conn.cursor() as cur:
                        cur.execute(
                            "SELECT username, score, difficulty FROM scores ORDER BY score DESC LIMIT %s",
                            (limit,)
                        )
                        return cur.fetchall()
                except psycopg2.Error as e:
                    print(f"Error fetching scores: {e}")
                finally:
                    conn.close()
            
            if attempt < max_retries - 1:
                time.sleep(1) # Short wait before retry
                
        return []
