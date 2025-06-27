import psycopg2
from fastapi import Depends
from app.core.settings import Settings
from contextlib import contextmanager

def get_db_conn():
    conn = psycopg2.connect(
        dbname="product_db",
        user="moretti-product", 
        password="moretti",
        host="localhost",
        port="5432"
    )

    try:
        yield conn
    finally:
        conn.close()

@contextmanager
def get_db_connection():
    conn = psycopg2.connect(
        dbname="product_db",
        user="moretti-product", 
        password="moretti",
        host="localhost",
        port="5432"
    )

    try:
        yield conn
    finally:
        conn.close()
