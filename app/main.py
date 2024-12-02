from querys import insert_jobs,insert_departments,insert_h_employees,query_number_employees
from flask import Flask, request, jsonify
from connection import conn

# Configuración de Flask
app = Flask(__name__)

# Configuración de la conexión a la base de datos
connection = conn()

@app.route('/')
def root():
    return 'Home'

@app.post('/insert/jobs')
def insert_jobs_endpoint():
    # Obtener datos del cuerpo de la solicitud
    data = request.get_json()
    id = data["id"]
    job = data['job']
    if not data:
        return jsonify({"error": "No data provided"}), 400
    with connection:
        cursor = connection.cursor()
        cursor.execute(insert_jobs(),(id,job))
    return jsonify({"message": "Job added successfully"}), 201

@app.post('/insert/departments')
def insert_departments_endpoint():
    # Obtener datos del cuerpo de la solicitud
    data = request.get_json()
    id = data["id"]
    department = data['department']
    if not data:
        return jsonify({"error": "No data provided"}), 400
    with connection:
        cursor = connection.cursor()
        cursor.execute(insert_departments(),(id,department))
    return jsonify({"message": "Department added successfully"}), 201

@app.post('/insert/h_employees')
def insert_h_employees_endpoint():
    # Obtener datos del cuerpo de la solicitud
    data = request.get_json()
    id = data["id"]
    name = data['name']
    datetime = data['datetime']
    department_id  = data['department_id']
    job_id = data['job_id']
    if not data.get('id') or not data.get('name') or not data.get('datetime') or not data.get('department_id') or not data.get('job_id'):
        return jsonify({"error": "all fields are required"}), 400
    with connection:
        cursor = connection.cursor()
        cursor.execute(insert_h_employees(),(id,name,datetime,department_id,job_id))
    return jsonify({"message": "hired_employee added successfully"}), 201

@app.post('/query')
def get_data_end_point():
    data = request.get_json()
    department = data['department']
    job = data['job']
    if not data:
        return jsonify({'error':'data input empty'})
    with connection:
        cursor = connection.cursor()
        cursor.execute(query_number_employees(department,job))
        resultados = cursor.fetchall()
        response = {
                    "data":resultados
                    }
    return jsonify(response),200

if __name__ == "__main__":  
    app.run(debug=True)
