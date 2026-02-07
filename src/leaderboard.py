import threading
from src.database import Database

class Leaderboard:
    def __init__(self):
        self.db = Database()
        self.use_db = False
        self.is_loading = True
        
        self.thread = threading.Thread(target=self._init_db_connection)
        self.thread.daemon = True
        self.thread.start()

    def _init_db_connection(self):
        self.db.connect()
        self.use_db = self.db.connected
        self.is_loading = False

    def add_score(self, name, score, difficulty="Medium"):
        if self.use_db:
            threading.Thread(target=self._add_db_score, args=(name, score, difficulty), daemon=True).start()

    def _add_db_score(self, name, score, difficulty):
        success = self.db.add_score(name, score, difficulty)
        if not success:
            print("Failed to save to DB.")

    def get_top_scores(self):
        if self.is_loading:
            return []
        
        if self.use_db:
            return self.db.get_top_scores()
        return []

    def is_online(self):
        return self.use_db and not self.is_loading
