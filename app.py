import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, render_template

app = Flask(__name__)

load_dotenv("D:\Coding\Github\CSI-3450-Project\ini.env")

def get_db_connection():
    connection = psycopg2.connect(
        dbname   = os.getenv("DB_NAME"),
        user     = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        host     = os.getenv("DB_HOST"),
        port     = os.getenv("DB_PORT"),    
    )
    return connection

@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM your_table;")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', data = data)

if __name__ == '__main__':
    app.run(debug = True)