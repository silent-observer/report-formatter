import input_parser
import output_generator
import pprint
import sys, os
import re
import logger
import traceback

if len(sys.argv) != 2:
    print("Usage: python formatter.py <input file>")
    input()
else:
    try:
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(application_path)
        generator = output_generator.DocxGenerator()

        filename = sys.argv[1]
        folder = re.match(r'^(.*)[/\\][^/\\]+$', filename)
        if folder:
            os.chdir(folder.group(1))
        parsed = input_parser.parse_markdown(filename)
        #pprint.pprint(parsed)
        settings = {
            'headingsArePadded': True,
            'blockEquationsArePadded': True,
            'tocTitle': 'Содержание',
            'sectionPageBreak': True,
            'headingsAutonumber': True,
            'tablesArePadded': False,
            'tableName': 'Таблица',
            'picturesArePadded': False,
            'pictureName': 'Рисунок',
            'structNames': ['РЕФЕРАТ', 'ВВЕДЕНИЕ', 'ЗАКЛЮЧЕНИЕ']
        }
        generator.set_settings(settings)
        generator.generate_ast(parsed)
        filename = re.sub(r'^(.*)\.[^.]+$', r'\1.docx', filename)
        generator.save(filename)
        if logger.have_logs():
            print(logger.get_logs())
            print('Press Enter to close this window')
            input()
        else:
            print('Succesfully generated ' + filename + '!')
    except:
        print(traceback.format_exc())
        input()
