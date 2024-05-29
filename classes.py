from database import get_db_connection

class ClassManager:

    def add_class(self, class_name, class_capacity):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO classes (name, capacity) VALUES (?, ?)", (class_name, class_capacity))
        class_id = c.lastrowid
        conn.commit()
        conn.close()
        return class_id

    def get_all_class_record(self):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM classes")
        classes = c.fetchall()
        conn.close()
        return classes
    
    def get_class_record(self, class_name):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM classes WHERE name = ?', (class_name,))
        class_record = c.fetchone()
        if class_record:
            return class_record
        else:
            return None

    def find_num_students(self, class_name):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            SELECT COUNT(students.id) FROM students
            JOIN classes ON students.class_id = classes.id
            WHERE classes.name = ?
        ''', (class_name,))
        num_students = c.fetchone()[0]
        return num_students

    def get_all_class_field(self, field_num):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM classes')
        class_records = c.fetchall()
        field_values = [record[field_num] for record in class_records]
        return field_values
