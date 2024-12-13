import json
from .session import _generate_session_id

from modules.database import get_db_connection

def _create_class(ClassObject):
    conn, cursor = get_db_connection()
    cursor.execute('INSERT INTO classes (id, teacher, name, description) VALUES (?, ?, ?, ?)', (ClassObject.id, ClassObject.teacher, ClassObject.name, ClassObject.description))
    session = cursor.execute('SELECT * FROM sessions WHERE session_id = ?', (ClassObject.teacher,)).fetchone()
    classes = list(json.loads(session['classes']))
    classes.append(ClassObject.id)
    print(classes)
    cursor.execute('UPDATE sessions SET classes = ? WHERE session_id = ?', (json.dumps(classes), ClassObject.teacher))
    conn.close()

class Class:
    def __init__(self, teacher, name="New Class", description="...", members=[], lessons=[], id=None):
        if id:
            self.id = id
            cursor = get_db_connection()[1]
            result = cursor.execute('SELECT * FROM classes WHERE id = ?', (id,)).fetchone()
            if not result:
                raise Exception("Class not found.")
            self.teacher = result['teacher']
            self.name = result['name']
            self.description = result['description']
            self.members = json.loads(result['students'])
            self.lessons = json.loads(result['lessons'])
            return
        self.id = _generate_session_id()
        self.teacher = teacher 
        self.name = name
        self.description = description
        self.members = members
        self.lessons = lessons
        _create_class(self)

    def create_lesson(self, name="New Lesson", description="...", settings={}, content=""):
        pass

    def to_dict(self):
        return {
            "id": self.id,
            "teacher": self.teacher,
            "name": self.name,
            "description": self.description
        }
