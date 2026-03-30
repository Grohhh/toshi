from database.connection import get_connection


class Room:

    STATUSES = ['свободна', 'занята', 'в ремонте', 'забронирована']

    def get_all():
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    r.room_id, r.room_number, r.total_beds, r.occupied_beds,
                    r.room_type, r.status, r.floor_area,
                    f.floor_number, b.name
                FROM rooms r
                JOIN floors f ON r.floor_id = f.floor_id
                JOIN buildings b ON f.building_id = b.building_id
                ORDER BY b.name, f.floor_number, r.room_number
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print(f"Ошибка получения комнат: {e}")
            return []

    def add(floor_id, room_number, total_beds=1, room_type='стандарт', status='свободна', floor_area=None):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO rooms (floor_id, room_number, total_beds, room_type, status, floor_area)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (floor_id, room_number, total_beds, room_type, status, floor_area))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка добавления комнаты: {e}")
            return False

    def update(room_id, floor_id, room_number, total_beds=1, room_type='стандарт', status='свободна', floor_area=None):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE rooms
                SET floor_id=%s, room_number=%s, total_beds=%s, room_type=%s, status=%s, floor_area=%s
                WHERE room_id=%s
            """, (floor_id, room_number, total_beds, room_type, status, floor_area, room_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка обновления комнаты: {e}")
            return False

    def delete(room_id):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            # Вместо удаления меняем статус на "в ремонте"
            cursor.execute("UPDATE rooms SET status = 'в ремонте' WHERE room_id = %s", (room_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка деактивации комнаты: {e}")
            return False

    def change_status(room_id, new_status):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE rooms SET status = %s WHERE room_id = %s", (new_status, room_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка изменения статуса: {e}")
            return False
