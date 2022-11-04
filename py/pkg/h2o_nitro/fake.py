import random
import datetime
from typing import Optional, Union

# noinspection SpellCheckingInspection
_lorem = '''
lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna 
aliqua ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat 
duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur 
excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum
'''

# noinspection SpellCheckingInspection
_lorems = set([w.strip() for w in _lorem.split(' ')])
_long_lorems = set([w for w in _lorems if len(w) > 2])


# noinspection PyShadowingBuiltins
def _sentence(min: int, max: int):
    return ' '.join(random.sample(_lorems, random.randint(min, max))).capitalize() + '.'


def lorem(sentences: Optional[int] = None, words: Optional[int] = None):
    if words is not None:
        return ' '.join(random.sample(_long_lorems, words)).title()
    if sentences is None:
        return _sentence(4, 5)
    lines = [_sentence(5, 9) for _ in range(sentences)]
    return ' '.join(lines)


def sentences(k=1):
    return ' '.join(_sentence(5, 9) for _ in range(k))


def words(k=3):
    return ' '.join(random.sample(_long_lorems, k)).title()
