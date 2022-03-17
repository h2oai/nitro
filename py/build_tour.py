from typing import List
import re
from pathlib import Path


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


def indent(prefix: str, lines: List[str]) -> str:
    return '\n'.join([prefix + line for line in lines])


def parse_groups(src: str) -> List[Group]:
    groups = []
    parts = src.split('# # ')[1:]
    for part in parts:
        subparts = part.split('# ## ')
        groups.append(Group(subparts[0].strip(), [parse_example(x) for x in subparts[1:]]))
    return groups


def build_funcs(groups: List[Group]) -> str:
    lines = []
    for g in groups:
        for e in g.examples:
            lines.append('')
            for line in e.code:
                lines.append(line)
            lines.append('')
    return '\n'.join(lines)


def build_topic_map(groups: List[Group]) -> str:
    lines = []
    for g in groups:
        for e in g.examples:
            lines.append(f'{e.name}={e.name},')

    return indent('    ', lines)


def build_toc(groups: List[Group]) -> str:
    lines = []
    for g in groups:
        lines.append(f'- {g.title}')
        for e in g.examples:
            lines.append(f'  - [{e.title}](#{e.name})')
    return indent('', lines)


def build_menu(groups: List[Group]) -> str:
    lines = []
    for g in groups:
        lines.append(f'option(main, "{g.title}", icon="TextDocument", options=[')
        for e in g.examples:
            lines.append(f'    option({e.name}, "{e.title}", icon="TextDocument"),')
        lines.append(']),')
    return indent('        ', lines)


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
