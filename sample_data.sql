INSERT INTO departments (id, name, street, postal_code) VALUES
(1, 'IT', 'Lenina St, 10', '123456'),
(2, 'HR', 'Pushkina St, 25', '654321');

INSERT INTO employees (first_name, last_name, email, job_id, salary, department_id) VALUES
('John', 'Smith', 'john.smith@company.com', 'IT_PROG', 95000, 1),
('Alice', 'Johnson', 'alice.j@company.com', 'HR_REP', 70000, 2),
('Bob', 'McDonald', 'bob.mcd@company.com', 'IT_PROG', 100000, 1),
('Eve', 'SMITH', 'eve@company.com', 'HR_REP', 68000, 2);

INSERT INTO workers (ln, fn, sn, work_description) VALUES
('Ivanov', 'Ivan', 'Ivanovich', 'Worked with Python, SQL, and Docker on data pipelines.'),
('Petrov', 'Petr', 'Petrovich', 'Used JavaScript, React, Node.js for web apps.'),
('Sidorov', 'Alex', 'Sergeevich', 'Experienced in C++, Linux, and PostgreSQL.');