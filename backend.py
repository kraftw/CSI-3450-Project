import psycopg2

hostname = 'localhost'
database = 'project'
username = 'postgres'
password = 'aol4ever'
port     = '5432'

connection = psycopg2.connect(
    host = hostname,
    database = database,
    user = username,
    password = password,
    port = port,
)

cursor = connection.cursor()

print("connected")