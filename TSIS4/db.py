import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "snake_game",
    "user": "postgres",
    "password": "1234",
}


def get_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.set_client_encoding("UTF8")
    return conn


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS game_sessions (
                    id SERIAL PRIMARY KEY,
                    player_id INTEGER REFERENCES players(id),
                    score INTEGER NOT NULL,
                    level_reached INTEGER NOT NULL,
                    played_at TIMESTAMP DEFAULT NOW()
                )
            """)

        conn.commit()


def get_or_create_player(username):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id FROM players WHERE username = %s",
                (username,)
            )

            row = cur.fetchone()

            if row:
                return row[0]

            cur.execute(
                "INSERT INTO players(username) VALUES (%s) RETURNING id",
                (username,)
            )

            player_id = cur.fetchone()[0]

        conn.commit()

    return player_id


def save_session(player_id, score, level_reached):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO game_sessions(player_id, score, level_reached)
                VALUES (%s, %s, %s)
            """, (player_id, score, level_reached))

        conn.commit()


def get_top10():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    p.username,
                    gs.score,
                    gs.level_reached,
                    TO_CHAR(gs.played_at, 'YYYY-MM-DD') AS date
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                ORDER BY gs.score DESC
                LIMIT 10
            """)

            return cur.fetchall()


def get_personal_best(player_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT COALESCE(MAX(score), 0)
                FROM game_sessions
                WHERE player_id = %s
            """, (player_id,))

            return cur.fetchone()[0]