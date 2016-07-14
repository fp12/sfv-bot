from config import app_config
from db_models import DBPersistence, DBUpdateChannel


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

        # with open('../config/createtables.sql') as data_file:
        try:
            self._c.execute('CREATE TABLE IF NOT EXISTS persistence ("key" TEXT, "value" TEXT)')            
            self._conn.commit()
        except Exception as e:
            self._log_exc('__init__', e)

        try:
            self._c.execute('INSERT INTO persistence (key, value) VALUES (?, ?)', ('last_tweet', '753076611352756228'))
            self._conn.commit()
        except Exception as e:
            self._log_exc('__init__', e)

        try:
            self._c.execute('CREATE TABLE IF NOT EXISTS update_channels ("server_id" TEXT, "channel_id" TEXT)')
            self._conn.commit()
        except Exception as e:
            self._log_exc('__init__', e)

        try:
            self._c.execute('INSERT INTO update_channels (server_id, channel_id) VALUES (?, ?)', ('154261963692703745', '169500338494111744'))
            self._conn.commit()
        except Exception as e:
            self._log_exc('__init__', e)

    def __del__(self):
        self._c.close()
        self._conn.close()

    def _log_exc(self, funcname, e):
        print('DBAccess Exception in {0}: {1}'.format(funcname, e))

    # Twitter

    def set_last_tweet(self, tweet_id):
        try:
            self._c.execute('UPDATE persistence SET value=? WHERE key=?', (tweet_id, 'last_tweet'))
            self._conn.commit()
        except Exception as e:
            self._log_exc('set_last_tweet', e)

    def get_last_tweet(self):
        self._c.execute('SELECT * FROM persistence WHERE key=?', ('last_tweet',))
        return DBPersistence(self._c.fetchone())

    def get_update_channels(self):
        self._c.execute('SELECT * FROM update_channels')
        for x in self._c.fetchall():
            yield DBUpdateChannel(x)


db = DBAccess()
