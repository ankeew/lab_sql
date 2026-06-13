# Таблица стеллажей и особые действия с ней

from dbtable import *
import psycopg2

class ShelfTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "shelves"

    def columns(self):
        # Используем OrderedDict для гарантированного порядка
        from collections import OrderedDict
        cols = OrderedDict()
        cols["shelf_id"] = ["serial", "PRIMARY KEY"]
        cols["hall_id"] = ["integer", "NOT NULL REFERENCES " +
                           self.dbconn.prefix + "halls(hall_id) ON DELETE CASCADE"]
        cols["shelf_index"] = ["integer", "NOT NULL CHECK (shelf_index > 0)"]
        return cols

    def table_constraints(self):
        return ["UNIQUE(hall_id, shelf_index)"]

    def primary_key(self):
        return ["shelf_id"]

    def all(self):
        sql = "SELECT s.shelf_id, s.hall_id, h.full_name, h.short_name, s.shelf_index"
        sql += " FROM " + self.table_name() + " s"
        sql += " JOIN " + self.dbconn.prefix + "halls h ON s.hall_id = h.hall_id"
        sql += " ORDER BY s.shelf_id, h.full_name, s.shelf_index"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

    def all_by_hall_id(self, hall_id):
        sql = "SELECT s.shelf_id, s.hall_id, h.full_name, h.short_name, s.shelf_index"
        sql += " FROM " + self.table_name() + " s"
        sql += " JOIN " + self.dbconn.prefix + "halls h ON s.hall_id = h.hall_id"
        sql += " WHERE s.hall_id = %s"
        sql += " ORDER BY s.shelf_index"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (hall_id,))
        return cur.fetchall()

    def find_by_position_in_hall(self, hall_id, num):
        sql = "SELECT shelf_id, hall_id, shelf_index FROM " + self.table_name()
        sql += " WHERE hall_id = %s"
        sql += " ORDER BY shelf_index"
        sql += " LIMIT 1 OFFSET %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (hall_id, num - 1))
        return cur.fetchone()

    def insert_shelf(self, hall_id, shelf_index):
        # ✅ ЯВНО указываем столбцы для вставки
        sql = "INSERT INTO " + self.table_name() + " (hall_id, shelf_index)"
        sql += " VALUES (%s, %s)"
        cur = self.dbconn.conn.cursor()
        try:
            cur.execute(sql, (hall_id, shelf_index))
            self.dbconn.conn.commit()
            return True, "Стеллаж добавлен!"
        except psycopg2.errors.UniqueViolation:
            self.dbconn.conn.rollback()
            return False, "Ошибка: стеллаж с таким индексом уже существует в этом зале!"
        except psycopg2.errors.CheckViolation:
            self.dbconn.conn.rollback()
            return False, "Ошибка: индекс стеллажа должен быть положительным числом!"
        except psycopg2.errors.ForeignKeyViolation:
            self.dbconn.conn.rollback()
            return False, "Ошибка: указанный зал не существует!"
        except psycopg2.errors.NotNullViolation:
            self.dbconn.conn.rollback()
            return False, "Ошибка: все поля обязательны для заполнения!"
        except Exception as e:
            self.dbconn.conn.rollback()
            return False, f"Ошибка при добавлении стеллажа: {str(e)}"

    def update_shelf(self, shelf_id, hall_id, shelf_index):
        sql = "UPDATE " + self.table_name()
        sql += " SET hall_id = %s, shelf_index = %s WHERE shelf_id = %s"
        cur = self.dbconn.conn.cursor()
        try:
            cur.execute(sql, (hall_id, shelf_index, shelf_id))
            self.dbconn.conn.commit()
            return True, "Стеллаж обновлен!"
        except psycopg2.errors.UniqueViolation:
            self.dbconn.conn.rollback()
            return False, "Ошибка: стеллаж с таким индексом уже существует в этом зале!"
        except psycopg2.errors.CheckViolation:
            self.dbconn.conn.rollback()
            return False, "Ошибка: индекс стеллажа должен быть положительным числом!"
        except psycopg2.errors.ForeignKeyViolation:
            self.dbconn.conn.rollback()
            return False, "Ошибка: указанный зал не существует!"
        except Exception as e:
            self.dbconn.conn.rollback()
            return False, f"Ошибка при обновлении стеллажа: {str(e)}"

    def delete_by_id(self, shelf_id):
        sql = "DELETE FROM " + self.table_name()
        sql += " WHERE shelf_id = %s"
        cur = self.dbconn.conn.cursor()
        try:
            cur.execute(sql, (shelf_id,))
            self.dbconn.conn.commit()
            return True, "Стеллаж удален!"
        except Exception as e:
            self.dbconn.conn.rollback()
            return False, f"Ошибка при удалении стеллажа: {str(e)}"

    def has_shelves_for_hall(self, hall_id):
        sql = "SELECT 1 FROM " + self.table_name()
        sql += " WHERE hall_id = %s LIMIT 1"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (hall_id,))
        return cur.fetchone() is not None

    def count_by_hall(self, hall_id):
        sql = "SELECT COUNT(*) FROM " + self.table_name()
        sql += " WHERE hall_id = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (hall_id,))
        return cur.fetchone()[0]

    def all_by_hall_page(self, hall_id, page, page_size):
        sql = "SELECT s.shelf_id, s.hall_id, h.full_name, h.short_name, s.shelf_index"
        sql += " FROM " + self.table_name() + " s"
        sql += " JOIN " + self.dbconn.prefix + "halls h ON s.hall_id = h.hall_id"
        sql += " WHERE s.hall_id = %s"
        sql += " ORDER BY s.shelf_index"
        sql += " LIMIT %s OFFSET %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (hall_id, page_size, (page - 1) * page_size))
        return cur.fetchall()