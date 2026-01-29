-- 4. ИЗВЛЕЧЕНИЕ ТЕХНОЛОГИЙ ИЗ ТЕКСТОВОГО ПОЛЯ
-- Анализирует поле work_description для извлечения слов (латиницей),
-- предполагая, что это названия технологий (Python, SQL, Docker и т.д.).
-- Группирует по сотруднику и объединяет уникальные технологии через запятую.
WITH tech AS (
  SELECT 
    ln,
    fn,
    sn,
    regexp_matches(work_description, '[A-Za-z]+', 'g') AS tech_match
  FROM workers
)
SELECT 
  ln,
  fn,
  sn,
  STRING_AGG(DISTINCT tech_match[1], ', ' ORDER BY tech_match[1]) AS technologies
FROM tech
GROUP BY ln, fn, sn;