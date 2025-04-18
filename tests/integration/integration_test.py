import pytest
import psycopg2

from db import get_db_connection, init_db, add_visit, get_visit_by_id, get_all_visits
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

@pytest.fixture(scope="function")
def clean_db(db_setup):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("TRUNCATE visits RESTART IDENTITY")
    conn.commit()
    cur.close()
    conn.close()
    yield

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

# def test_add_visit_isolated(db_setup):
#     # test add visit separate first
#     visit_data = add_visit(TEST_IP, USER_AGENT)

def test_add_and_get_visit(clean_db):
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


# This test adds visits and fetches them to check that they match
def test_get_all_visits(clean_db):
    test_visits = [
        {
            "ip": "127.0.0.1",
            "user_agent": "firefox browser 1"
        },
        {
            "ip": "127.0.0.2",
            "user_agent": "firefox browser 2"
        },
        {
            "ip": "127.0.0.3", 
            "user_agent": "firefox browser 3"
        }
    ]

    added_visits = []
    for visit in test_visits:
        visit_data = add_visit(visit["ip"], visit["user_agent"])
        added_visits.append(visit_data)

    all_visits = get_all_visits()

    assert len(all_visits) == len(test_visits), f"Expected {len(test_visits)} visits, got {len(all_visits)}"

    for added_visit in added_visits:
        matching_visits = [
            v for v in all_visits
            if v["id"] == added_visit["id"]
            and v["ip"] == added_visit["ip"]
            and v["user_agent"] == added_visit["user_agent"]
        ]
        assert len(matching_visits) == 1, f"Visit with id {added_visit['id']} not found or duplicated"

    visit_ids = [visit["id"] for visit in all_visits]
    assert visit_ids == sorted(visit_ids), "Visits are not ordered by IDs"
            