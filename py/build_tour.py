from typing import List
import re
from pathlib import Path


class Printer:
    def __init__(self, indent='    '):
        self.lines = []
        self._indent = indent
        self._level = 0

    def indent(self):
        self._level += 1
        return self

    def dedent(self):
        self._level -= 1
        return self

    def __call__(self, line=''):
        self.lines.append((self._indent * self._level) + line)

    def join(self, prefix: str = '') -> str:
        return '\n'.join([prefix + line for line in self.lines])


def read_file(p: str) -> str:
    return Path(p).read_text()


def write_file(p: str, text: str):
    Path(p).write_text(text)


class Example:
    def __init__(self, title: str, name: str, comments: List[str], code: List[str]):
        self.title = title
        self.name = name
        self.comments = comments
        self.code = code


class Group:
    def __init__(self, title: str, examples: List[Example]):
        self.title = title
        self.examples = examples


def parse_example(src: str) -> Example:
    lines = src.strip().splitlines()
    title = lines[0].strip()
    comments = []
    code = []
    for line in lines[1:]:
        if line.startswith('#'):
            comments.append(line.lstrip('# '))
        else:
            code.append(line)

    if len(comments) == 0:
        raise ValueError(f'{title}: no comments')
    if len(code) == 0:
        raise ValueError(f'{title}: no code')

    name = re.match(r'^def\s+(\w+)', code[0]).group(1)

    return Example(title, name, comments, code)


def parse_groups(src: str) -> List[Group]:
    groups = []
    parts = src.split('# # ')[1:]
    for part in parts:
        subparts = part.split('# ## ')
        groups.append(Group(subparts[0].strip(), [parse_example(x) for x in subparts[1:]]))
    return groups


def build_funcs(groups: List[Group]) -> str:
    p = Printer()
    for g in groups:
        for e in g.examples:
            doc_var = e.name + '_docs'
            p()
            p(f'{doc_var} = (')

            p.indent()

            p("'''")
            p(f'## {g.title} - {e.title}')
            for line in e.comments:
                p(f'{line}')
            p("```py")
            for line in e.code:
                p(f'{line}')
            p("```")
            p("''',")
            p("'### Output',")

            p.dedent()
            p(')')
            p()
            p()
            for line in e.code:
                p(line.replace('view(', f'view(*{doc_var}, '))
            p()
    return p.join()


def build_topic_map(groups: List[Group]) -> str:
    p = Printer().indent()
    for g in groups:
        for e in g.examples:
            p(f'{e.name}={e.name},')

    return p.join()


def build_toc(groups: List[Group]) -> str:
    p = Printer()
    for g in groups:
        p(f'- {g.title}')
        for e in g.examples:
            p(f'  - [{e.title}](#{e.name})')
    return p.join()


def build_menu(groups: List[Group]) -> str:
    p = Printer().indent().indent()
    for g in groups:
        p(f'option(main, "{g.title}", icon="TextDocument", options=[')
        p.indent()
        for e in g.examples:
            p(f'option({e.name}, "{e.title}", icon="TextDocument"),')
        p.dedent()
        p(']),')
    return p.join()


def main():
    src = read_file('examples.py')
    groups = parse_groups(src)

    tour = read_file('tour_bootstrap.py')

    tour = tour.replace('# EXAMPLES', build_funcs(groups))
    tour = tour.replace('    # TOPIC_MAP', build_topic_map(groups))
    tour = tour.replace('TOC', build_toc(groups))
    tour = tour.replace('        # MENU', build_menu(groups))

    write_file('tour.py', tour)


if __name__ == '__main__':
    main()
