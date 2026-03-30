from database.connection import get_connection


class Building:

    def get_all():
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT building_id, name, address, total_floors, built_year, is_active
                FROM buildings
                ORDER BY name
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print(f"Ошибка получения корпусов: {e}")
            return []

    def add(name, address=None, total_floors=1, built_year=None):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO buildings (name, address, total_floors, built_year)
                VALUES (%s, %s, %s, %s)
            """, (name, address, total_floors, built_year))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка добавления корпуса: {e}")
            return False

    def update(building_id, name, address=None, total_floors=1, built_year=None):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE buildings
                SET name=%s, address=%s, total_floors=%s, built_year=%s
                WHERE building_id=%s
            """, (name, address, total_floors, built_year, building_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка обновления корпуса: {e}")
            return False

    def delete(building_id):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE buildings SET is_active = FALSE WHERE building_id = %s", (building_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка удаления корпуса: {e}")
            return False
