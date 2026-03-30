from database.connection import get_connection


class Floor:

    def get_all():
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT f.floor_id, f.building_id, b.name, f.floor_number, f.total_rooms
                FROM floors f
                JOIN buildings b ON f.building_id = b.building_id
                ORDER BY b.name, f.floor_number
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print(f"Ошибка получения этажей: {e}")
            return []

    def add(building_id, floor_number, total_rooms=0):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO floors (building_id, floor_number, total_rooms)
                VALUES (%s, %s, %s)
            """, (building_id, floor_number, total_rooms))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка добавления этажа: {e}")
            return False

    def update(floor_id, building_id, floor_number, total_rooms=0):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE floors
                SET building_id=%s, floor_number=%s, total_rooms=%s
                WHERE floor_id=%s
            """, (building_id, floor_number, total_rooms, floor_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка обновления этажа: {e}")
            return False

    def delete(floor_id):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM floors WHERE floor_id = %s", (floor_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка удаления этажа: {e}")
            return False
