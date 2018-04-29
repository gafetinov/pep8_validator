import sys
import argparse

BIN_IPERATORS = ('==', '=', '+=', '-=', '*=', '/=',
                 '<=', '>=', '<', '>'
                 'not in', 'in', 'is not', 'is',
                 'and', 'or', 'not')
ASSIGNMENT_OPERATORS = ('=', '+=', '-=', '*=', '/=')
PUNCTUATION_MARKS = (',', ';', ':')
BOOL_TYPES = ('True', 'False')
OPENED_BRACKETS = ('(', '[', '{')
CLOSED_BRACKETS = (')', ']', '}')
BRACKETS = OPENED_BRACKETS + CLOSED_BRACKETS
START_WORDS = ('def', 'class', 'if', 'while', 'for')
FILE_NAME = 'input.txt'


def main():
    parser = argparse.ArgumentParser(description='Check code for PEP8.')
    parser.add_argument('--files', nargs='*',
                        help='Check transferred files to PEP8')
    parser.add_argument('string', nargs='*')
    arguments = parser.parse_args()
    errors = []
    if arguments.files:
        for file in arguments.files:
            with open(file) as file:
                for line in file:
                    errors.append(search_errors(line))
    else:
        errors + search_errors(' '.join(arguments.string))
    for error in errors:
        error.write()


def search_errors(line):
    errors = []
    line_number = 1

    if line.isspace():
        previous_line = ''
    line_length = len(line)
    if not is_space_count_multiple_four(line):
            errors.append(
                Error((1, line_number),
                      'Indentation is not a multiple of four'))
    words = line.split()
    if words[0] == 'class':
        if not is_cap_word(words[1]):
            errors.append(
                Error((line.find(words[0]), line_number),
                      'Wrong name of class'))
    elif words[0] == 'def':
        if not words[1].islower():
            errors.append(
                Error((line.find(words[0]), line_number),
                      'Wrong name of function'))
        # Не используйте пробелы вокруг знака =,
        # если он используется для обозначения именованного аргумента
        # или значения параметров по умолчанию.'''
        for i in range(line_length):
            if line[i] == '=':
                if line[i-1] == ' ' or line[i+1] == ' ':
                    errors.append(Error((i, line_number),
                                        'Unexpected spaces around keyword / parameter equals'))
    elif words[0] == 'import':
        if words[1].isupper():
            errors.append(
                Error((line.find(words[0]), line_number),
                      'Wrong name of module'))
        if words[1].find(',') != -1:
            errors.append(Error((1, line_number),
                                'Every import should be on a separate line'))
    # Избегайте лишних пробелов вокруг скобок и знаков препинания
    previous_word = ''
    next_word = ''
    for i in range(len(words)):
        if i+1 < len(words):
            next_word = words[i+1]
        if words[i][-1] in OPENED_BRACKETS and\
                i+1 < len(words) and next_word not in BIN_IPERATORS:
            errors.append(Error((1, line_number),
                                'whitespace after ' + words[i][-1]))
        if words[i][0] in BRACKETS+PUNCTUATION_MARKS and\
                len(previous_word) > 0 and previous_word[-1] != ',' and\
                previous_word not in BIN_IPERATORS:
            errors.append(Error((1, line_number),
                                'whitespace before ' + words[i][0]))
        previous_word = words[i]
    # Не используйте пробелы вокруг знака =,
    # если он используется для обозначения именованного аргумента
    # или значения параметров по умолчанию.'''
    if words[0] == 'def':
        for i in range(line_length):
            if line[i] == '=':
                if line[i-1] == ' ' or line[i+1] == ' ':
                    errors.append(Error((i, line_number),
                                        'unexpected spaces around keyword / parameter equals'))

    #  В стадии разработки
    #  else:
    #      for operator in BIN_IPERATORS:
    #          i = line.find(operator)
    #          if i != -1:
    #              if (line[i-1] != ' ' or line[i+1] != ' ') and\
    #                      not line[i-1].isalpha() and\
    #                      not line[i+1].isalpha():
    #                  errors.append(Error((i, line_number),
    #                                      'missing whitespace around operator'))
    #              if line[i-2] == ' ' or line[i+2] == ' ':
    #                  errors.append(Error((i, line_number),
    #                                      'multiple spaces around operator'))

    # Не используйте составные инструкции
    for mark in PUNCTUATION_MARKS:
        i = line.find(mark)
        if mark == ',':
            i = -1
        if i != -1:
            if i+1 < len(line.rstrip()):
                    errors.append(Error((i, line_number),
                                        'multiple statements on one line'))
    # Коментарии
    line = line.lstrip()
    i = line.find('#')
    if i != -1:
        if line[i+1] != ' ':
            errors.append(Error((i, line_number),
                                'inline comment should start with "# "'))
    # Не сравнивайте логические типы через ==
    for boolean in BOOL_TYPES:
        line_without_spaces = line.replace(' ', '')
        i = line_without_spaces.find(boolean)
        operators = ('==', '!=', 'is', 'isnot')
        if i != -1:
            for operator in operators:
                if line_without_spaces[i-2:i] == operator or\
                   line_without_spaces[i-5:i] == operator:
                    errors.append(Error((i, line_number),
                                        'Do not compare logical types through operators "==", "!=", "is", "is not"'))
    if line_length > 79:
        errors.append(Error((79, line_number),
                            'Symbols in line over than 79'))
    line_number += 1
    return errors


def is_start_with_tab(line):
    return line[0] == '\t'


def is_space_count_multiple_four(line):
    for (i, ch) in enumerate(line):
        if ch != ' ':
            return i % 4 == 0


def is_cap_word(word):
    return word[0].istitle() and word.find('_') == -1


class Error:
    def __init__(self, coordintes, description):
        self.coordinates = coordintes
        self.description = description

    def write(self):
        print('{0}:{1}'.format(self.coordinates, self.description))

    def get_description(self):
        return self.description


if __name__ == '__main__':
    main()
