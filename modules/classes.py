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

#lesson structure
{
    "id": 0,
    "class": "class_id",
    "name": "Lesson 1",
    "description": "This is the first lesson.",
    "created_at": "2021-09-01T12:00:00",
    "language": "English",
    "settings": {
        "due_date": "2021-09-08T12:00:00",
    },
    "content": [
        ("hello", "hej"),
        ("world", "värld"),
        ("goodbye", "hejdå")
    ]
}

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

    def create_lesson(self, name="New Lesson", description="...", settings={}, content={}):
        connection, cursor = get_db_connection()

        lesson_id = cursor.execute('SELECT COUNT(*) FROM lessons').fetchone()[0]
        cursor.execute('INSERT INTO lessons (id, class, name, description, settings, content) VALUES (?, ?, ?, ?, ?, ?)', (lesson_id, self.id, name, description, json.dumps(settings), json.dumps(content)))
        self.lessons.append(lesson_id)
        cursor.execute('UPDATE classes SET lessons = ? WHERE id = ?', (json.dumps(self.lessons), self.id))
        connection.close()
        return lesson_id
    
    def get_lesson(self, lesson_id):
        connection, cursor = get_db_connection()
        result = cursor.execute('SELECT * FROM lessons WHERE id = ?', (lesson_id,)).fetchone()
        connection.close()
        return result

    def to_dict(self):
        return {
            "id": self.id,
            "teacher": self.teacher,
            "name": self.name,
            "description": self.description
        }
