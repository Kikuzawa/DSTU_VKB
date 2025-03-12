-- Функция добавления новой книги
CREATE OR REPLACE FUNCTION add_book(
    p_title VARCHAR,
    p_author VARCHAR,
    p_isbn VARCHAR,
    p_publication_date DATE,
    p_status VARCHAR
)
RETURNS INTEGER AS $$
DECLARE
    v_book_id INTEGER;
BEGIN
    INSERT INTO books (title, author, isbn, publication_date, status)
    VALUES (p_title, p_author, p_isbn, p_publication_date, p_status)
    RETURNING book_id INTO v_book_id;
    
    RETURN v_book_id;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Ошибка при добавлении книги: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Функция изменения информации о книге
CREATE OR REPLACE FUNCTION update_book(
    p_book_id INTEGER,
    p_title VARCHAR DEFAULT NULL,
    p_author VARCHAR DEFAULT NULL,
    p_isbn VARCHAR DEFAULT NULL,
    p_publication_date DATE DEFAULT NULL,
    p_status VARCHAR DEFAULT NULL
)
RETURNS BOOLEAN AS $$
BEGIN
    UPDATE books
    SET
        title = COALESCE(p_title, title),
        author = COALESCE(p_author, author),
        isbn = COALESCE(p_isbn, isbn),
        publication_date = COALESCE(p_publication_date, publication_date),
        status = COALESCE(p_status, status)
    WHERE book_id = p_book_id;
    
    RETURN TRUE;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Ошибка при обновлении книги: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Функция удаления книги
CREATE OR REPLACE FUNCTION delete_book(p_book_id INTEGER)
RETURNS BOOLEAN AS $$
BEGIN
    -- Сначала проверяем, нет ли активных выдач
    IF EXISTS (SELECT 1 FROM book_issue WHERE book_id = p_book_id AND status = 'выдана') THEN
        RAISE EXCEPTION 'Нельзя удалить книгу с активными выдачами';
    END IF;
    
    DELETE FROM books WHERE book_id = p_book_id;
    RETURN TRUE;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Ошибка при удалении книги: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Функция добавления нового читателя
CREATE OR REPLACE FUNCTION add_reader(
    p_surname VARCHAR,
    p_name VARCHAR,
    p_patronymic VARCHAR,
    p_contact_info TEXT,
    p_registration_date DATE
)
RETURNS INTEGER AS $$
DECLARE
    v_reader_id INTEGER;
BEGIN
    INSERT INTO readers (surname, name, patronymic, contact_info, registration_date)
    VALUES (p_surname, p_name, p_patronymic, p_contact_info, p_registration_date)
    RETURNING reader_id INTO v_reader_id;
    
    RETURN v_reader_id;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Ошибка при добавлении читателя: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Функция изменения информации о читателе
CREATE OR REPLACE FUNCTION update_reader(
    p_reader_id INTEGER,
    p_surname VARCHAR DEFAULT NULL,
    p_name VARCHAR DEFAULT NULL,
    p_patronymic VARCHAR DEFAULT NULL,
    p_contact_info TEXT DEFAULT NULL,
    p_registration_date DATE DEFAULT NULL
)
RETURNS BOOLEAN AS $$
BEGIN
    UPDATE readers
    SET
        surname = COALESCE(p_surname, surname),
        name = COALESCE(p_name, name),
        patronymic = COALESCE(p_patronymic, patronymic),
        contact_info = COALESCE(p_contact_info, contact_info),
        registration_date = COALESCE(p_registration_date, registration_date)
    WHERE reader_id = p_reader_id;
    
    RETURN TRUE;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Ошибка при обновлении данных читателя: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Функция удаления читателя
CREATE OR REPLACE FUNCTION delete_reader(p_reader_id INTEGER)
RETURNS BOOLEAN AS $$
BEGIN
    -- Проверяем, нет ли активных выдач
    IF EXISTS (SELECT 1 FROM book_issue WHERE reader_id = p_reader_id AND status = 'выдана') THEN
        RAISE EXCEPTION 'Нельзя удалить читателя с активными выдачами';
    END IF;
    
    DELETE FROM readers WHERE reader_id = p_reader_id;
    RETURN TRUE;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Ошибка при удалении читателя: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Функция добавления новой библиотеки
CREATE OR REPLACE FUNCTION add_library(
    p_name VARCHAR,
    p_address VARCHAR,
    p_phone VARCHAR
)
RETURNS INTEGER AS $$
DECLARE
    v_library_id INTEGER;
BEGIN
    INSERT INTO libraries (name, address, phone)
    VALUES (p_name, p_address, p_phone)
    RETURNING library_id INTO v_library_id;
    
    RETURN v_library_id;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Ошибка при добавлении библиотеки: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Функция изменения информации о библиотеке
CREATE OR REPLACE FUNCTION update_library(
    p_library_id INTEGER,
    p_name VARCHAR DEFAULT NULL,
    p_address VARCHAR DEFAULT NULL,
    p_phone VARCHAR DEFAULT NULL
)
RETURNS BOOLEAN AS $$
BEGIN
    UPDATE libraries
    SET
        name = COALESCE(p_name, name),
        address = COALESCE(p_address, address),
        phone = COALESCE(p_phone, phone)
    WHERE library_id = p_library_id;
    
    RETURN TRUE;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Ошибка при обновлении данных библиотеки: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Функция удаления библиотеки
CREATE OR REPLACE FUNCTION delete_library(p_library_id INTEGER)
RETURNS BOOLEAN AS $$
BEGIN
    -- Проверяем, нет ли привязанных сотрудников и выдач
    IF EXISTS (
        SELECT 1 FROM employees WHERE library_id = p_library_id
        UNION ALL
        SELECT 1 FROM book_issue WHERE library_id = p_library_id
    ) THEN
        RAISE EXCEPTION 'Нельзя удалить библиотеку с активными данными';
    END IF;
    
    DELETE FROM libraries WHERE library_id = p_library_id;
    RETURN TRUE;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Ошибка при удалении библиотеки: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Функция добавления нового сотрудника
CREATE OR REPLACE FUNCTION add_employee(
    p_surname VARCHAR,
    p_name VARCHAR,
    p_patronymic VARCHAR,
    p_position VARCHAR,
    p_library_id INTEGER
)
RETURNS INTEGER AS $$
DECLARE
    v_employee_id INTEGER;
BEGIN
    -- Проверяем существование библиотеки
    IF NOT EXISTS (SELECT 1 FROM libraries WHERE library_id = p_library_id) THEN
        RAISE EXCEPTION 'Библиотека с указанным ID не существует';
    END IF;
    
    INSERT INTO employees (surname, name, patronymic, position, library_id)
    VALUES (p_surname, p_name, p_patronymic, p_position, p_library_id)
    RETURNING employee_id INTO v_employee_id;
    
    RETURN v_employee_id;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Ошибка при добавлении сотрудника: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Функция изменения информации о сотруднике
CREATE OR REPLACE FUNCTION update_employee(
    p_employee_id INTEGER,
    p_surname VARCHAR DEFAULT NULL,
    p_name VARCHAR DEFAULT NULL,
    p_patronymic VARCHAR DEFAULT NULL,
    p_position VARCHAR DEFAULT NULL,
    p_library_id INTEGER DEFAULT NULL
)
RETURNS BOOLEAN AS $$
BEGIN
    -- Проверяем существование новой библиотеки, если она указана
    IF p_library_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM libraries WHERE library_id = p_library_id) THEN
        RAISE EXCEPTION 'Библиотека с указанным ID не существует';
    END IF;
    
    UPDATE employees
    SET
        surname = COALESCE(p_surname, surname),
        name = COALESCE(p_name, name),
        patronymic = COALESCE(p_patronymic, patronymic),
        position = COALESCE(p_position, position),
        library_id = COALESCE(p_library_id, library_id)
    WHERE employee_id = p_employee_id;
    
    RETURN TRUE;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Ошибка при обновлении данных сотрудника: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Функция удаления сотрудника
CREATE OR REPLACE FUNCTION delete_employee(p_employee_id INTEGER)
RETURNS BOOLEAN AS $$
BEGIN
    -- Проверяем, нет ли активных выдач
    IF EXISTS (SELECT 1 FROM book_issue WHERE employee_id = p_employee_id AND status = 'выдана') THEN
        RAISE EXCEPTION 'Нельзя удалить сотрудника с активными выдачами';
    END IF;
    
    DELETE FROM employees WHERE employee_id = p_employee_id;
    RETURN TRUE;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Ошибка при удалении сотрудника: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Функция выдачи книги
CREATE OR REPLACE FUNCTION issue_book(
    p_reader_id INTEGER,
    p_employee_id INTEGER,
    p_library_id INTEGER,
    p_book_id INTEGER,
    p_return_date DATE
)
RETURNS INTEGER AS $$
DECLARE
    v_issue_id INTEGER;
BEGIN
    -- Проверяем существование всех связанных записей
    IF NOT EXISTS (SELECT 1 FROM readers WHERE reader_id = p_reader_id) THEN
        RAISE EXCEPTION 'Читатель не найден';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM employees WHERE employee_id = p_employee_id) THEN
        RAISE EXCEPTION 'Сотрудник не найден';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM libraries WHERE library_id = p_library_id) THEN
        RAISE EXCEPTION 'Библиотека не найдена';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM books WHERE book_id = p_book_id) THEN
        RAISE EXCEPTION 'Книга не найдена';
    END IF;
    
    -- Проверяем статус книги
    IF (SELECT status FROM books WHERE book_id = p_book_id) != 'в наличии' THEN
        RAISE EXCEPTION 'Книга недоступна для выдачи';
    END IF;
    
    -- Проверяем, не превышает ли читатель лимит выдач
    IF EXISTS (
        SELECT 1 FROM book_issue 
        WHERE reader_id = p_reader_id 
        AND status = 'выдана'
        AND issue_date >= (CURRENT_DATE - INTERVAL '30 days')
        LIMIT 5
    ) THEN
        RAISE EXCEPTION 'Превышен лимит активных выдач';
    END IF;
    
    INSERT INTO book_issue (reader_id, employee_id, library_id, book_id, issue_date, return_date, status)
    VALUES (p_reader_id, p_employee_id, p_library_id, p_book_id, CURRENT_DATE, p_return_date, 'выдана')
    RETURNING issue_id INTO v_issue_id;
    
    -- Обновляем статус книги
    UPDATE books SET status = 'выдана' WHERE book_id = p_book_id;
    
    RETURN v_issue_id;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Ошибка при выдаче книги: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Функция возврата книги
CREATE OR REPLACE FUNCTION return_book(p_issue_id INTEGER)
RETURNS BOOLEAN AS $$
BEGIN
    -- Обновляем статус выдачи
    UPDATE book_issue 
    SET status = 'возвращена', return_date = CURRENT_DATE
    WHERE issue_id = p_issue_id;
    
    -- Обновляем статус книги
    UPDATE books 
    SET status = 'в наличии'
    WHERE book_id = (SELECT book_id FROM book_issue WHERE issue_id = p_issue_id);
    
    RETURN TRUE;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Ошибка при возврате книги: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;



