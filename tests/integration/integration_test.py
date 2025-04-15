import pytest
import os

from app.main import app
from hamcrest import assert_that, equal_to, has_entries, has_item

TEST_DB = "db/integration_test.db"

os.makedirs("db", exist_ok=True)

@pytest.fixture
def client():

