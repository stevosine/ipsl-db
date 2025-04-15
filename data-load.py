import psycopg2
from faker import Faker
import random
from tqdm import tqdm

fake = Faker()

# Connect to the PostgreSQL running in Kubernetes
conn = psycopg2.connect(
    dbname="ipsldb",
    user="ipsladm",
    password="ipsl2025",
    host="localhost",
    port=5432
)
cur = conn.cursor()

# Drop and recreate the tables
cur.execute("""
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product TEXT NOT NULL,
    amount NUMERIC(10,2),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
""")
conn.commit()

# Insert 10,000 customers
customer_ids = []
print("Inserting customers...")
for _ in tqdm(range(100000)):
    name = fake.name()
    email = fake.unique.email()
    cur.execute(
        "INSERT INTO customers (name, email) VALUES (%s, %s) RETURNING id",
        (name, email)
    )
    customer_ids.append(cur.fetchone()[0])
conn.commit()

# Insert 100,000 orders
print("Inserting orders...")
for _ in tqdm(range(100000)):
    customer_id = random.choice(customer_ids)
    product = fake.word()
    amount = round(random.uniform(10.0, 10000.0), 2)
    order_date = fake.date_time_between(start_date='-1y', end_date='now')
    cur.execute("""
        INSERT INTO orders (customer_id, product, amount, order_date)
        VALUES (%s, %s, %s, %s)
    """, (customer_id, product, amount, order_date))

conn.commit()
cur.close()
conn.close()

print("Done populating database!")
