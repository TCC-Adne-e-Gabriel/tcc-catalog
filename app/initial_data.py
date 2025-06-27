from app.core.db import get_db_connection
def create_tables(): 
    queries = (
        """ 
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

        CREATE TABLE categories (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            name VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )

        CREATE TABLE products (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            name VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL,
            price NUMERIC(10, 2) NOT NULL,
            available BOOLEAN NOT NULL DEFAULT TRUE,
            sku VARCHAR(255) NOT NULL UNIQUE,
            discount NUMERIC(10, 2) DEFAULT 0,
            quantity INTEGER NOT NULL,
            image BYTEA,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )

        CREATE TABLE product_categories (
            product_id UUID NOT NULL,
            categoria_id UUID NOT NULL,
            PRIMARY KEY (product_id, categoria_id),
            FOREIGN KEY (product_id) 
                REFERENCES products(id) 
                ON UPDATE CASCADE,
                ON DELETE CASCADE,
            FOREIGN KEY (categoria_id) 
                REFERENCES categories(id) 
                ON UPDATE CASCADE
                ON DELETE CASCADE
        );
        """
    )
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            for command in queries:
                cur.execute(command)
            conn.commit()

def initialize_db(): 
    create_tables()
