-- 1. Просмотр истории объекта
SELECT * FROM get_object_history('furniture', 1);

-- 2. Восстановление версии объекта на определенную дату
-- Восстановление состояния на 25 марта 2025, 13:13:00 (версия с материалом "Wood")
SELECT restore_object_version('furniture', 1, '2025-03-25 13:13:00');

-- Проверяем результат
SELECT * FROM get_object_history('furniture', 1) LIMIT 3;
-- 3. Сравнение двух версий объекта
SELECT * FROM compare_object_versions(
    'furniture',
    1,
    '2025-03-25 13:13:00',
    '2025-04-15 12:26:00');

-- 4. Получение состояния таблицы на определенный момент времени
-- Получение состояния таблицы на 25 марта 2025, 13:13:30
SELECT * FROM get_table_history('furniture', '2025-03-25 13:13:30') AS (
    id INT,
    time_create TIMESTAMP,
    time_dead TIMESTAMP,
    material VARCHAR(50),
    dimensions VARCHAR(50)
);
