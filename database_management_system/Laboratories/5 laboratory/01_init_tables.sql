-- Удаление существующих таблиц --
DROP TABLE IF EXISTS books CASCADE;
DROP TABLE IF EXISTS readers CASCADE;
DROP TABLE IF EXISTS libraries CASCADE;
DROP TABLE IF EXISTS employees CASCADE;
DROP TABLE IF EXISTS book_issue CASCADE;
DROP TABLE IF EXISTS auth_employees CASCADE;


CREATE TABLE books (
    book_id INT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255),
    isbn VARCHAR(20),
    publication_date DATE,
    status VARCHAR(50)
);

CREATE TABLE readers (
    reader_id INT PRIMARY KEY,
    surname VARCHAR(100),
    name VARCHAR(100),
    patronymic VARCHAR(100),
    contact_info TEXT,
    registration_date DATE
);

CREATE TABLE libraries (
    library_id INT PRIMARY KEY,
    name VARCHAR(200),
    address VARCHAR(300),
    phone VARCHAR(20)
);

CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    surname VARCHAR(100),
    name VARCHAR(100),
    patronymic VARCHAR(100),
    position VARCHAR(100),
    library_id INT,
    FOREIGN KEY (library_id) REFERENCES libraries(library_id)
);

CREATE TABLE book_issue (
    issue_id INT PRIMARY KEY,
    reader_id INT,
    employee_id INT,
    library_id INT,
    book_id INT,
    issue_date DATE,
    return_date DATE,
    status VARCHAR(50),
    FOREIGN KEY (reader_id) REFERENCES readers(reader_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (library_id) REFERENCES libraries(library_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);


CREATE TABLE auth_employees (
    employee_id INT PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

