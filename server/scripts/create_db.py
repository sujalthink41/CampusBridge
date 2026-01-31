import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy.engine.url import make_url

from campus_bridge.config.settings.app import app_settings


def create_database():
    """Create the database if it doesn't exist"""
    db_url = make_url(app_settings.DATABASE_URL)
    db_name = db_url.database

    # Connect to 'postgres' database to create the new database
    # We construct a URL pointing to the default 'postgres' db
    postgres_url = db_url.set(database="postgres")

    if postgres_url.drivername.startswith("postgresql+asyncpg"):
        postgres_url = postgres_url.set(drivername="postgresql+psycopg2")

    print(f"Connecting to database server...")
    try:
        # Extract connection args
        conn = psycopg2.connect(
            dbname="postgres",
            user=postgres_url.username,
            password=postgres_url.password,
            host=postgres_url.host,
            port=postgres_url.port,
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute(
            f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'"
        )
        exists = cursor.fetchone()

        if not exists:
            print(f"Creating database '{db_name}'...")
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"Database '{db_name}' created successfully!")
        else:
            print(f"Database '{db_name}' already exists.")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error creating database: {e}")
        # If we can't connect to postgres, maybe we can't create it automatically
        # but we should let the user know.


if __name__ == "__main__":
    create_database()
