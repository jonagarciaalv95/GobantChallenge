# querys.py

#JOBS
def insert_jobs():
    return """
    INSERT INTO jobs (id, job) VALUES (%s, %s);
    """

# DEPARTMENTS
def insert_departments():
    return """
    INSERT INTO departments (id, department) VALUES (%s, %s);
    """

#HIRED EMPLOYEES
def insert_h_employees():
    return """
    INSERT INTO hired_employees (id, name, datetime, department_id, job_id) VALUES (%s,%s,%s,%s,%s);"""

def query_number_employees(department,job):
    return f"""
    SELECT d.department,
    j.job,
    EXTRACT(QUARTER FROM TO_TIMESTAMP(he.datetime, 'YYYY-MM-DD HH24:MI:SS')) AS quarter, 
    count(distinct(he.id)) as number_employees
    FROM hired_employees as he
    INNER JOIN departments as d ON (he.department_id = d.id)
    INNER JOIN jobs as j ON (he.job_id = j.id)
    WHERE d.department = '{department}' AND 
    EXTRACT(YEAR FROM TO_TIMESTAMP(he.datetime, 'YYYY-MM-DD HH24:MI:SS')) = 2021 AND j.job= '{job}'
    GROUP BY d.department,j.job,EXTRACT(QUARTER FROM TO_TIMESTAMP(he.datetime, 'YYYY-MM-DD HH24:MI:SS'));"""
