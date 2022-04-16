# Copyright 2022 H2O.ai, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# This script extracts all the examples from examples.py and exports them
# to the interactive tour, README, docs, etc.
#
# Warning: Super-fragile, but gets the job done. Tread carefully.
#

from typing import Union, List
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


def dedent(lines: List[str]) -> List[str]:
    return [line[4:] if line.startswith('    ') else line for line in lines]


def is_def(line: str) -> bool:
    return line.startswith('def ')


def quote_newlines(line: str) -> str:
    return line.replace('\\n', '\\\\n')


def remove_def_if_only_def(lines: List[str]) -> List[str]:
    n = 0
    for line in lines:
        if is_def(line):
            n += 1
    if n == 1:
        if is_def(lines[0]):
            return dedent(lines[1:])
    return lines


def strip_lines(lines: List[str]) -> List[str]:
    return '\n'.join(lines).strip().splitlines()


class Code:
    def __init__(self):
        self.lines: List[str] = []


class Comment:
    def __init__(self):
        self.lines: List[str] = []


Block = Union[Code, Comment]


class Example:
    def __init__(self, title: str, name: str, blocks: List[Block]):
        self.title = title
        self.name = name
        self.blocks = blocks


class Group:
    def __init__(self, title: str, description: str, examples: List[Example]):
        self.name = title.lower().replace(' ', '-')
        self.title = title
        self.description = description
        self.examples = examples


def parse_example(src: str) -> Example:
    lines = src.strip().splitlines()
    title = lines[0].strip()
    blocks: List[Block] = []
    block = None

    def save():
        if block:
            block.lines = strip_lines(block.lines)
            if len(block.lines):
                blocks.append(block)

    for line in lines[1:]:
        if line.startswith('#'):
            if not isinstance(block, Comment):
                save()
                block = Comment()
            block.lines.append(line.lstrip('# '))
        else:
            if not isinstance(block, Code):
                save()
                block = Code()
            block.lines.append(line)

    save()

    name = None
    for block in blocks:
        if isinstance(block, Code):
            name = re.match(r'^def\s+(\w+)', block.lines[0]).group(1)
            break

    if name is None:
        raise ValueError('could not determine example name')

    return Example(title, name, blocks)


def parse_groups(src: str) -> List[Group]:
    groups = []
    parts = src.split('# # ')[1:]
    for part in parts:
        subparts = part.split('# ## ')
        header = subparts[0].strip().splitlines()
        title = header[0]
        description = '\n'.join(header[1:])
        groups.append(Group(title, description, [parse_example(x) for x in subparts[1:]]))
    return groups


def build_funcs(groups: List[Group]) -> str:
    p = Printer()
    for g in groups:
        for e in g.examples:
            doc_var = e.name + '_docs'
            p()
            p(f'{doc_var} = (')
            p('"""')
            p(f'## {g.title} - {e.title}')
            for block in e.blocks:
                if isinstance(block, Comment):
                    for line in block.lines:
                        p(line)
                else:
                    p("```py")
                    for line in remove_def_if_only_def(block.lines):
                        p(quote_newlines(line))
                    p("```")
            p('""",')
            p("    '### Output',")
            p(')')
            p()
            for block in e.blocks:
                if isinstance(block, Code):
                    p()
                    for line in block.lines:
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
        p()
        p(f'### {g.title}')
        p()
        for e in g.examples:
            p(f'- [{e.title}](#{e.name})')
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
    tour = (Path('docs') / '_template.py').read_text(). \
        replace('# EXAMPLES', build_funcs(groups)). \
        replace('    # TOPIC_MAP', build_topic_map(groups)). \
        replace('TOC', build_toc(groups)). \
        replace('        # MENU', build_menu(groups))
    tour_dir = Path('h2o_nitro') / 'docs'
    tour_dir.mkdir(exist_ok=True)
    (tour_dir / 'docs.py').write_text(tour)


def write_example(p: Printer, e: Example):
    for block in e.blocks:
        if isinstance(block, Comment):
            p()
            for line in block.lines:
                p(line)
            p()
        else:
            p()
            p('```py')
            for line in remove_def_if_only_def(block.lines):
                p(line)
            p('```')
            p()


docs_dir = Path('..') / 'docs'


def write_docs_examples(groups: List[Group]):
    for g in groups:
        p = Printer()
        p(f'# {g.title}')
        p()
        p(g.description)
        for e in g.examples:
            p()
            p(f'## {e.title}')
            write_example(p, e)
        (docs_dir / f'{g.name}.md').write_text(str(p))


yaml_separator_begin = '# Begin generated'
yaml_separator_end = '# End generated'


def write_docs_yaml(groups: List[Group]):
    p = Printer('  ')

    yaml_path = Path('..') / 'mkdocs.yml'
    yaml = yaml_path.read_text()
    yaml_begin = yaml.split(yaml_separator_begin)[0].strip()
    yaml_end = yaml.split(yaml_separator_end)[1].strip()

    p(yaml_begin)
    p.indent()
    p(yaml_separator_begin)

    p('- Guide:')
    p.indent()
    for g in groups:
        p(f"- '{g.name}.md'")

    p(yaml_separator_end)
    p.dedent()
    p(yaml_end)

    yaml_path.write_text(str(p))


def decr_headings(s: str):
    return re.sub(r'^#', '##', s, flags=re.MULTILINE)


def write_readme(groups: List[Group]):
    readme = (docs_dir / 'index.md').read_text()
    readme = readme.replace('assets/', 'docs/assets/')
    readme += decr_headings((docs_dir / 'install.md').read_text())
    (Path('..') / 'README.md').write_text(readme)


def count_examples(groups: List[Group]):
    n = 0
    for g in groups:
        n += len(g.examples)
    return n


def read_example_code(file_name):
    print(f'Reading {file_name} ...')

    code = (Path('docs') / file_name).read_text()

    # Clear everything before the first H1, if any
    parts = code.split('# # ')
    if len(parts) > 1:
        parts[0] = ''

    code = '\n# # '.join(parts)  # re-assemble

    def include_file(match):
        return read_example_code(match.group(1).strip())

    return re.sub(r'^# #include (.+)', include_file, code, flags=re.MULTILINE)


def main():
    print('Collecting examples...')
    examples_code = read_example_code('index.py')

    print('Parsing examples')
    groups = parse_groups(examples_code)

    print(f'Found {count_examples(groups)} examples in {len(groups)} groups.')

    print('Generating tour...')
    write_tour(groups)

    print('Generating README.md...')
    write_readme(groups)

    print('Generating examples for docs...')
    write_docs_examples(groups)

    print('Updating mkdocs.yml...')
    write_docs_yaml(groups)

    print('Done!')


if __name__ == '__main__':
    main()
