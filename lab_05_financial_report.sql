-- 5. ФИНАНСОВЫЙ ОТЧЁТ ПО СЧЁТУ (ХРАНИМАЯ ПРОЦЕДУРА)
-- Генерирует отчёт по банковским операциям за период:
--   - Топ-3 пополнений (положительные суммы),
--   - Топ-3 списаний (отрицательные суммы),
--   - Общее количество операций,
--   - Средняя сумма операции.
-- Использует JOIN между operations и operations_log.
CREATE OR REPLACE PROCEDURE statement_of_acount(
  start_d TIMESTAMP,
  end_d TIMESTAMP,
  account VARCHAR(20)
) AS $$
DECLARE
  avg_o FLOAT;
  count_o INTEGER;
  l RECORD;
BEGIN
  RAISE INFO 'три самые крупные операции с положительной суммой';
  FOR l IN (
    SELECT o_l.operation_type, o.operation_sum, o_l.operation_date
    FROM operations_log o_l 
    JOIN operations o ON o.id = o_l.operation_id
    WHERE o.account_number = account 
      AND o_l.operation_date BETWEEN start_d AND end_d 
      AND o.operation_sum > 0 
    ORDER BY o.operation_sum DESC 
    LIMIT 3
  ) LOOP
    RAISE INFO 'Тип: %, Сумма: %, Дата: %', 
      l.operation_type, 
      l.operation_sum, 
      l.operation_date;
  END LOOP;

  RAISE INFO 'три самые крупные операции с отрицательной суммой';
  FOR l IN (
    SELECT o_l.operation_type, o.operation_sum, o_l.operation_date
    FROM operations_log o_l 
    JOIN operations o ON o.id = o_l.operation_id
    WHERE o.account_number = account 
      AND o_l.operation_date BETWEEN start_d AND end_d 
      AND o.operation_sum < 0 
    ORDER BY o.operation_sum ASC 
    LIMIT 3
  ) LOOP
    RAISE INFO 'Тип: %, Сумма: %, Дата: %', 
      l.operation_type, 
      l.operation_sum, 
      l.operation_date;
  END LOOP;

  SELECT COUNT(*), AVG(o.operation_sum) INTO count_o, avg_o
  FROM operations o 
  JOIN operations_log ol ON o.id = ol.operation_id
  WHERE ol.account_number = account
    AND ol.operation_date BETWEEN start_d AND end_d;

  RAISE INFO 'общее количество операций: %', count_o;
  RAISE INFO 'среднее значение суммы: %', COALESCE(avg_o, 0);
END
$$ LANGUAGE plpgsql;

-- Вызов процедуры для примера
CALL statement_of_acount('2024-01-15', '2024-01-24', '40817810099910004312');