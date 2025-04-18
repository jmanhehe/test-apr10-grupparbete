import pytest
import psycopg2

from db import get_db_connection, init_db, add_visit, get_visit_by_id
from datetime import datetime, timezone

TEST_IP = "127.0.0.1"
USER_AGENT = "TestUserAgent"

@pytest.fixture(scope="module")
def db_setup():
    # Initialize DB
    init_db()
    yield

    # Clean up
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS visits")
    conn.commit()
    cur.close()
    conn.close()

def test_db_connection():
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        assert result[0] == 1, "Failed to execute simple query"
    finally:
        cur.close()
        conn.close()

def test_init_db(db_setup):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'visits'
        """)
        columns = [(row[0], row[1]) for row in cur.fetchall()]
        expected_colums = [
            ('id', 'integer'),
            ('timestamp', 'timestamp without time zone'),
            ('ip', 'text'),
            ('user_agent', 'text')
        ]
        assert sorted(columns) == sorted(expected_colums), "Table structure is incorrect"
    finally:
        cur.close()
        conn.close()

def test_add_and_get_visit(db_setup):
    ip = "127.0.0.1"
    user_agent = "TestUserAgent"
    visit_data = add_visit(ip, user_agent)

    # Verify data from visit_data
    assert visit_data["id"] is not None, "Visit ID is none"
    assert visit_data["ip"] == ip, "IP doesnt match"
    assert visit_data["user_agent"] == user_agent, "User Agent doesnt match"

    # This timestamp check needs to be looked at
    # assert isinstance(visit_data["timestamp"], datetime), "Timestamp is not a datetime"

    # Check the visit using ID
    specific_visit = get_visit_by_id(visit_data["id"])
    assert specific_visit is not None, "Visit not found using the ID"
    assert specific_visit["id"] == visit_data["id"], "Visit ID doesnt match against specific ID"
    assert specific_visit["ip"] == ip, "IP doesnt match"
    assert specific_visit["user_agent"] == user_agent, "Specific user agent doesnt match"
    
    # Same as above, timestamp needs to be checked at
    # assert specific_visit["timestamp"] == visit_data["timestamp"], "Timestamp does not match"