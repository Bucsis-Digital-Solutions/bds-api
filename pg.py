import psycopg2 as pg
import os
from dotenv import load_dotenv

load_dotenv()

database=os.getenv("PG_NAME")
user=os.getenv("PG_USER")
host=os.getenv("PG_HOST")
password=os.getenv("PG_PASS")

def connect():
    return pg.connect(
        database=database,
        user=user,
        host=host,
        password=password,
    )

if __name__ == "__main__":
    print("Health Check")
    print(database, user, host, password)
    conn = connect()
    print (conn)
    cur = conn.cursor()
    print(cur)
    cur.execute("SELECT version();")
    print(cur.fetchone())
