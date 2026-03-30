from database.connection import get_connection


class Student:

    def get_all():
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT student_id, student_code, last_name, first_name, middle_name,
                       birth_date, gender, phone, email, group_name, course, faculty, is_active
                FROM students
                ORDER BY last_name, first_name
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print(f"Ошибка получения студентов: {e}")
            return []

    def add(student_code, last_name, first_name, middle_name=None, birth_date=None,
            gender='м', phone=None, email=None, group_name=None, course=None, faculty=None):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO students (student_code, last_name, first_name, middle_name,
                                      birth_date, gender, phone, email, group_name, course, faculty)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (student_code, last_name, first_name, middle_name, birth_date,
                  gender, phone, email, group_name, course, faculty))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка добавления студента: {e}")
            return False

    def update(student_id, student_code, last_name, first_name, middle_name=None, birth_date=None,
               gender='м', phone=None, email=None, group_name=None, course=None, faculty=None):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE students
                SET student_code=%s, last_name=%s, first_name=%s, middle_name=%s,
                    birth_date=%s, gender=%s, phone=%s, email=%s, group_name=%s, course=%s, faculty=%s
                WHERE student_id=%s
            """, (student_code, last_name, first_name, middle_name, birth_date,
                  gender, phone, email, group_name, course, faculty, student_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка обновления студента: {e}")
            return False

    def delete(student_id):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE students SET is_active = FALSE WHERE student_id = %s", (student_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка удаления студента: {e}")
            return False
