import asyncio
import aiohttp
from config import app_config
import logging
import log
from cfn_const import *
from cfn_models import PlayerSearch


class URL_Binder():
    __Base = 'https://api.prod.capcomfighters.net'
    License = __Base + '/bentov2/sf5/myinfo/%s/fighterlicense/%s'
    Ranking = __Base + '/bentov2/sf5/contents/%s/ranking;page=%s'
    Match = __Base + '/bentov2/sf5/myinfo/%s/match/%s;opponentfull:matchtype=%s'
    Rival = __Base + '/bentov2/sf5/myinfo/%s/searchrival/fightersid;id=%s:sort=lp:page=1:sortdir=d'
    Login = __Base + '/login/extlogin.php'

    def __init__(self, cookie):
        id_from_cookie = cookie.split('%3A')[0].split('=')[1]
        self.License = URL_Binder.License % (id_from_cookie, '%s')
        self.Ranking = URL_Binder.Ranking % (id_from_cookie, '%s')
        self.Match = URL_Binder.Match % (id_from_cookie, '%s', '%s')
        self.Rival = URL_Binder.Rival % (id_from_cookie, '%s')


class CFN_API():
    __AUTH_HEADERS = { 'User-Agent': 'game=KiwiGame, engine=UE4, version=0' }
    __HEADERS = { 'User-Agent': 'game=KiwiGame, engine=UE4, version=0', 'Host': 'api.prod.capcomfighters.net', 'Connection': 'Keep-Alive', 'Cache-Control': 'no-cache' }

    def __init__(self, loop=None): 
        self._loop = loop or asyncio.get_event_loop()
        self._session = None
        self._urls = None

    def __del__(self):
        if self._session:
            self._session.close()

    async def connect(self):
        cookie = app_config['cookie']
        if not cookie:
            auth_cookie = app_config['auth_cookie']
            if auth_cookie:
                headers = self.__AUTH_HEADERS.update({'Cookie' : auth_cookie})
                logging.info('No request cookie: auth login with %s', auth_cookie)
                conn = aiohttp.TCPConnector(verify_ssl=False)
                with aiohttp.ClientSession(connector=conn, loop=self._loop, headers=self._auth) as auth_session:
                    data = app_config['auth_data']
                    logging.info('Requesting Cookie with: %s' % data)
                    async with auth_session.post(URL_Binder.Login, data=data) as resp:
                        if resp.status != 200:
                            logging.error('Couldn\'t post request to CFN API')
                            return False
                        elif not resp.cookies:
                            logging.error('No cookies returned from request: %s', await resp.text())
                            return False
                        else:
                            cookie = resp.cookies
                            logging.info('Successfully returned request cookie: %s', cookie)
            else:
                logging.error('No Auth Cookie to login')
                return False

        if cookie:
            logging.info('Creating session with cookie: %s', cookie)
            headers = self.__HEADERS.update({'Cookie' : cookie})
            self._urls = URL_Binder(cookie)
            conn = aiohttp.TCPConnector(verify_ssl=False)
            self._session = aiohttp.ClientSession(connector=conn, loop=self._loop, headers=headers)
            return True

        logging.error('No cookie to make reqests')
        return False

    async def _get(self, url):
        if self._session:
            async with self._session.get(url) as resp:
                result = await resp.text()
                if 'Session Expired' in result:
                    logging.info('Session expired')
                    self._session.close()
                    self._session = None
                    return None
                return result
        else:
            return None

    async def find_player_by_name(self, player_name):
        potential_names = [player_name]
        if PROBLEM_CHAR in player_name:
            potential_names.extend(player_name.split(PROBLEM_CHAR))
        logging.info('find_player_by_name on: %s' % potential_names)
        for name in potential_names:
            url = self._urls.Rival % name
            search = PlayerSearch.create(await self._get(url))
            if search and len(search.found_players) > 0:
                for player in search.found_players:
                    if player.name.lower() == player_name.lower():
                        return player
        return None


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    cfn_api = CFN_API(loop=loop)
    loop.run_until_complete(cfn_api.connect())
    loop.run_until_complete(cfn_api.find_player_by_name('Backdash_Luffy'))
else:
    cfn_api = CFN_API()
