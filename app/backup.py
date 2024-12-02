import fastavro
from fastavro import writer
from connection import conn

connection = conn()

# Definición de esquema según la tabla
def selection_table_schema(table):
    if table == 'jobs':
        schema = {
            "type": "record",
            "name": "jobs",
            "fields": [{"name": "id", "type": "int"},
                       {"name": "job", "type": "string"}]
        }
    elif table == 'departments':
        schema = {
            "type": "record",
            "name": "departments",
            "fields": [{"name": "id", "type": "int"},
                       {"name": "department", "type": "string"}]
        }
    else:  # hired_employees (tabla por defecto)
        schema = {
            "type": "record",
            "name": "hired_employees",
            "fields": [
                {"name": "id", "type": "int"},
                {"name": "name", "type": "string"},
                {"name": "datetime", "type": "string"},
                {"name": "department_id", "type": "int"},
                {"name": "job_id", "type": "int"}
            ]
        }
    return schema

# Función para crear un backup en formato AVRO
def backup_table_to_avro(table):
    with connection:
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM {table};')
        rows = cursor.fetchall()
    
    # Obtener el esquema de AVRO basado en la tabla
    schema = selection_table_schema(table)

    # Guardar las filas en un archivo AVRO
    with open(f'{table}_backup.avro', 'wb') as out_file:
        writer(out_file, schema, rows)

# Función para restaurar desde un archivo AVRO
def restore_table_from_avro(table):
    with open(f'{table}_backup.avro', 'rb') as in_file:
        reader = fastavro.reader(in_file)
        cursor = connection.cursor()
        
        # Ajustar el insert según la tabla para corresponder con las columnas
        if table == 'jobs':
            insert_query = '''INSERT INTO jobs (id, job) VALUES (?, ?)'''
        elif table == 'departments':
            insert_query = '''INSERT INTO departments (id, department) VALUES (?, ?)'''
        elif table == 'hired_employees':
            insert_query = '''INSERT INTO hired_employees (id, name, datetime, department_id, job_id) VALUES (?, ?, ?, ?, ?)'''
        
        # Insertar cada registro desde el archivo AVRO en la tabla correspondiente
        for record in reader:
            cursor.execute(insert_query, tuple(record.values()))  # Se asegura que los valores se inserten correctamente según el esquema
        
        connection.commit()

# Ejemplo de cómo hacer un backup y restauración
backup_table_to_avro('jobs')
#restore_table_from_avro('jobs')
