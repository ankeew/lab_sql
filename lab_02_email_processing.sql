-- 2. ОБРАБОТКА EMAIL-АДРЕСОВ
-- Преобразует email к формату "ab_@domain.com":
-- - если email короче 3 символов до @ — оставляет как есть,
-- - иначе оставляет первые 2 символа, ставит "_", затем "@" и домен.
-- Пример: john.doe@example.com → jo_@example.com
SELECT 
  last_name,
  email,
  CASE 
    WHEN email LIKE '__@%' THEN email
    ELSE REGEXP_REPLACE(
      email,
      '^(.{2}).*?(@)',  
      '\1_\2'           
    )
  END AS modified_email
FROM employees be;