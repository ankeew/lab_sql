-- Таблица сотрудников для lab_01, lab_02 и lab_03
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    job_id VARCHAR(20),
    salary NUMERIC(10,2),
    department_id INTEGER
);

-- Таблица департаментов для lab_01, lab_02 и lab_03
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    street VARCHAR(100),
    postal_code VARCHAR(20)
);

-- Таблица работников для lab_04
CREATE TABLE workers (
    ln VARCHAR(100),
    fn VARCHAR(100),
    sn VARCHAR(100),
    work_description TEXT
);

-- Таблица операций для lab_05
CREATE TABLE operations (
    id SERIAL PRIMARY KEY,
    account_number VARCHAR(20) NOT NULL,
    operation_name VARCHAR(100) NOT NULL,
    operation_sum DECIMAL(10, 2) NOT NULL
);

-- Таблица журнал операций для lab_05
CREATE TABLE operations_log (
    operation_id INTEGER NOT NULL REFERENCES operations(id) ON DELETE CASCADE,
    account_number VARCHAR(20) NOT NULL,
    operation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    operation_type CHAR(1) NOT NULL CHECK (operation_type IN ('-', '+'))
);