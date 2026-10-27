
import os

import pymysql
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "careerfit_ai"),
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5,
    )


if __name__ == "__main__":
    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT DATABASE() AS database_name")
            result = cursor.fetchone()
            print("Database connection successful:", result)

        connection.close()

    except pymysql.MySQLError as error:
        print("Database connection failed:", error)
