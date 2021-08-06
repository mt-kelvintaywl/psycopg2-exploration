import datetime
import os

import psycopg2 as pg
import pytest


@pytest.fixture(scope="module")
def cursor():
    db_url = os.environ.get("DATABASE_URL")
    conn = pg.connect(db_url)
    with conn.cursor() as cursor:
        yield cursor
    conn.close()


@pytest.fixture(scope="module", autouse=True)
def setup_tables(cursor):
    qry = """
    CREATE TABLE comments (
        id SERIAL PRIMARY KEY,
        message TEXT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );

    INSERT INTO comments (message) VALUES ('first blood!'), ('this is hello'), ('third comment');
    """
    cursor.execute(qry)

# NOTE: all tests focus on using dicts (i.e., named arguments) for query arguments

def test_count(cursor):
    cursor.execute("SELECT COUNT(*) FROM comments")
    row = cursor.fetchone()
    assert row[0] == 3


def test_limit_in_arg(cursor):
    qry = """
    SELECT id, message
    FROM comments
    ORDER BY id DESC
    LIMIT %(limit)s
    """
    cursor.execute(qry, { "limit": 2 })
    rows = cursor.fetchall()
    assert len(rows) == 2
    ids = [id for (id, _msg) in rows]
    assert ids == [3, 2]


def test_multiple_args(cursor):
    qry = """
    SELECT id, message
    FROM comments
    WHERE message LIKE %(prefix)s AND created_at >= %(created_after)s
    ORDER BY id DESC
    LIMIT %(limit)s
    """
    args = {"prefix": "th%", "created_after": datetime.date(2021, 1, 1), "limit": 1}
    cursor.execute(qry, args)
    rows = cursor.fetchall()
    assert len(rows) == 1
    id, message = rows[0]
    assert id == 3 
    assert message == "third comment"


def test_like_clause_with_percentage_harcoded(cursor):
    qry = """
    WITH sampled AS (
      SELECT *
      FROM comments
      ORDER BY id DESC
      LIMIT %(size)s
    )
    SELECT id, message
    FROM sampled
    WHERE message LIKE 'th%%'
    """
    args = {"size": 3}
    cursor.execute(qry, args)
    rows = cursor.fetchall()
    assert len(rows) == 2
