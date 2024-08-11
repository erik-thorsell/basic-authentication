import secrets
import base64
import json
from modules.database import get_db_connection

class Session:
    def __init__(self, session_id=None):
        """Initializes a new session object."""
        self.id = session_id or self._generate_session_id()
        self._update()

    def _generate_session_id(self):
        """Generates a cryptographically secure, random, session ID."""
        token_bytes = secrets.token_bytes(32)
        return base64.urlsafe_b64encode(token_bytes).decode('utf-8')

    def _update(self):
        """Updates the session object."""
        conn, cursor = get_db_connection()
        result = cursor.execute('SELECT * FROM sessions WHERE session_id = ?', (self.id,)).fetchone()
        conn.close()
        if not result:
            return self._create()
            
        self.username = result['username']
        self.code = result['code']
        self.classes = json.loads(result['classes'])
        return self

    def _create(self):
        """Creates a new session."""
        conn, cursor = get_db_connection()
        self.username = "user" + str(cursor.execute('SELECT COUNT(*) FROM sessions').fetchone()[0])
        cursor.execute('INSERT INTO sessions (session_id, username) VALUES (?, ?)', (self.id, self.username))
        conn.close()
        return self._update()

    def to_dict(self):
        self._update()
        return {
            "id": self.id,
            "username": self.username,
            "code": self.code,
            "classes": self.classes
        }