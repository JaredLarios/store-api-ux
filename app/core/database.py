"""
database connection and handling data
"""

from typing import Optional

import psycopg2 as pg
import psycopg2.extras
from app.core import config


db = None


def start_connection(custom_uri: Optional[str] = None):
    """
    Starts the connection to the database
    """
    try:
        global db
        if custom_uri:
            db = pg.connect(custom_uri, cursor_factory=psycopg2.extras.RealDictCursor)
        else:
            db = pg.connect(
                config.DATABASE_URI, cursor_factory=psycopg2.extras.RealDictCursor
            )
        db.autocommit = True
    except Exception as exc:
        raise RuntimeError("database error") from exc


def get_database():
    """
    Get the database connection
    return:
        Database Connection with
    """
    if not db:
        raise RuntimeError("Database not initialized")
    return db
