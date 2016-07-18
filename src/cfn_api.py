import asyncio
import aiohttp
from config import app_config
import logging
import log
from cfn_const import *
from cfn_models import PlayerSearch


class URL_Binder():
    __Base = 'https://api.prod.capcomfighters.net/bentov2/sf5'
    License = __Base + '/myinfo/%s/fighterlicense/%s'
    Ranking = __Base + '/contents/%s/ranking;page=%s'
    Match = __Base + '/myinfo/%s/match/%s;opponentfull:matchtype=%s'
    Rival = __Base + '/myinfo/%s/searchrival/fightersid;id=%s:sort=lp:page=1:sortdir=d'

    def __init__(self, cookie):
        id_from_cookie = cookie.split('%3A')[0].split('=')[1]
        self.License = URL_Binder.License % (id_from_cookie, '%s')
        self.Ranking = URL_Binder.Ranking % (id_from_cookie, '%s')
        self.Match = URL_Binder.Match % (id_from_cookie, '%s', '%s')
        self.Rival = URL_Binder.Rival % (id_from_cookie, '%s')


class CFN_API():
    __HEADERS = { 'User-Agent': 'game=KiwiGame, engine=UE4, version=0', 'Host': 'api.prod.capcomfighters.net', 'Connection': 'Keep-Alive', 'Cache-Control': 'no-cache' }

    def __init__(self, loop=None):
        self._cookie = app_config['cookie']
        self.__HEADERS.update({'Cookie' : self._cookie})
        self._urls = URL_Binder(self._cookie)     
        self._loop = loop or asyncio.get_event_loop()
        conn = aiohttp.TCPConnector(verify_ssl=False)
        self._session = aiohttp.ClientSession(connector=conn, loop=self._loop, headers=self.__HEADERS)

    def __del__(self):
        self._session.close()        

    async def _do_request(self, url):
        async with self._session.get(url) as resp:
            result = await resp.text()
            if 'Session Expired' in result:
                logging.info('Session expired')
                return None
            return result

    async def find_player_by_name(self, player_name):
        potential_names = [player_name]
        if PROBLEM_CHAR in player_name:
            potential_names.extend(player_name.split(PROBLEM_CHAR))
        logging.info('find_player_by_name on: %s' % potential_names)
        for name in potential_names:
            url = self._urls.Rival % name
            search = PlayerSearch.create(await self._do_request(url))
            if search and len(search.found_players) > 0:
                for player in search.found_players:
                    if player.name.lower() == player_name.lower():
                        return player
        return None


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(CFN_API(loop=loop).find_player_by_name('Backdash_Luffy'))
else:
    cfn_api = CFN_API()
