import os

import psycopg2 as pg


def setup_tables(cursor):
  # create table(s)
  cursor.execute("""
  CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
  );""")

  cursor.execute("""
  INSERT INTO comments (message) VALUES ('first blood!'), ('this is hello'), ('third comment');
  """)


def fancy_query(cursor):
  qry = """
  SELECT id, message
  FROM comments
  WHERE message LIKE %(prefix)s
  ORDER BY id DESC
  LIMIT %(limit)s
  """
  args = { "limit": 1, "prefix": "th%" }
  cursor.execute(qry, args)
  print(cursor.fetchall())

def main(db_url: str):
    conn = pg.connect(db_url)
    with conn.cursor() as cursor:
        setup_tables(cursor)
        fancy_query(cursor)
    conn.close()


if __name__ == '__main__':
    main(os.environ['DATABASE_URL'])
