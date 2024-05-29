import sqlite3

subjects = [
    "Mathematics", "Physics", "Chemistry", "Biology", "History",
    "English Language", "Geography", "Computer Science", "Economics", "Literature",
    "Spanish", "French", "German", "Art", "Music",
    "Physical Education", "Psychology", "Sociology", "Further Maths", "Business Studies",
    "Accounting", "Engineering", "Design and Tech.", "Drama", "Film Studies",
    "Data Science", "Law", "Media Studies", "Philosophy", "Religious Studies",
    "Politics", "Statistics", "Astronomy", "Geology", "Anthropology",
    "Archaeology", "Linguistics", "Criminology", "Food Science", "Nutrition",
    "Horticulture", "Botany", "Zoology", "Entomology", "Meteorology",
    "Oceanography", "Astrophysics", "Biotechnology", "Nanotechnology", "Cryptography"
]

def get_db_connection():
    conn = sqlite3.connect('school.db')
    return conn

# Database connection setup
conn = sqlite3.connect('school.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS classes (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    capacity INTEGER
)''')

c.execute('''CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    class_id INTEGER,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE
)''')

c.execute('''CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY,
    name TEXT,
    student_id INTEGER,
    score INTEGER DEFAULT -1,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
)''')

conn.commit()

# Close connection on script exit
import atexit
@atexit.register
def close_connection():
    conn.close()
