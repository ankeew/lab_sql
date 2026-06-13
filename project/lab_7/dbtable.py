# Базовые действия с таблицами

from dbconnection import *

class DbTable:
    dbconn = None

    def __init__(self):
        return

    def table_name(self):
        return self.dbconn.prefix + "table"

    def columns(self):
        return {"test": ["integer", "PRIMARY KEY"]}

    def column_names(self):
        return sorted(self.columns().keys(), key=lambda x: x)

    def primary_key(self):
        return ['id']

    def column_names_without_id(self):
        """Возвращает колонки для INSERT, исключая первичные ключи"""
        all_columns = sorted(self.columns().keys(), key=lambda x: x)
        # Получаем список первичных ключей
        pk_columns = self.primary_key()
        
        # Исключаем колонки, которые являются первичными ключами
        # Также исключаем колонки с auto-increment (serial)
        result = []
        for col in all_columns:
            if col not in pk_columns:
                # Проверяем, не является ли колонка serial/generated
                col_def = self.columns()[col]
                if 'serial' not in col_def:
                    result.append(col)
        return result

    def table_constraints(self):
        return []

    def create(self):
        sql = "CREATE TABLE " + self.table_name() + "("
        arr = [k + " " + " ".join(v) for k, v in sorted(self.columns().items(), key=lambda x: x[0])]
        sql += ", ".join(arr + self.table_constraints())
        sql += ")"
        cur = self.dbconn.conn.cursor()
        try:
            cur.execute(sql)
            self.dbconn.conn.commit()
        except Exception as e:
            self.dbconn.conn.rollback()
            raise e
        finally:
            cur.close()
        return

    def drop(self):
        sql = "DROP TABLE IF EXISTS " + self.table_name() + " CASCADE"
        cur = self.dbconn.conn.cursor()
        try:
            cur.execute(sql)
            self.dbconn.conn.commit()
        finally:
            cur.close()
        return

    def insert_one(self, vals):
        """Вставка одной записи"""
        columns = self.column_names_without_id()
        
        if len(vals) != len(columns):
            raise ValueError(f"Ожидается {len(columns)} значений, получено {len(vals)}")
        
        # Экранируем имена колонок двойными кавычками
        sql = "INSERT INTO " + self.table_name() + "("
        sql += ", ".join([f'"{col}"' for col in columns]) + ") VALUES("
        sql += ", ".join(["%s"] * len(vals)) + ")"
        
        print(f"DEBUG SQL: {sql}")  # Отладка
        print(f"DEBUG VALUES: {vals}")  # Отладка
        
        cur = self.dbconn.conn.cursor()
        try:
            cur.execute(sql, vals)
            self.dbconn.conn.commit()
            return True
        except Exception as e:
            self.dbconn.conn.rollback()
            raise e
        finally:
            cur.close()

    def first(self):
        pk_cols = self.primary_key()
        sql = "SELECT * FROM " + self.table_name()
        if pk_cols:
            order_clause = ", ".join([f'"{col}"' for col in pk_cols])
            sql += " ORDER BY " + order_clause
        cur = self.dbconn.conn.cursor()
        try:
            cur.execute(sql)
            return cur.fetchone()
        finally:
            cur.close()

    def last(self):
        pk_cols = self.primary_key()
        sql = "SELECT * FROM " + self.table_name()
        if pk_cols:
            order_clause = ", ".join([f'"{col}" DESC' for col in pk_cols])
            sql += " ORDER BY " + order_clause
        cur = self.dbconn.conn.cursor()
        try:
            cur.execute(sql)
            return cur.fetchone()
        finally:
            cur.close()

    def all(self):
        pk_cols = self.primary_key()
        sql = "SELECT * FROM " + self.table_name()
        if pk_cols:
            order_clause = ", ".join([f'"{col}"' for col in pk_cols])
            sql += " ORDER BY " + order_clause
        cur = self.dbconn.conn.cursor()
        try:
            cur.execute(sql)
            return cur.fetchall()
        finally:
            cur.close()