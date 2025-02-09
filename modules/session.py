import secrets
import base64
import json
from modules.database import get_db_connection


def _generate_session_id(): # this function is used to generate a random session ID
    token_bytes = secrets.token_bytes(32)
    return base64.urlsafe_b64encode(token_bytes).decode('utf-8')
class Session:
    def __init__(self, session_id=None): # generates a new session ID if none is provided
        self.id = session_id or _generate_session_id()
        self._update()

    def _update(self): # updates the session from the database
        conn, cursor = get_db_connection()
        result = cursor.execute('SELECT * FROM sessions WHERE session_id = ?', (self.id,)).fetchone()
        conn.close()
        if not result:
            return self._create()
            
        self.username = result['username'] # was supposed to be for cosmetic purposes, never implemented
        self.code = result['code'] # is supposed to be used to handle switching between different sessions, never implemented
        self.classes = json.loads(result['classes']) # list of classes the user is in
        return self

    def _create(self): # creates a new session in the database
        conn, cursor = get_db_connection()
        self.username = "user" + str(cursor.execute('SELECT COUNT(*) FROM sessions').fetchone()[0]) # generate a new username
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