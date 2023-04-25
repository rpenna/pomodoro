import sqlite3
from datetime import datetime


DATABASES = {
    'production': 'repository/pomodoro.db',
    'development': 'repository/dev.db',
    'test': 'repository/test.db',
}


DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

class PomodoroRepository:
    def __init__(self, db: str = 'production'):
        self.__db_name = db
        self.__db = DATABASES.get(db, DATABASES.get('test'))
        self.__conn = sqlite3.connect(self.__db)
        self.__setup()

    def __setup(self):
        with self.__conn:
            self.__conn.execute(
                """
                    CREATE TABLE IF NOT EXISTS pomodoro (
                        pomodoro_id INTEGER NOT NULL,
                        start_datetime DATE NOT NULL,
                        end_datetime DATE NOT NULL,
                        PRIMARY KEY (pomodoro_id, start_datetime)
                    )
                """
            )

    def __to_datetime(self, date: str) -> datetime:
        return datetime.strptime(date, DATETIME_FORMAT)

    def teardown(self):
        if self.__db_name != 'test':
            return
        with self.__conn:
            self.__conn.execute('DROP TABLE pomodoro')

    def generate_new_pomodoro(self) -> int:
        sql = """
            SELECT MIN(pomodoro_id) + 1 AS next_id
            FROM pomodoro
            WHERE pomodoro_id >= 1
                AND pomodoro_id + 1 NOT IN (
                    SELECT DISTINCT pomodoro_id
                    FROM pomodoro
                )
            GROUP BY pomodoro_id
            LIMIT 1
        """
        result = self.__conn.execute(sql).fetchall()
        if not result:
            return 1
        return result[0]['next_id']

    def save_pomodoro(self, pomodoro_id: int, pomodoro_info: dict) -> None:
        sql = """
            INSERT INTO pomodoro (pomodoro_id, start_datetime, end_datetime)
            VALUES (?, ?, ?)
        """
        data = [
            pomodoro_id,
            pomodoro_info['start_time'],
            pomodoro_info['end_time']
        ]
        self.__conn.execute(sql, data)
        

    def get_pomodoros(self, pomodoro_id: int) -> list:
        sql = """
            SELECT pomodoro_id, start_datetime, end_datetime
            FROM pomodoro
            WHERE pomodoro_id = ?
            ORDER BY start_datetime
        """
        data = [pomodoro_id]
        result_set = self.__conn.execute(sql, data)
        pomodoros = []
        for row in result_set.fetchall():
            pomodoros.append(
                {
                    'pomodoro_id': row[0],
                    'start_time': self.__to_datetime(row[1]),
                    'end_time': self.__to_datetime(row[2])
                }
            )
        return pomodoros
