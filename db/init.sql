CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY,
    job VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY,
    department VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS hired_employees (
    id INTEGER PRIMARY KEY, 
    name VARCHAR(255) NOT NULL,
    datetime VARCHAR(255) NOT NULL,
    department_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);

