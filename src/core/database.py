"""
Database management
"""
import sqlite3
from pathlib import Path
from typing import Optional
from contextlib import contextmanager

class Database:
    """SQLite database manager"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Create database and tables if they don't exist"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Stories table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    style TEXT NOT NULL,
                    panels_json TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Webtoons table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS webtoons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    story_id INTEGER NOT NULL,
                    image_path TEXT NOT NULL,
                    status TEXT DEFAULT 'generated',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (story_id) REFERENCES stories(id)
                )
            """)
            
            # Instagram posts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS instagram_posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    webtoon_id INTEGER NOT NULL,
                    instagram_id TEXT,
                    caption TEXT,
                    hashtags TEXT,
                    posted_at TIMESTAMP,
                    likes INTEGER DEFAULT 0,
                    comments INTEGER DEFAULT 0,
                    saves INTEGER DEFAULT 0,
                    reach INTEGER DEFAULT 0,
                    last_updated TIMESTAMP,
                    FOREIGN KEY (webtoon_id) REFERENCES webtoons(id)
                )
            """)
            
            # A/B tests table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ab_tests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    test_name TEXT NOT NULL,
                    variant TEXT NOT NULL,
                    post_id INTEGER NOT NULL,
                    engagement_rate REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (post_id) REFERENCES instagram_posts(id)
                )
            """)
            
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """Get database connection context manager"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def insert_story(self, title: str, topic: str, style: str, panels_json: str) -> int:
        """Insert a new story"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO stories (title, topic, style, panels_json) VALUES (?, ?, ?, ?)",
                (title, topic, style, panels_json)
            )
            conn.commit()
            return cursor.lastrowid
    
    def insert_webtoon(self, story_id: int, image_path: str) -> int:
        """Insert a new webtoon"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO webtoons (story_id, image_path) VALUES (?, ?)",
                (story_id, image_path)
            )
            conn.commit()
            return cursor.lastrowid
    
    def insert_instagram_post(self, webtoon_id: int, instagram_id: str, 
                             caption: str, hashtags: str) -> int:
        """Insert a new Instagram post"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO instagram_posts 
                   (webtoon_id, instagram_id, caption, hashtags, posted_at) 
                   VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)""",
                (webtoon_id, instagram_id, caption, hashtags)
            )
            conn.commit()
            return cursor.lastrowid
    
    def update_post_metrics(self, post_id: int, likes: int, comments: int, 
                           saves: int, reach: int):
        """Update Instagram post metrics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE instagram_posts 
                   SET likes = ?, comments = ?, saves = ?, reach = ?, 
                       last_updated = CURRENT_TIMESTAMP
                   WHERE id = ?""",
                (likes, comments, saves, reach, post_id)
            )
            conn.commit()
