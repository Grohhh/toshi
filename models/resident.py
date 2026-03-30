from database.connection import get_connection


class Resident:

    def get_all():
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    res.resident_id,
                    s.student_code,
                    s.last_name || ' ' || s.first_name || ' ' || s.middle_name,
                    r.room_number,
                    res.bed_number,
                    res.check_in_date,
                    res.contract_number,
                    res.status
                FROM residents res
                JOIN students s ON res.student_id = s.student_id
                JOIN rooms r ON res.room_id = r.room_id
                ORDER BY res.resident_id DESC
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print(f"Ошибка получения проживающих: {e}")
            return []

    def add(student_id, room_id, bed_number, check_in_date=None, contract_number=None, contract_date=None):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO residents (student_id, room_id, bed_number, check_in_date, contract_number, contract_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (student_id, room_id, bed_number, check_in_date, contract_number, contract_date))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка добавления проживающего: {e}")
            return False

    def update(resident_id, student_id, room_id, bed_number):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE residents
                SET student_id=%s, room_id=%s, bed_number=%s
                WHERE resident_id=%s
            """, (student_id, room_id, bed_number, resident_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка обновления проживающего: {e}")
            return False

    def delete(resident_id):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM residents WHERE resident_id = %s", (resident_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка удаления проживающего: {e}")
            return False

    def checkout(resident_id):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE residents
                SET status = 'выселен', check_out_date = CURRENT_DATE
                WHERE resident_id = %s
            """, (resident_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка выселения: {e}")
            return False
