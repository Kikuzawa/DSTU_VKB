-- 1. Создаем функцию для получения состояния таблицы на определенный момент времени
CREATE OR REPLACE FUNCTION get_table_history(
    table_name TEXT,
    moment TIMESTAMP DEFAULT now()
) RETURNS SETOF RECORD AS $$
BEGIN
    RETURN QUERY EXECUTE format('
        SELECT * FROM %I
        WHERE time_create <= %L
        AND (time_dead IS NULL OR time_dead > %L)
        ORDER BY id, time_create',
        table_name, moment, moment);
END;
$$ LANGUAGE plpgsql;

-- 2. Создаем функцию для отката состояния объекта
CREATE OR REPLACE FUNCTION revert_object(
    target_table TEXT,
    object_id INT,
    revert_to TIMESTAMP
) RETURNS VOID AS $$
DECLARE
    latest_record RECORD;
    revert_record RECORD;
    col_name TEXT;
    col_list TEXT := '';
    value_list TEXT := '';
    query_text TEXT;
BEGIN
    -- Находим последнюю версию объекта
    EXECUTE format('
        SELECT * FROM %I 
        WHERE id = %s 
        ORDER BY time_create DESC 
        LIMIT 1',
        target_table, object_id) INTO latest_record;
    
    -- Если объект существует и не удален
    IF latest_record IS NOT NULL AND latest_record.time_dead IS NULL THEN
        -- Устанавливаем время смерти текущей версии
        EXECUTE format('
            UPDATE %I 
            SET time_dead = %L 
            WHERE id = %s AND time_create = %L',
            target_table, now(), object_id, latest_record.time_create);
    END IF;
    
    -- Находим версию для отката
    EXECUTE format('
        SELECT * FROM %I 
        WHERE id = %s AND time_create <= %L 
        AND (time_dead IS NULL OR time_dead > %L)
        ORDER BY time_create DESC 
        LIMIT 1',
        target_table, object_id, revert_to, revert_to) INTO revert_record;
    
    -- Если нашли версию для отката
    IF revert_record IS NOT NULL THEN
        -- Собираем список столбцов и значений для вставки
        FOR col_name IN 
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = target_table 
            AND column_name NOT IN ('id', 'time_create', 'time_dead')
        LOOP
            IF col_list <> '' THEN
                col_list := col_list || ', ';
                value_list := value_list || ', ';
            END IF;
            
            col_list := col_list || col_name;
            
            -- Получаем значение из revert_record по имени столбца
            EXECUTE format('SELECT ($1).%I::text', col_name) 
            USING revert_record 
            INTO value_list;
            
            -- Добавляем значение в список
            value_list := value_list || quote_literal(value_list);
        END LOOP;
        
        -- Формируем и выполняем запрос на вставку
        query_text := format('
            INSERT INTO %I (id, time_create, time_dead, %s)
            VALUES (%s, %L, NULL, %s)',
            target_table, col_list, object_id, now(), value_list);
        
        EXECUTE query_text;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- 3. Создаем представления для удобного доступа к истории изменений
CREATE OR REPLACE VIEW electronic_equipment_history AS
SELECT id, time_create, time_dead, warranty_period, manufacturer,
       CASE WHEN time_dead IS NULL THEN 'Active' ELSE 'Inactive' END AS status
FROM electronic_equipment
ORDER BY id, time_create;

CREATE OR REPLACE VIEW furniture_history AS
SELECT id, time_create, time_dead, material, dimensions,
       CASE WHEN time_dead IS NULL THEN 'Active' ELSE 'Inactive' END AS status
FROM furniture
ORDER BY id, time_create;

CREATE OR REPLACE VIEW consumables_history AS
SELECT id, time_create, time_dead, quantity, unit,
       CASE WHEN time_dead IS NULL THEN 'Active' ELSE 'Inactive' END AS status
FROM consumables
ORDER BY id, time_create;
