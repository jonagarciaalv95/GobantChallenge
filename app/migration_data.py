import psycopg2
from dotenv import load_dotenv
import pandas as pd
import logging
import os

# Load environment variables from .env file
load_dotenv()

# Configuración de la conexión a la base de datos
user = os.getenv('USER')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')

DB_CONFIG = {
    "dbname": database,  
    "user": user,
    "password": password,
    "host": "postgres-db",  
    "port": "5432",       # port inside docker
}

# Configuración de logging
logging.basicConfig(filename='data_migration_errors.log', level=logging.ERROR,
                    format='%(asctime)s - %(message)s')

# Funciones

# Cargar archivo CSV
def read_csv(path_file, file, col_name):
    df = pd.read_csv(os.path.join(path_file, file), sep=',', encoding='utf-8', header=None, names=col_name)
    return df

def get_files(path_files):
    files = os.listdir(path_files)
    return files

def validate_and_cast_data(df, table_name):
    try:
        if table_name == 'departments':
            df['id'] = pd.to_numeric(df['id'], errors='coerce', downcast='integer')
            df['department'] = df['department'].astype(str)
        
        elif table_name == 'jobs':
            df['id'] = pd.to_numeric(df['id'], errors='coerce', downcast='integer')
            df['job'] = df['job'].astype(str)
        
        elif table_name == 'hired_employees':
            df['id'] = pd.to_numeric(df['id'], errors='coerce', downcast='integer')
            df['name'] = df['name'].astype(str)
            df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
            df['department_id'] = pd.to_numeric(df['department_id'], errors='coerce', downcast='integer')
            df['job_id'] = pd.to_numeric(df['job_id'], errors='coerce', downcast='integer')
        
        df = df.dropna()  # Remove rows with NaN values

        return df
    except Exception as e:
        logging.error(f"Error al validar datos de {table_name}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

# Cargar datos de los archivos CSV
def load_csv_to_db(file_path, file, col_name):
    try:
        # Read CSV file
        df = read_csv(file_path, file, col_name)
        df = validate_and_cast_data(df, file[:-4])  # file[:-4] removes the .csv extension

        if not df.empty:
            # Insert the validated data into the database
            insert_data_to_db(file[:-4], df)
            print(f"Datos de {file[:-4]} cargados exitosamente.")
        else:
            print(f"Todos los datos de {file[:-4]} fueron inválidos.")

    except Exception as e:
        logging.error(f"Error al cargar datos en {file[:-4]}: {e}")

# Function to insert data into the database using psycopg2
def insert_data_to_db(table_name, df):
    try:
        # Establishing the connection with the database
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                print("Conexión exitosa.")

                # Building the insert query
                for _, row in df.iterrows():
                    columns = ', '.join(df.columns)
                    values = ', '.join([f"'{str(value)}'" for value in row])
                    query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
                    
                    cur.execute(query)

                # Commit the transaction
                conn.commit()

    except Exception as e:
        logging.error(f"Error al insertar datos en la tabla {table_name}: {e}")
        if conn:
            conn.rollback()

# Main process
files_path = './app/data'
col_name = {
    'departments': ("id", 'department'),
    'jobs': ("id", 'job'),
    'hired_employees': ("id", 'name', 'datetime', 'department_id', 'job_id')
}

# Get the list of files
files = get_files(files_path)
print(files)

# Loop over each file and load it into the DB
for file in files:
    if file.endswith('.csv'):  # Ensure we're processing only CSV files
        load_csv_to_db(files_path, file, col_name.get(file[:-4]))
        print(f'Load data {file[:-4]} successfully.')
