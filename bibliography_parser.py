import mistune
import re
from mistune.directives.base import Directive
from logger import log

BOOK_REFERENCE_PATTERN = r'\[\!([a-zA-Z_. -]+)\!\]'

def parse_book_reference(inline, m, state):
    text = m.group(1)
    return 'book_ref', text

class DirectiveBook(Directive):
    def parse(self, block, m, state):
        title = m.group('value')
        options = self.parse_options(m)
        book_type = None
        authors = []
        other_people = None
        title_info = None
        edition = None
        city = None
        publisher = None
        year = None
        pages = None
        volume = None
        source = None
        tag = None
        isbn = None
        doi = None
        url = None
        date = None

        for (key, val) in options:
            key = key.replace('_', '-')
            if key == 'type':
                book_type = val
            elif key == 'author':
                authors.append(val)
            elif key == 'other-people':
                other_people = val
            elif key == 'title-info':
                title_info = val
            elif key == 'edition':
                edition = val
            elif key == 'city':
                city = val
            elif key == 'volume':
                volume = val
            elif key == 'source':
                source = val
            elif key == 'publisher' or key == 'website':
                publisher = val
            elif key == 'year':
                try:
                    year = int(val)
                except (ValueError, TypeError):
                    return {
                        'type': 'block_error',
                        'raw': f'Book publishment year MUST be an integer! ({title})'
                    }
            elif key == 'pages':
                try:
                    if book_type == 'article':
                        pages = val
                    else:
                        pages = int(val)
                except (ValueError, TypeError):
                    return {
                        'type': 'block_error',
                        'raw': f'Book page count MUST be an integer! ({title})'
                    }
            elif key == 'isbn':
                isbn = val
            elif key == 'doi':
                doi = val
            elif key == 'url':
                url = val
            elif key == 'date' or key == 'date-of-access':
                date = val
            elif key == 'tag':
                tag = val
            else:
                log(f'Warning: unknown key \'{key}\' in book definition! ({title})')
        if book_type is None:
            return {
                'type': 'block_error',
                'raw': f'Book MUST have a valid type! ({title})'
            }
        
        return {'type': 'book', 'raw': None, 'params': 
            (title, book_type, authors, other_people, title_info, 
            edition, city, publisher, year, pages, volume, source, isbn, doi, url, date, tag)}
    def __call__(self, md):
        self.register_directive(md, 'book')
        if md.renderer.NAME == 'ast':
            md.renderer.register('book', render_ast_book)

        md.inline.register_rule('book_ref', BOOK_REFERENCE_PATTERN, parse_book_reference)
        index = md.inline.rules.index('std_link')
        md.inline.rules.insert(index, 'book_ref')


def render_ast_book(children, title, book_type, authors, 
                    other_people, title_info, 
                    edition, city, publisher, year, pages,
                    volume, source, isbn, doi, url,
                    date, tag):
    return {
        'type': 'book',
        'title': title,
        'book_type': book_type,
        'authors': authors,
        'other_people': other_people,
        'title_info': title_info,
        'edition': edition,
        'city': city,
        'publisher': publisher,
        'year': year,
        'pages': pages,
        'volume': volume,
        'source': source,
        'isbn': isbn,
        'doi': doi,
        'url': url,
        'date': date,
        'tag': tag
    }


def name_reverse(text):
    l = text.split(' ')
    return '\u00A0'.join([l[-1]] + l[:-1])

def output_authors(authors, other_people):
    if len(authors) > 0:
        text = authors[0]
        if len(authors) < 5:
            for i in range(1, len(authors)):
                text += ', ' + authors[i]
            if other_people:
                text += '; ' + other_people
        else:
            for i in range(1, 3):
                text += ', ' + authors[i]
            text += ' [и др]'
    else:
        text = other_people
    return text

def book_text(obj):
    author_name = name_reverse(obj['authors'][0]) if len(obj['authors']) > 0 else None
    for i in range(len(obj['authors'])):
        obj['authors'][i] = obj['authors'][i].replace(' ', '\u00A0')
    text = ''
    if obj['book_type'] == 'book' or obj['book_type'] == 'article':
        if len(obj['authors']) > 0 and len(obj['authors']) < 4:
            text += author_name + ' '
        text += obj['title']
        if obj['title_info']:
            text += ' : ' + obj['title_info']
        if len(obj['authors']) > 0 or obj['other_people']:
            text += ' / '
            text += output_authors(obj['authors'], obj['other_people'])
        if obj['source']:
            text += ' // ' + obj['source']
        text += '. – '
        if obj['edition']:
            text += obj['edition'] + '. – '
        
        missing_fields = ''
        if obj['book_type'] == 'book' and obj['city'] is None:
            missing_fields += 'city, '
        if obj['book_type'] == 'book' and obj['publisher'] is None:
            missing_fields += 'publisher, '
        if obj['year'] is None:
            missing_fields += 'year, '
        if obj['pages'] is None:
            missing_fields += 'pages, '
        if missing_fields != '':
            fields = missing_fields[:-2]
            title = obj['title']
            log(f'ERROR: please specify {fields} for the book {title}')
            return 'ERROR'
        
        if obj['book_type'] == 'book':
            text += obj['city'] + ' : ' + obj['publisher'] + ', '
            text += str(obj['year']) + '. – ' + str(obj['pages']) + ' с.'
        else:
            if obj['volume']:
                text += obj['volume'] + '. – '
            text += str(obj['year']) + '. – с. ' + str(obj['pages'])
        if obj['isbn']:
            text += ' – ISBN ' + obj['isbn'] + '.'
        elif obj['doi']:
            text += ' – DOI ' + obj['doi'] + '.'
    elif obj['book_type'] == 'website':
        text += obj['title']
        if obj['title_info']:
            text += ' : ' + obj['title_info']
        text += '. – '

        if obj['city']:
            text += obj['city']
            if obj['year']:
                text += ', ' + str(obj['year'])
            text += '. – '
        elif obj['year']:
            text += str(obj['year']) + '. – '

        
        missing_fields = ''
        if obj['url'] is None:
            missing_fields += 'url, '
        if obj['date'] is None:
            missing_fields += 'date of access, '
        if missing_fields != '':
            fields = missing_fields[:-2]
            title = obj['title']
            log(f'ERROR: please specify {fields} for the website {title}')
            return 'ERROR'
        
        text += 'URL: ' + obj['url'] + ' (дата обращения: ' + obj['date'] + ').'
    elif obj['book_type'] == 'webpage':
        if len(obj['authors']) > 0 and len(obj['authors']) < 4:
            text += author_name + ' '
        text += obj['title']
        if obj['title_info']:
            text += ' : ' + obj['title_info']
        if len(obj['authors']) > 0 or obj['other_people']:
            text += ' / '
            text += output_authors(obj['authors'], obj['other_people'])
        
        text += ' // '

        missing_fields = ''
        if obj['publisher'] is None:
            missing_fields += 'website name, '
        if obj['url'] is None:
            missing_fields += 'url, '
        if obj['date'] is None:
            missing_fields += 'date of access, '
        if missing_fields != '':
            fields = missing_fields[:-2]
            title = obj['title']
            log(f'ERROR: please specify {fields} for the website {title}')
            return 'ERROR'

        text += obj['publisher'] + ' : [сайт]. – '

        if obj['city']:
            text += obj['city']
            if obj['year']:
                text += ', ' + str(obj['year'])
            text += '. – '
        elif obj['year']:
            text += str(obj['year']) + '. – '

        
        text += 'URL: ' + obj['url'] + ' (дата обращения: ' + obj['date'] + ').'
    else:
        book_type = obj['book_type']
        log(f'ERROR: unknown book type {book_type} for the resource {title}')
        return 'ERROR'
    return text

