from typing import List
import shutil
import re
from pathlib import Path


class Printer:
    def __init__(self, indent='    '):
        self._lines = []
        self._indent = indent
        self._level = 0

    def indent(self):
        self._level += 1
        return self

    def dedent(self):
        self._level -= 1
        return self

    def __call__(self, line=''):
        self._lines.append((self._indent * self._level) + line)

    def __str__(self):
        return '\n'.join(self._lines)


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
    return str(p)


def build_topic_map(groups: List[Group]) -> str:
    p = Printer().indent()
    for g in groups:
        for e in g.examples:
            p(f'{e.name}={e.name},')

    return str(p)


def build_toc(groups: List[Group]) -> str:
    p = Printer()
    for g in groups:
        p(f'- {g.title}')
        for e in g.examples:
            p(f'  - [{e.title}](#{e.name})')
    return str(p)


def build_menu(groups: List[Group]) -> str:
    p = Printer().indent().indent()
    for g in groups:
        p(f'option(main, "{g.title}", icon="TextDocument", options=[')
        p.indent()
        for e in g.examples:
            p(f'option({e.name}, "{e.title}", icon="TextDocument"),')
        p.dedent()
        p(']),')
    return str(p)


def write_tour(groups: List[Group]):
    tour = Path('tour.template.py').read_text(). \
        replace('# EXAMPLES', build_funcs(groups)). \
        replace('    # TOPIC_MAP', build_topic_map(groups)). \
        replace('TOC', build_toc(groups)). \
        replace('        # MENU', build_menu(groups))
    Path('tour.py').write_text(tour)


def write_examples(groups: List[Group]):
    template = Path('example.template.py').read_text()
    examples_dir = Path('examples')
    for g in groups:
        group_dir = examples_dir / g.title.lower()
        shutil.rmtree(group_dir)
        group_dir.mkdir(parents=True)
        for e in g.examples:
            code = template.replace('# CODE', '\n' + '\n'.join(e.code).strip() + '\n')
            (group_dir / f'{e.name}.py').write_text(code)


def write_readme(groups: List[Group]):
    p = Printer()
    for g in groups:
        for e in g.examples:
            p(f'### {g.title} - {e.title}')
            p()
            for line in e.comments:
                p(line)
            p()
            p('```py')
            for line in e.code:
                p(line)
            p('```')
            p()
    readme = Path('README.template.md').read_text(). \
        replace('EXAMPLES', str(p))
    Path('../README.md').write_text(readme)


def main():
    groups = parse_groups(Path('examples.py').read_text())
    write_tour(groups)
    write_examples(groups)
    write_readme(groups)


if __name__ == '__main__':
    main()
