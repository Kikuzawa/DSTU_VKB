-- 1. Функция для восстановления объекта на определенную дату (исправленная)
CREATE OR REPLACE FUNCTION restore_object_version(
    target_table TEXT,
    object_id INT,
    version_time TIMESTAMP
) RETURNS TEXT AS $$
DECLARE
    result TEXT;
    col_record RECORD;
    col_list TEXT := '';
    value_list TEXT := '';
    query_text TEXT;
BEGIN
    -- Собираем список столбцов и значений для вставки
    FOR col_record IN 
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = target_table 
        AND column_name NOT IN ('id', 'time_create', 'time_dead')
    LOOP
        IF col_list <> '' THEN
            col_list := col_list || ', ';
            value_list := value_list || ', ';
        END IF;
        
        col_list := col_list || col_record.column_name;
        value_list := value_list || format('(SELECT %I FROM %I WHERE id = %s AND time_create <= %L ORDER BY time_create DESC LIMIT 1)',
                                        col_record.column_name, 
                                        target_table, 
                                        object_id, 
                                        version_time);
    END LOOP;
    
    -- Формируем и выполняем запрос на вставку
    query_text := format('
        INSERT INTO %I (id, time_create, time_dead, %s)
        SELECT %s, now(), NULL, %s
        WHERE EXISTS (
            SELECT 1 FROM %I 
            WHERE id = %s AND time_create <= %L
        )',
        target_table, col_list, object_id, value_list, target_table, object_id, version_time);
    
    EXECUTE query_text;
    
    -- Обновляем время смерти предыдущей активной версии
    EXECUTE format('
        UPDATE %I 
        SET time_dead = now() 
        WHERE id = %s AND time_dead IS NULL AND time_create < now()',
        target_table, object_id);
    
    result := format('Object %s from table %I restored to version at %s', 
                    object_id, target_table, version_time);
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- 2. Функция для сравнения двух версий объекта (исправленная)
CREATE OR REPLACE FUNCTION compare_object_versions(
    target_table TEXT,
    object_id INT,
    version1 TIMESTAMP,
    version2 TIMESTAMP
) RETURNS TABLE (
    column_name TEXT,
    value1 TEXT,
    value2 TEXT,
    changed BOOLEAN
) AS $$
DECLARE
    query_text TEXT;
BEGIN
    query_text := format('
        WITH 
        v1 AS (
            SELECT * FROM %I 
            WHERE id = %s AND time_create <= %L 
            ORDER BY time_create DESC LIMIT 1
        ),
        v2 AS (
            SELECT * FROM %I 
            WHERE id = %s AND time_create <= %L 
            ORDER BY time_create DESC LIMIT 1
        )
        SELECT 
            c.column_name::TEXT,
            COALESCE(
                (SELECT jsonb_path_query_first(
                    to_jsonb(v1), 
                    format(''$.%%s'', c.column_name)::jsonpath
                )::TEXT FROM v1), 
                ''N/A'') AS value1,
            COALESCE(
                (SELECT jsonb_path_query_first(
                    to_jsonb(v2), 
                    format(''$.%%s'', c.column_name)::jsonpath
                )::TEXT FROM v2), 
                ''N/A'') AS value2,
            EXISTS (
                SELECT 1 FROM v1, v2
                WHERE to_jsonb(v1)->>c.column_name IS DISTINCT FROM 
                      to_jsonb(v2)->>c.column_name
            ) AS changed
        FROM information_schema.columns c
        WHERE c.table_name = %L
        AND c.column_name NOT IN (''time_create'', ''time_dead'')
        ORDER BY c.ordinal_position',
        target_table, object_id, version1,
        target_table, object_id, version2,
        target_table);
    
    RETURN QUERY EXECUTE query_text;
END;
$$ LANGUAGE plpgsql;