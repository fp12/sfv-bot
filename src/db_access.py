from config import app_config
from db_models import DBPersistence, DBUpdateChannel
from log import log_db


class DBAccess():
    def __init__(self):
        if 'heroku' in app_config:
            import psycopg2
            from urllib.parse import urlparse
            url = urlparse(app_config['database'])
            self._conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
        else:
            import sqlite3
            self._conn = sqlite3.connect(app_config['database'])
        self._c = self._conn.cursor()

    def __del__(self):
        self._c.close()
        self._conn.close()

    # Twitter

    def set_last_tweet(self, tweet_id):
        try:
            self._c.execute('UPDATE persistence SET value=%s WHERE key=%s;', (tweet_id, 'last_tweet'))
            self._conn.commit()
        except:
            log_db.exception('set_last_tweet')

    def get_last_tweet(self):
        self._c.execute('SELECT * FROM persistence WHERE key=%s;', ('last_tweet',))
        return DBPersistence(self._c.fetchone())

    def set_last_idle(self, idle):
        idle_txt = 'True' if idle else 'False'
        try:
            self._c.execute('UPDATE persistence SET value=%s WHERE key=%s;', (idle_txt, 'last_idle'))
            self._conn.commit()
        except:
            log_db.exception('set_last_idle')

    def get_last_idle(self):
        self._c.execute('SELECT * FROM persistence WHERE key=%s;', ('last_idle',))
        return DBPersistence(self._c.fetchone())

    def get_update_channels(self):
        self._c.execute('SELECT * FROM update_channels')
        for x in self._c.fetchall():
            yield DBUpdateChannel(x)

    def set_last_message(self, channel_id, message_id):
        try:
            self._c.execute('UPDATE update_channels SET last_message=%s WHERE channel_id=%s;', (message_id, channel_id))
            self._conn.commit()
        except:
            log_db.exception('set_last_message')


db = DBAccess()
