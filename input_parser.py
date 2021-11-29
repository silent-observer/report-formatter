import mistune
import re
from bibliography_parser import DirectiveBook
from logger import log

EQUATION_PATTERN = r'''(?<!\$)\$([^$\n]+)\$'''
BLOCK_EQUATION_PATTERN = re.compile(r''' *\$\$([^$\n]*)\$\$\n''')

def parse_equation(inline, m, state):
    text = m.group(1)
    text = re.sub(r' +([><+*/-=]) +', r'\1', text)
    text = text.replace('*', '⋅')
    return 'equation', text
def parse_block_equation(inline, m, state):
    return {'type': 'block_equation', 'text': m.group(1)}

def plugin_equation(md):
    md.inline.register_rule('equation', EQUATION_PATTERN, parse_equation)
    md.inline.rules.append('equation')
    md.block.register_rule('block_equation', BLOCK_EQUATION_PATTERN, parse_block_equation)
    md.block.rules.append('block_equation')


BLOCK_TABLE_PATTERN = re.compile(
    r' {0,3}!table(?:\[([a-zA-Z0-9_-]+)\])?'
    r'(?: +([0-9]+) ([0-9]+) *)?'
    r' +([^\n]+)\n')
TABLE_SECTION_NUMBERING_PATTERN = re.compile(r''' {0,3}!tablenumbering += +(section|global)\n''')

def parse_block_table(inline, m, state):
    text = m.group(4)
    tag = m.group(1)
    if m.group(2) is not None:
        width = m.group(2)
        height = m.group(3)
        return {'type': 'block_table', 'params': (width, height, text, tag), 'text': ''}
    else:
        return {'type': 'block_table', 'params': (3, 4, text, tag), 'text': ''}
def render_block_table(children, width, height, text, tag):
    return {
        'type': 'block_table',
        'text': text,
        'width': int(width),
        'height': int(height),
        'tag': tag,
        'children': children
    }
def parse_table_numbering(inline, m, state):
    return {'type': 'table_numbering', 'text': m.group(1)}
def plugin_block_table(md):
    md.block.register_rule('block_table', BLOCK_TABLE_PATTERN, parse_block_table)
    md.block.rules.append('block_table')
    md.renderer.register('block_table', render_block_table)
    md.block.register_rule('table_numbering', 
        TABLE_SECTION_NUMBERING_PATTERN, parse_table_numbering)
    md.block.rules.append('table_numbering')


PICTURE_PATTERN = re.compile(
    r' {0,3}!picture(?:\[([a-zA-Z0-9_-]+)\])?'
    r'(?: +([w|h])([0-9.]+))?'
    r' +(?:([\w\/\\.:]+)|"([\w\s\/\\.:]+)")'
    r' +([^\n]+)\n')
PICTURE_SECTION_NUMBERING_PATTERN = re.compile(r''' {0,3}!picturenumbering += +(section|global)\n''')

def parse_picture(inline, m, state):
    path = m.group(4) or m.group(5)
    text = m.group(6)
    tag = m.group(1)
    if m.group(2) is not None:
        symbol = m.group(2)
        try:
            size = float(m.group(3))
        except (ValueError, TypeError):
            log('Warning: picture size MUST be a float!')
        return {'type': 'picture', 'text': '',
            'params': (symbol, size, path, text, tag)}
    else:
        return {'type': 'picture', 'text': '',
            'params': (None, None, path, text, tag)}
def render_picture(children, symbol, size, path, text, tag):
    return {
        'type': 'picture', 
        'text': text, 
        'symbol': symbol, 
        'size': size, 
        'path': path,
        'tag': tag,
        'children': children
    }
def parse_picture_numbering(inline, m, state):
    return {'type': 'picture_numbering', 'text': m.group(1)}
def plugin_picture(md):
    md.block.register_rule('picture', PICTURE_PATTERN, parse_picture)
    md.block.rules.append('picture')
    md.renderer.register('picture', render_picture)
    md.block.register_rule('picture_numbering', 
        PICTURE_SECTION_NUMBERING_PATTERN, parse_picture_numbering)
    md.block.rules.append('picture_numbering')


TOC_PATTERN = re.compile(r''' {0,3}!toc\n''')
BIBLIO_PATTERN = re.compile(r''' {0,3}!biblio\n''')
REF_PATTERN = r'!([a-zA-Z0-9_-]+)!'

def parse_toc(inline, m, state):
    return {'type': 'toc', 'text': ''}
def parse_biblio(inline, m, state):
    return {'type': 'biblio', 'text': ''}
def parse_ref(inline, m, state):
    return 'ref', m.group(1)
def plugin_misc(md):
    md.block.register_rule('toc', TOC_PATTERN, parse_toc)
    md.block.rules.append('toc')
    md.block.register_rule('biblio', BIBLIO_PATTERN, parse_biblio)
    md.block.rules.append('biblio')
    md.inline.register_rule('ref', REF_PATTERN, parse_ref)
    md.inline.rules.append('ref')


CODE_BLOCK_PATTERN  = re.compile(r'''```[a-zA-Z0-9_]*\n((?:``?(?!`)|[^`])*)\n```''')
def parse_code_block(inline, m, state):
    return {'type': 'code_block', 'text': m.group(1)}
def plugin_code(md):
    md.block.register_rule('code_block', CODE_BLOCK_PATTERN, parse_code_block)
    md.block.rules.append('code_block')


def parse_markdown(filename):
    mistune.scanner.Matcher.PARAGRAPH_END = re.compile(
        mistune.scanner.Matcher.PARAGRAPH_END.pattern + r'|(?:\n {0,3}!)')

    markdown = mistune.create_markdown(
        plugins=[plugin_equation, plugin_block_table,
                 plugin_picture, plugin_misc, DirectiveBook()],
        renderer=mistune.AstRenderer()
    )

    text_file = open(filename, mode='r', encoding="utf-8")
    text = text_file.read()
    text_file.close()

    parsed = markdown(text)
    return parsed