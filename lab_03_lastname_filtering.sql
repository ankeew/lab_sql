-- 3. ФИЛЬТРАЦИЯ СОТРУДНИКОВ ПО КОРРЕКТНОЙ ФАМИЛИИ
-- Находит сотрудников с фамилиями, соответствующими шаблону:
--   - начинается с заглавной буквы,
--   - остальные буквы — строчные (латиница).
-- Пример: "Smith" — подходит, "McDonald" или "SMITH" — нет.
-- Выводит фамилию, улицу и почтовый индекс из связанной таблицы департаментов.
SELECT 
  bd_e.last_name, 
  bd_d.street, 
  bd_d.postal_code 
FROM employees bd_e
JOIN departments bd_d ON bd_d.id = bd_e.department_id
WHERE bd_e.last_name IN (
  SELECT last_name 
  FROM employees
  WHERE last_name ~ '^[A-Z][a-z]+$'
);