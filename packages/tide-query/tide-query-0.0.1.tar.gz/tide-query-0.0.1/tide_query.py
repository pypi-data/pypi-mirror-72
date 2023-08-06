from .query import YouDaoQuery
from time import sleep
from random import randrange
from typing import List, Tuple


class TideQuery:
    def __init__(self, target: YouDaoQuery, query_list: List[str],
                 interval: Tuple[int, int] = (1, 2)):
        self._target: YouDaoQuery = target
        self._query_list: List[str] = query_list
        self._minimal = min(*interval) * 1000
        self._maximal = max(*interval) * 1000

    def start(self) -> List:
        ret = []
        for i in self._query_list:
            retry_count = 3
            result = YouDaoQuery.Result(source='', target='', symbol_en='', symbol_us='')
            while retry_count:
                sleep(randrange(self._minimal, self._maximal) * 0.001)
                try:
                    result: YouDaoQuery.Result = self._target.get_result(i)
                    if result['symbol_us']:
                        break
                except Exception:
                    pass
                    sleep(5)
                retry_count -= 1
            ret.append(result)
        return ret
