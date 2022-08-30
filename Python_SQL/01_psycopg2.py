import psycopg2
from psycopg2.extras import RealDictCursor, execute_values

conn = psycopg2.connect(dbname='testdb', user='postgres', password='1')

cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS superheroes;")
cur.execute("DROP TABLE IF EXISTS traffic_light;")

conn.commit()

cur.execute("CREATE TABLE superheroes (hero_id serial PRIMARY KEY, hero_name varchar, strength int);")

cur.execute("INSERT INTO superheroes (hero_name, strength) VALUES (%s, %s);", ("Superman", 100))
cur.execute("INSERT INTO superheroes (hero_name, strength) VALUES (%s, %s);", ("Flash", 999))
cur.execute("""
            INSERT INTO superheroes (hero_name, strength) 
            VALUES (%(name)s, %(strength)s);
            """,
            {"name": "Green Arrow", "strength": 80})

conn.commit()

cur.execute("CREATE TABLE traffic_light (light_id serial PRIMARY KEY, light text);")

cur.execute("INSERT INTO traffic_light(light) VALUES (%s);", ("red",))

conn.commit()

cur.execute("SELECT * FROM superheroes")
one_line = cur.fetchone()
print(one_line)

full_fetch = cur.fetchall()
for rec in full_fetch:
    print(rec)

conn.commit()

cur.close()
conn.close()

# ! TEMPLATE HOW TO WORK
try:
    conn = psycopg2.connect(dbname='testdb', user='postgres', password='1')
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            execute_values(cur, "INSERT INTO traffic_light(light) VALUES %s;", [("green",), ("yellow",)])
            cur.execute("SELECT * FROM traffic_light")
            records = cur.fetchall()
            print(records)
            print(records[0]["light"])
finally:
    conn.close()


