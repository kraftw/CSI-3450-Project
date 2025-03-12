import os
import psycopg2
from mappings import *
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.urandom(24)

load_dotenv("D:\Coding\Github\CSI-3450-Project\ini.env")

PASSWORD = os.getenv("ADMIN_PASSWORD")

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
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        entered_password = request.form['password']
        if entered_password == PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('privatedata'))
        else:
            return render_template('login.html', error="Incorrect Password!")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))

@app.route('/bookauthor')
def bookauthor():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        SELECT b.bookid, b.title, b.isbn, b.publicationyear, CONCAT('$', b.price) AS price, p.name, c.categoryname
        FROM book b
        JOIN publisher p ON b.publisherid = p.publisherid
        JOIN category c ON b.categoryid = c.categoryid
        ORDER BY b.bookid ASC;
    """)
    books = cursor.fetchall()
    book_columns = [desc[0] for desc in cursor.description]
    
    cursor.execute("""
        SELECT * FROM author;
    """)
    authors = cursor.fetchall()
    author_columns = [desc[0] for desc in cursor.description]
    
    cursor.execute("""
        SELECT b.title AS title, CONCAT(a.firstname, ' ', a.lastname) AS authorname
        FROM bookauthor ba
        JOIN book b ON ba.bookid = b.bookid
        JOIN author a ON ba.authorid = a.authorid
        ORDER BY b.title ASC, a.lastname ASC;
    """)
    bookauthors = cursor.fetchall()
    bookauthor_columns = ["Book Title", "Author Name"]
    
    cursor.close()
    connection.close()
    
    mapped_book_columns = [book_mapping.get(col, col) for col in book_columns]
    mapped_author_columns = [author_mapping.get(col, col) for col in author_columns]
    
    return render_template('bookauthor.html',
                           books = books, book_columns = mapped_book_columns,
                           authors = authors, author_columns = mapped_author_columns,
                           bookauthors = bookauthors, bookauthor_columns = bookauthor_columns)

@app.route('/privatedata')
def privatedata():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        SELECT * FROM customer
        ORDER BY customerid ASC;
    """)
    customers = cursor.fetchall()
    customer_columns = [desc[0] for desc in cursor.description]
    
    cursor.execute("""
        SELECT o.orderid, CONCAT(c.firstname, ' ', c.lastname) AS customername, o.orderdate, CONCAT('$', o.totalamount) AS totalamount
        FROM orders o
        JOIN customer c ON o.customerid = c.customerid
        ORDER BY o.orderid ASC;           
    """)
    orders = cursor.fetchall()
    orders_columns = [desc[0] for desc in cursor.description]
    
    cursor.execute("""
        SELECT paymentid, orderid, paymentdate, paymentmethod, CONCAT('$', amount) AS amount FROM payment
        ORDER BY paymentid ASC;
    """)
    payments = cursor.fetchall()
    payment_columns = [desc[0] for desc in cursor.description]
    
    cursor.execute("""
        SELECT od.orderid, STRING_AGG(CONCAT(od.quantity, 'x ', b.title, ' (', CONCAT('$', od.subtotal), ')'), ', ') AS orderitems
        FROM orderdetail od
        JOIN book b ON od.bookid = b.bookid
        GROUP BY od.orderid
        ORDER BY od.orderid ASC;
    """)
    orderdetails = cursor.fetchall()
    orderdetail_columns = ["Order ID", "Order Items"]
    
    cursor.close()
    connection.close()
    
    mapped_customer_columns = [customer_mapping.get(col, col) for col in customer_columns]
    mapped_orders_columns = [orders_mapping.get(col, col) for col in orders_columns]
    mapped_payment_columns = [payment_mapping.get(col, col) for col in payment_columns]
    
    return render_template('privatedata.html',
                           customers = customers, customer_columns = mapped_customer_columns,
                           orders = orders, orders_columns = mapped_orders_columns,
                           payments = payments, payment_columns = mapped_payment_columns,
                           orderdetails = orderdetails, orderdetail_columns = orderdetail_columns)

@app.route('/publisher')
def publisher():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        SELECT * FROM publisher
        ORDER BY publisherid ASC;
    """)
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    
    cursor.close()
    connection.close()
    
    mapped_columns = [publisher_mapping.get(col, col) for col in columns]
   
    return render_template('publisher.html', data = data, columns = mapped_columns)

if __name__ == '__main__':
    app.run(debug = True)