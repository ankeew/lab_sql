# Таблица залов и особые действия с ней

from dbtable import *
import psycopg2

class HallTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "halls"

    def columns(self):
        # Используем OrderedDict для гарантированного порядка
        from collections import OrderedDict
        cols = OrderedDict()
        cols["hall_id"] = ["serial", "PRIMARY KEY"]
        cols["full_name"] = ["varchar(64)", "NOT NULL CHECK (length(trim(full_name)) > 0)"]
        cols["short_name"] = ["varchar(64)", "NOT NULL CHECK (length(trim(short_name)) > 0)"]
        return cols

    def table_constraints(self):
        return ["UNIQUE(full_name)", "UNIQUE(short_name)"]

    def primary_key(self):
        return ["hall_id"]

    def all(self):
        sql = "SELECT hall_id, full_name, short_name FROM " + self.table_name()
        sql += " ORDER BY hall_id"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

    def find_by_full_name(self, full_name):
        sql = "SELECT hall_id, full_name, short_name FROM " + self.table_name()
        sql += " WHERE full_name = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (full_name,))
        return cur.fetchone()

    def find_by_short_name(self, short_name):
        sql = "SELECT hall_id, full_name, short_name FROM " + self.table_name()
        sql += " WHERE short_name = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (short_name,))
        return cur.fetchone()

    def find_by_position(self, num):
        sql = "SELECT hall_id, full_name, short_name FROM " + self.table_name()
        sql += " ORDER BY full_name"
        sql += " LIMIT 1 OFFSET %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (num - 1,))
        return cur.fetchone()

    def find_by_id(self, hall_id):
        sql = "SELECT hall_id, full_name, short_name FROM " + self.table_name()
        sql += " WHERE hall_id = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (hall_id,))
        return cur.fetchone()

    def insert_hall(self, full_name, short_name):
        # ✅ ЯВНО указываем столбцы для вставки
        sql = "INSERT INTO " + self.table_name() + " (full_name, short_name)"
        sql += " VALUES (%s, %s)"
        cur = self.dbconn.conn.cursor()
        try:
            cur.execute(sql, (full_name, short_name))
            self.dbconn.conn.commit()
            return True, "Зал добавлен!"
        except psycopg2.errors.UniqueViolation:
            self.dbconn.conn.rollback()
            return False, "Ошибка: зал с таким полным или кратким названием уже существует!"
        except psycopg2.errors.CheckViolation:
            self.dbconn.conn.rollback()
            return False, "Ошибка: названия не могут быть пустыми или содержать только пробелы!"
        except psycopg2.errors.NotNullViolation:
            self.dbconn.conn.rollback()
            return False, "Ошибка: все поля обязательны для заполнения!"
        except Exception as e:
            self.dbconn.conn.rollback()
            return False, f"Ошибка при добавлении зала: {str(e)}"

    def update_hall(self, hall_id, full_name, short_name):
        sql = "UPDATE " + self.table_name()
        sql += " SET full_name = %s, short_name = %s WHERE hall_id = %s"
        cur = self.dbconn.conn.cursor()
        try:
            cur.execute(sql, (full_name, short_name, hall_id))
            self.dbconn.conn.commit()
            return True, "Зал обновлен!"
        except psycopg2.errors.UniqueViolation:
            self.dbconn.conn.rollback()
            return False, "Ошибка: зал с таким полным или кратким названием уже существует!"
        except psycopg2.errors.CheckViolation:
            self.dbconn.conn.rollback()
            return False, "Ошибка: названия не могут быть пустыми или содержать только пробелы!"
        except Exception as e:
            self.dbconn.conn.rollback()
            return False, f"Ошибка при обновлении зала: {str(e)}"

    def delete_by_id(self, hall_id):
        sql = "DELETE FROM " + self.table_name()
        sql += " WHERE hall_id = %s"
        cur = self.dbconn.conn.cursor()
        try:
            cur.execute(sql, (hall_id,))
            self.dbconn.conn.commit()
            return True, "Зал удален!"
        except psycopg2.errors.ForeignKeyViolation:
            self.dbconn.conn.rollback()
            return False, "Ошибка: нельзя удалить зал, так как есть связанные стеллажи!"
        except Exception as e:
            self.dbconn.conn.rollback()
            return False, f"Ошибка при удалении зала: {str(e)}"

    def count(self):
        sql = "SELECT COUNT(*) FROM " + self.table_name()
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()[0]

    def all_page(self, page, page_size):
        sql = "SELECT hall_id, full_name, short_name FROM " + self.table_name()
        sql += " ORDER BY full_name"
        sql += " LIMIT %s OFFSET %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (page_size, (page - 1) * page_size))
        return cur.fetchall()