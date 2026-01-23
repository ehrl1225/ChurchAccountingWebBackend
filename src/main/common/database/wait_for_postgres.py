import os
import time
import psycopg

from common.env import settings

print("Waiting for postgres...")

while True:
    try:
        conn = psycopg.connect(
            host=settings.profile_config.DB_HOST,
            port=settings.profile_config.DB_PORT,
            user=settings.profile_config.DB_USER,
            password=settings.profile_config.DB_PASSWORD,
            dbname=settings.profile_config.DB_NAME,
        )
        conn.close()
        print("Postgresql is ready")
        break
    except psycopg.OperationalError:
        print("Postgresql is not ready... Waiting...")
        time.sleep(1)