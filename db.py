import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()


def get_conn():
    """PostgreSQL 연결을 생성합니다."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "hw01_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )


def fetch_all(query, params=None):
    """SELECT 결과 여러 행을 딕셔너리 형태로 반환합니다."""
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params or ())
            return cur.fetchall()


def fetch_one(query, params=None):
    """SELECT 결과 한 행을 딕셔너리 형태로 반환합니다."""
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params or ())
            return cur.fetchone()


def execute(query, params=None):
    """INSERT/UPDATE/DELETE 문을 실행합니다."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            conn.commit()
