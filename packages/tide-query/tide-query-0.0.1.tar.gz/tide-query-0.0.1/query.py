from enum import Enum
from typing import List, TypedDict

import re
import bs4
import requests

soup = bs4.BeautifulSoup


class YouDaoQuery:
    URL = 'http://www.youdao.com/w/'

    class Language(Enum):
        cn = ''
        # fr = 'fr/'
        # ko = 'ko/'
        # jap = 'jap/'

    class Result(TypedDict):
        source: str
        target: str
        symbol_us: str
        symbol_en: str

    def __init__(self, lang: Language, silent=False):
        assert isinstance(lang, YouDaoQuery.Language)
        self.lang: str = lang.value
        self.silent = silent

    def _get_url(self) -> str:
        return YouDaoQuery.URL + self.lang

    def get_result(self, source: str) -> Result or False:
        self._log(f'Ready query: {source}...')

        text: str = requests.get(self._get_url() + source).text

        if not YouDaoQuery._check(text=text):
            self._log(f'query fail: {source}')
            return YouDaoQuery.Result(
                source=source,
                target='',
                symbol_us='',
                symbol_en='',
            )

        self._log(f'query success: {source}')
        return YouDaoQuery.Result(
            **YouDaoQuery._parse(text),
            source=source,
        )

    def _log(self, content: str):
        self.silent or print(content)

    @staticmethod
    def _check(text: str) -> bool:
        return not not soup(text, features='html.parser').select('.baav')

    @staticmethod
    def _parse(text: str) -> Result:
        targets: str = re.findall(
            re.compile(r'<div class="trans-container">\s+?<ul>([\s\S]+?)</ul>\s+?</div>'),
            text
        )[0]

        target_list: List[bs4.element.Tag] = soup(targets, features='html.parser').select('li')

        pronounce_list: List[bs4.element.Tag] = \
            soup(text, features='html.parser').select('.baav')[0].select('.pronounce')
        symbol_list: List[bs4.element.Tag] = [i.select('.phonetic')[0] for i in pronounce_list]

        return YouDaoQuery.Result(
            target='\n'.join([i.get_text() for i in target_list]),
            symbol_us=symbol_list[0].getText() if len(symbol_list) > 0 else '',
            symbol_en=symbol_list[1].getText() if len(symbol_list) > 1 else '',
        )
