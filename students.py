from database import get_db_connection

class StudentManager:
    def add_student(self, name, class_id):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO students (name, class_id) VALUES (?, ?)", (name, class_id))
        conn.commit()
        conn.close()

    def get_student_id(self, student_name, class_name):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            SELECT students.id FROM students
            JOIN classes ON students.class_id = classes.id
            WHERE students.name = ? AND classes.name = ?
        ''', (student_name, class_name))
        student_id = c.fetchone()
        conn.close()
        if student_id:
            return student_id[0]
        else:
            return None
        
    def get_students(self):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM students")
        students = c.fetchall()
        conn.close()
        return students

    def transfer_student(self, student_id, new_class_id):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("UPDATE students SET class_id = ? WHERE id = ?", (new_class_id, student_id))
        conn.commit()
        conn.close()

    def delete_student(self, student_id):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        conn.close()

    def get_students_by_class(self, class_name):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            SELECT students.* FROM students
            JOIN classes ON students.class_id = classes.id
            WHERE classes.name = ?
        ''', (class_name,))
        students = c.fetchall()
        conn.close()
        return students