import sys
from typing import List, Tuple
from html.parser import HTMLParser
from pathlib import Path


class Node:
    def __init__(self, parent, tag, attrs):
        self.parent = parent
        self.tag = tag
        self.attrs = attrs
        self.text = None
        self.style = None
        self.children = []


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.node = Node(None, None, None)

    def handle_starttag(self, tag, attrs):
        node = Node(self.node, tag.lower(), attrs)
        for attr, value in attrs:
            if attr.lower() == 'class':
                node.style = value
        self.node.children.append(node)
        self.node = node

    def handle_endtag(self, tag):
        while self.node.tag != tag:  # Ascend if not closed
            self.node = self.node.parent
        self.node = self.node.parent

    def handle_data(self, data):
        text = data.strip()
        if len(text):
            self.node.text = text


class Printer:
    def __init__(self):
        self.text = []
        self.depth = 0

    def __call__(self, *args):
        tab = ' ' * self.depth
        for arg in args:
            self.text.append(tab + arg)

    def indent(self):
        self.depth += 4

    def dedent(self):
        self.depth -= 4

    def __str__(self):
        return '\n'.join(self.text)


def to_html(node: Node, p: Printer):
    tag = node.tag
    attrs = ' '.join([f'{attr}={repr(value)}' for attr, value in node.attrs])
    attrs = f' {attrs} '
    if len(node.children):
        p(f'<{tag}{attrs}>')
        p.indent()
        for child in node.children:
            to_html(child, p)
        p.dedent()
        p(f'</{tag}>')
    else:
        if node.text:
            p(f'<{tag}{attrs}>{node.text}</{tag}>')
        else:
            p(f'<{tag}{attrs}/>')


def transpile(node: Node, p: Printer):
    if node.tag == 'svg':
        svg = Printer()
        to_html(node, svg)
        node.text = str(svg)
        node.children.clear()

    begin = 'box('
    end = f') / {repr(node.style)},' if node.style else '),'
    if node.tag != 'div':
        p(f'# {node.tag}')
    if len(node.children):
        p(begin)
        p.indent()
        for child in node.children:
            transpile(child, p)
        p.dedent()
        p(end)
    else:
        text = repr(node.text) if node.text else ''
        if node.tag == 'svg':
            text += ", mode='svg'"
        p(f'{begin}{text}{end}')


def slurp_input():
    stdin = []
    for line in sys.stdin:
        if line.rstrip() == 'Exit':
            break
        stdin.append(line)
    return ''.join(stdin)


def main(args):
    html = slurp_input()
    parser = Parser()
    parser.feed(html)
    p = Printer()
    transpile(parser.node, p)
    print(p)


main(sys.argv)
