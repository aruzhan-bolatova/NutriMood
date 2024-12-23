import pandas as pd
import mysql.connector
import json

# MySQL connection details
conn = mysql.connector.connect(
    user='root',  # Replace with your MySQL username
    password='Arya@1234',  # Replace with your MySQL password
    host='127.0.0.1:',  # Localhost (or the IP address of your MySQL server)
    database='moodbite1520_test'  # Replace with your database name
)