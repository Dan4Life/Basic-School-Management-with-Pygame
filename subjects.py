from database import get_db_connection

class SubjectManager:

    def add_subjects(self, student_id, subjects):
        conn = get_db_connection()
        c = conn.cursor()
        for subject in subjects:
            c.execute('INSERT INTO subjects (name, student_id, score) VALUES (?, ?, ?)', (subject, student_id, -1))
        conn.commit()
        conn.close()

    def get_subjects(self):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM subjects")
        subjects = c.fetchall()
        conn.close()
        return subjects

    def get_average_score(self, subject_name, class_id):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''SELECT AVG(subjects.score) FROM subjects
                     JOIN students ON subjects.student_id = students.id
                     JOIN classes ON students.class_id = classes.id
                     WHERE subjects.name = ? AND classes.id = ?
                     AND subjects.score != -1 AND subjects.score IS NOT NULL''', 
                     (subject_name, class_id))
        avg_score = c.fetchone()[0]
        conn.close()
        return avg_score
    
    def get_student_subjects(self, student_id):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM subjects WHERE student_id = ?", (student_id,))
        subjects = c.fetchall()
        conn.close()
        return subjects

    def update_subject_score(self, student_id, subject_id, new_score):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            UPDATE subjects
            SET score = ?
            WHERE student_id = ? AND id = ?
        ''', (new_score, student_id, subject_id))
        print("Successfully Updated!")
        conn.commit()
        conn.close()

    def delete_subject_score(self, student_id, subject_id):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            UPDATE subjects
            SET score = -1
            WHERE student_id = ? AND id = ?
        ''', (student_id, subject_id))
        conn.commit()
        conn.close()