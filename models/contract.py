from database.connection import get_connection


class Contract:

    def get_all():
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    c.contract_id,
                    c.contract_number,
                    c.contract_date,
                    s.last_name || ' ' || s.first_name,
                    r.room_number,
                    c.start_date,
                    c.end_date,
                    c.monthly_fee,
                    c.status
                FROM contracts c
                JOIN students s ON c.student_id = s.student_id
                JOIN rooms r ON c.room_id = r.room_id
                ORDER BY c.contract_id DESC
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print(f"Ошибка получения договоров: {e}")
            return []

    def add(contract_number, student_id, room_id, start_date, end_date, monthly_fee=0):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO contracts (contract_number, student_id, room_id, start_date, end_date, monthly_fee)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (contract_number, student_id, room_id, start_date, end_date, monthly_fee))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка добавления договора: {e}")
            return False

    def update(contract_id, contract_number, student_id, room_id, start_date, end_date, monthly_fee=0):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE contracts
                SET contract_number=%s, student_id=%s, room_id=%s, start_date=%s, end_date=%s, monthly_fee=%s
                WHERE contract_id=%s
            """, (contract_number, student_id, room_id, start_date, end_date, monthly_fee, contract_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка обновления договора: {e}")
            return False

    def delete(contract_id):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM contracts WHERE contract_id = %s", (contract_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка удаления договора: {e}")
            return False
