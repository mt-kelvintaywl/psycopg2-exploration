import os

import psycopg2 as pg


def main(db_url: str):
    conn = pg.connect(db_url)
    with conn.cursor() as curr:
        curr.execute(open("schema.sql", "r").read())

    conn.close()


if __name__ == '__main__':
    main(os.environ['DATABASE_URL'])
