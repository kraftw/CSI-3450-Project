author_mapping = {
    'authorid': 'ID',
    'firstname': 'First Name',
    'lastname': 'Last Name',
}

book_mapping = {
    'bookid': 'ID',
    'title': 'Title',
    'isbn': 'ISBN',
    'publicationyear': 'Publication Year',
    'price': 'Price',
    'name': "Publisher",
    'categoryname': 'Category',
}

customer_mapping = {
    'customerid': 'ID',
    'firstname': 'First Name',
    'lastname': 'Last Name',
    'email': 'Email',
    'phone': 'Phone Number',
    'address': 'Address',
    'city': 'City',
    'state': 'State',
    'zipcode': 'Zipcode',
    'country': 'country',
}

orders_mapping = {
    'orderid': 'ID',
    'customername': 'Customer Name',
    'orderdate': 'Order Date',
    'totalamount': 'Order Total',
}

payment_mapping = {
    'paymentid': 'Payment ID',
    'orderid': 'Order ID',
    'paymentdate': 'Payment Date',
    'paymentmethod': 'Payment Method',
    'amount': 'Amount Paid',
}

publisher_mapping = {
    'publisherid': 'ID',
    'name': 'Publisher Name',
    'address': 'Address',
    'phone': 'Phone Number',
}