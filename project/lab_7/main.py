import sys
sys.path.append('tables')

from project_config import *
from dbconnection import *
from tables.hall_table import *
from tables.shelf_table import *

class Main:

    config = ProjectConfig()
    connection = DbConnection(config)
    PAGE_SIZE = 5

    def __init__(self):
        DbTable.dbconn = self.connection
        return

    def db_init(self):
        ht = HallTable()
        st = ShelfTable()
        ht.create()
        st.create()
        return

    def db_insert_somethings(self):
        ht = HallTable()
        st = ShelfTable()
        
        ht.insert_hall("Главный читальный зал", "ГЧЗ")
        ht.insert_hall("Зал периодических изданий", "ЗПИ")
        ht.insert_hall("Зал научной литературы", "ЗНЛ")
        ht.insert_hall("Детский зал", "ДЗ")
        ht.insert_hall("Зал редких книг", "ЗРК")
        
        hall1 = ht.find_by_short_name("ГЧЗ")
        hall2 = ht.find_by_short_name("ЗПИ")
        hall3 = ht.find_by_short_name("ЗНЛ")
        
        if hall1:
            st.insert_shelf(hall1[0], 1)
            st.insert_shelf(hall1[0], 2)
            st.insert_shelf(hall1[0], 3)
        
        if hall2:
            st.insert_shelf(hall2[0], 1)
            st.insert_shelf(hall2[0], 2)
        
        if hall3:
            st.insert_shelf(hall3[0], 1)
        
        return

    def db_drop(self):
        st = ShelfTable()
        ht = HallTable()
        st.drop()
        ht.drop()
        return

    def show_main_menu(self):
        menu = """Добро пожаловать в систему управления залами и стеллажами!
Основное меню (выберите цифру в соответствии с необходимым действием):
    1 - просмотр залов;
    2 - сброс и инициализация таблиц;
    9 - выход."""
        print(menu)
        return

    def read_next_step(self):
        return input("=> ").strip()

    def after_main_menu(self, next_step):
        if next_step == "2":
            confirm = input("Вы уверены? Все данные будут удалены! (да/нет): ").strip()
            if confirm == "да":
                self.db_drop()
                self.db_init()
                self.db_insert_somethings()
                print("Таблицы созданы заново и заполнены тестовыми данными!")
            else:
                print("Операция отменена!")
            return "0"
        elif next_step != "1" and next_step != "9":
            print("Выбрано неверное число! Повторите ввод!")
            return "0"
        else:
            return next_step

    def show_halls(self):
        self.hall_id = -1
        self._halls_page = 1
        self._show_halls_page(1)
        return

    def after_show_halls(self, next_step):
        while True:
            if next_step == "3":
                self.show_add_hall()
                self._show_halls_page(self._halls_page)
                next_step = self.read_next_step()
            elif next_step == "4":
                self.show_edit_hall()
                self._show_halls_page(self._halls_page)
                next_step = self.read_next_step()
            elif next_step == "5":
                self.show_delete_hall()
                self._show_halls_page(self._halls_page)
                next_step = self.read_next_step()
            elif next_step == "6":
                next_step = self.show_shelves_by_hall()
            elif next_step == "7":
                ht = HallTable()
                total = ht.count()
                total_pages = (total + self.PAGE_SIZE - 1) // self.PAGE_SIZE
                if self._halls_page < total_pages:
                    self._halls_page += 1
                else:
                    print("Это последняя страница!")
                self._show_halls_page(self._halls_page)
                next_step = self.read_next_step()
            elif next_step == "8":
                if self._halls_page > 1:
                    self._halls_page -= 1
                else:
                    print("Это первая страница!")
                self._show_halls_page(self._halls_page)
                next_step = self.read_next_step()
            elif next_step != "0" and next_step != "9":
                print("Выбрано неверное число! Повторите ввод!")
                next_step = self.read_next_step()
            else:
                return next_step

    def _show_halls_page(self, page):
        ht = HallTable()
        total = ht.count()
        if total == 0:
            print("\n=== Список залов пуст! ===\n")
            menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    3 - добавление нового зала;
    9 - выход."""
            print(menu)
            return
        
        total_pages = (total + self.PAGE_SIZE - 1) // self.PAGE_SIZE
        offset = (page - 1) * self.PAGE_SIZE
        lst = ht.all_page(page, self.PAGE_SIZE)
        
        print(f"\n=== Просмотр списка залов! Страница {page} из {total_pages} ===")
        print(f"{'№':<5} {'Полное название':<35} {'Краткое название':<20}")
        print("-" * 65)
        for i, row in enumerate(lst, offset + 1):
            print(f"{i:<5} {row[1]:<35} {row[2]:<20}")
        
        menu = """
Дальнейшие операции:
    0 - возврат в главное меню;
    3 - добавление нового зала;
    4 - изменение зала;
    5 - удаление зала;
    6 - просмотр стеллажей зала;
    7 - следующая страница;
    8 - предыдущая страница;
    9 - выход."""
        print(menu)
        self._halls_page = page
        self._halls_offset = offset
        return

    def validate_string_input(self, value, field_name, max_length=64, allow_empty=False):
        """Валидация строковых данных"""
        value = value.strip()
        
        if not allow_empty and len(value) == 0:
            return False, f"{field_name} не может быть пустым!"
        
        if len(value) > max_length:
            return False, f"{field_name} слишком длинное (макс. {max_length} символов)!"
        
        if value.isspace():
            return False, f"{field_name} не может состоять только из пробелов!"
        
        if value.isdigit():
            return False, f"{field_name} не может являться не строкой!"

        return True, value

    def validate_integer_input(self, value, field_name, min_value=None, max_value=None):
        """Валидация целочисленных данных"""
        if not value.strip():
            return False, f"{field_name} не может быть пустым!", None
        
        if not value.strip().lstrip('-').isdigit():
            return False, f"{field_name} должно быть целым числом!", None
        
        try:
            int_value = int(value.strip())
        except ValueError:
            return False, f"{field_name} должно быть целым числом!", None
        
        if min_value is not None and int_value < min_value:
            return False, f"{field_name} должно быть не меньше {min_value}!", None
        
        if max_value is not None and int_value > max_value:
            return False, f"{field_name} должно быть не больше {max_value}!", None
        
        return True, "", int_value

    def show_add_hall(self):
        print("\n=== Добавление нового зала ===")
        
        # Ввод полного названия
        while True:
            full_name = input("Введите полное название зала (0 - отмена): ").strip()
            if full_name == "0":
                print("Добавление отменено!")
                return
            
            valid, message = self.validate_string_input(full_name, "Полное название")
            if not valid:
                print(message)
                continue
            
            full_name = message
            break
        
        # Ввод краткого названия
        while True:
            short_name = input("Введите краткое название зала (0 - отмена): ").strip()
            if short_name == "0":
                print("Добавление отменено!")
                return
            
            valid, message = self.validate_string_input(short_name, "Краткое название")
            if not valid:
                print(message)
                continue
            
            short_name = message
            break
        
        # Попытка добавить зал
        success, message = HallTable().insert_hall(full_name, short_name)
        print(message)
        return

    def show_edit_hall(self):
        print("\n=== Изменение зала ===")
        ht = HallTable()
        total = ht.count()
        
        if total == 0:
            print("Список залов пуст!")
            return
        
        while True:
            num = input(f"Укажите номер строки зала для изменения (1-{total}, 0 - отмена): ").strip()
            if num == "0":
                print("Изменение отменено!")
                return
            
            valid, message, num_int = self.validate_integer_input(num, "Номер строки", 1, total)
            if not valid:
                print(message)
                continue
            
            hall = ht.find_by_position(num_int)
            if not hall:
                print(f"Зал с номером {num_int} не найден!")
                continue
            
            break
        
        print(f"\nВыбран зал:")
        print(f"  Полное название: {hall[1]}")
        print(f"  Краткое название: {hall[2]}")
        
        # Ввод нового полного названия
        while True:
            full_name = input(f"Новое полное название [{hall[1]}] (Enter - оставить, 0 - отмена): ").strip()
            if full_name == "0":
                print("Изменение отменено!")
                return
            
            if full_name == "":
                full_name = hall[1]
                break
            
            valid, message = self.validate_string_input(full_name, "Полное название")
            if not valid:
                print(message)
                continue
            
            full_name = message
            break
        
        # Ввод нового краткого названия
        while True:
            short_name = input(f"Новое краткое название [{hall[2]}] (Enter - оставить, 0 - отмена): ").strip()
            if short_name == "0":
                print("Изменение отменено!")
                return
            
            if short_name == "":
                short_name = hall[2]
                break
            
            valid, message = self.validate_string_input(short_name, "Краткое название")
            if not valid:
                print(message)
                continue
            
            short_name = message
            break
        
        # Попытка обновить зал
        success, message = ht.update_hall(hall[0], full_name, short_name)
        print(message)
        return

    def show_delete_hall(self):
        print("\n=== Удаление зала ===")
        ht = HallTable()
        total = ht.count()
        
        if total == 0:
            print("Список залов пуст!")
            return
        
        while True:
            num = input(f"Укажите номер строки зала для удаления (1-{total}, 0 - отмена): ").strip()
            if num == "0":
                print("Удаление отменено!")
                return
            
            valid, message, num_int = self.validate_integer_input(num, "Номер строки", 1, total)
            if not valid:
                print(message)
                continue
            
            hall = ht.find_by_position(num_int)
            if not hall:
                print(f"Зал с номером {num_int} не найден!")
                continue
            
            break
        
        print(f"\nВыбран зал для удаления:")
        print(f"  Полное название: {hall[1]}")
        print(f"  Краткое название: {hall[2]}")
        
        # Проверка связанных стеллажей
        st = ShelfTable()
        if st.has_shelves_for_hall(hall[0]):
            shelves_count = st.count_by_hall(hall[0])
            print(f"\nВНИМАНИЕ! В этом зале есть {shelves_count} стеллаж(ей)!")
        
        confirm = input("\nВы уверены, что хотите удалить этот зал? (да/нет): ").strip()
        if confirm == "да":
            success, message = ht.delete_by_id(hall[0])
            print(message)
        else:
            print("Удаление отменено!")
        return

    def show_shelves_by_hall(self):
        print("\n=== Просмотр стеллажей зала ===")
        ht = HallTable()
        total = ht.count()
        
        if total == 0:
            print("Список залов пуст! Сначала добавьте зал.")
            return "1"
        
        if self.hall_id == -1:
            while True:
                num = input(f"Укажите номер строки зала (1-{total}, 0 - отмена): ").strip()
                if num == "0":
                    return "1"
                
                valid, message, num_int = self.validate_integer_input(num, "Номер строки", 1, total)
                if not valid:
                    print(message)
                    continue
                
                hall = ht.find_by_position(num_int)
                if not hall:
                    print(f"Зал с номером {num_int} не найден!")
                    continue
                
                self.hall_id = hall[0]
                self.hall_obj = hall
                break
        
        print(f"\n=== Зал: {self.hall_obj[1]} ({self.hall_obj[2]}) ===")
        
        st = ShelfTable()
        lst = st.all_by_hall_id(self.hall_id)
        
        if not lst:
            print("\nВ этом зале пока нет стеллажей.")
        else:
            print(f"\n{'№':<5} {'Индекс стеллажа':<20}")
            print("-" * 30)
            for i, row in enumerate(lst, 1):
                print(f"{i:<5} {row[4]:<20}")
        
        menu = """
Дальнейшие операции:
    0 - возврат в главное меню;
    1 - возврат к просмотру залов;
    2 - добавление нового стеллажа;
    3 - изменение стеллажа;
    4 - удаление стеллажа;
    9 - выход."""
        print(menu)
        next_step = self.read_next_step()
        
        while True:
            if next_step == "2":
                self.show_add_shelf()
                next_step = self.show_shelves_by_hall()
            elif next_step == "3":
                self.show_edit_shelf(lst)
                next_step = self.show_shelves_by_hall()
            elif next_step == "4":
                self.show_delete_shelf(lst)
                next_step = self.show_shelves_by_hall()
            elif next_step == "0" or next_step == "1" or next_step == "9":
                self.hall_id = -1
                return next_step
            else:
                print("Выбрано неверное число! Повторите ввод!")
                next_step = self.read_next_step()

    def show_add_shelf(self):
        print(f"\n=== Добавление стеллажа в зал: {self.hall_obj[1]} ===")
        
        while True:
            shelf_index = input("Введите индекс стеллажа (положительное целое число, 0 - отмена): ").strip()
            if shelf_index == "0":
                print("Добавление отменено!")
                return
            
            valid, message, index_int = self.validate_integer_input(shelf_index, "Индекс стеллажа", 1)
            if not valid:
                print(message)
                continue
            
            break
        
        # Попытка добавить стеллаж
        success, message = ShelfTable().insert_shelf(self.hall_id, index_int)
        print(message)
        return

    def show_edit_shelf(self, lst):
        print(f"\n=== Изменение стеллажа в зале: {self.hall_obj[1]} ===")
        
        if not lst:
            print("Список стеллажей пуст!")
            return
        
        while True:
            num = input(f"Укажите номер строки стеллажа для изменения (1-{len(lst)}, 0 - отмена): ").strip()
            if num == "0":
                print("Изменение отменено!")
                return
            
            valid, message, num_int = self.validate_integer_input(num, "Номер строки", 1, len(lst))
            if not valid:
                print(message)
                continue
            
            shelf = lst[num_int - 1]
            break
        
        print(f"\nВыбран стеллаж с индексом: {shelf[4]}")
        
        # Ввод нового индекса
        while True:
            new_index = input(f"Новый индекс стеллажа [{shelf[4]}] (Enter - оставить, 0 - отмена): ").strip()
            if new_index == "0":
                print("Изменение отменено!")
                return
            
            if new_index == "":
                new_index = shelf[4]
                break
            
            valid, message, index_int = self.validate_integer_input(new_index, "Индекс стеллажа", 1)
            if not valid:
                print(message)
                continue
            
            new_index = index_int
            break
        
        # Попытка обновить стеллаж
        success, message = ShelfTable().update_shelf(shelf[0], self.hall_id, new_index)
        print(message)
        return

    def show_delete_shelf(self, lst):
        print(f"\n=== Удаление стеллажа из зала: {self.hall_obj[1]} ===")
        
        if not lst:
            print("Список стеллажей пуст!")
            return
        
        while True:
            num = input(f"Укажите номер строки стеллажа для удаления (1-{len(lst)}, 0 - отмена): ").strip()
            if num == "0":
                print("Удаление отменено!")
                return
            
            valid, message, num_int = self.validate_integer_input(num, "Номер строки", 1, len(lst))
            if not valid:
                print(message)
                continue
            
            shelf = lst[num_int - 1]
            break
        
        print(f"\nВыбран стеллаж для удаления:")
        print(f"  Индекс: {shelf[4]}")
        
        confirm = input("\nВы уверены, что хотите удалить этот стеллаж? (да/нет): ").strip()
        if confirm == "да":
            success, message = ShelfTable().delete_by_id(shelf[0])
            print(message)
        else:
            print("Удаление отменено!")
        return

    def main_cycle(self):
        current_menu = "0"
        next_step = None
        while current_menu != "9":
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
            elif current_menu == "1":
                self.show_halls()
                next_step = self.read_next_step()
                current_menu = self.after_show_halls(next_step)
        print("\nДо свидания!")
        return

    def test(self):
        DbTable.dbconn.test()

if __name__ == "__main__":
    m = Main()
    m.main_cycle()