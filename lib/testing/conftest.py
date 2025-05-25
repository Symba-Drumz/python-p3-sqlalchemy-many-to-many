#!/usr/bin/env python3

import os
import pytest
from sqlalchemy import create_engine, text

package_dir = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[0:-1])
db_dir = os.path.join(package_dir, 'many_to_many.db')
SQLITE_URL = ''.join(['sqlite:///', db_dir])

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))

@pytest.fixture(autouse=True)
def clear_game_users():
    engine = create_engine(SQLITE_URL)
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM game_users"))
        conn.commit()
