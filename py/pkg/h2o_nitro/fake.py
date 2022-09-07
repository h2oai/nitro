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


def _walk(min=0.0, max=100.0, variation: Optional[float] = None, start: Optional[float] = None):
    if variation is None:
        variation = (max - min) / 10.0
    if start is None:
        start = random.uniform(min, max)
    x = start
    while True:
        x += (random.random() - 0.5) * variation
        if not min <= x <= max:
            x = random.uniform(min, max)
        yield x


def numbers(k: Union[int, list], min=0.0, max=100.0, variation: Optional[float] = None, start: Optional[float] = None):
    w = _walk(min, max, variation, start)
    if isinstance(k, list):
        return [(k[i], next(w)) for i in range(len(k))]
    return [next(w) for _ in range(k)]


def hours(k: int, ago: int):
    x = datetime.datetime.utcnow() - datetime.timedelta(hours=ago)
    return [(x + datetime.timedelta(hours=i)).isoformat() + 'Z' for i in range(k)]


def days(k: int, ago: int):
    x = datetime.datetime.utcnow() - datetime.timedelta(days=ago)
    return [(x + datetime.timedelta(days=i)).isoformat() + 'Z' for i in range(k)]
