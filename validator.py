import sys
import argparse
from errors.error import Error

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
ERRORS = []


def main():
    parser = argparse.ArgumentParser(description='Check code for PEP8.')
    parser.add_argument('--files', nargs='*',
                        help='Check transferred files to PEP8')
    parser.add_argument('string', nargs='*')
    arguments = parser.parse_args()
    if arguments.files:
        for file_name in arguments.files:
            with open(file_name) as file:
                line_number = 1
                for line in file:
                    search_errors(line, file_name, line_number)
                    line_number += 1
    else:
        search_errors(' '.join(arguments.string), 'string', 1)
    for error in ERRORS:
        error.write()


def search_errors(line, file_name, line_number):
    if not is_space_count_multiple_four(line):
            ERRORS.append(
                Error(file_name,
                      (1, line_number),
                      'E0101'))
    words = line.split()
    if words[0] == 'class':
        if not is_cap_word(words[1]):
            ERRORS.append(
                Error(file_name,
                      (line.find(words[1])+1, line_number),
                      'E0201'))
    elif words[0] == 'def':
        if not words[1].islower():
            ERRORS.append(
                Error(file_name,
                      (line.find(words[1])+1, line_number),
                      'E0202'))
        # Не используйте пробелы вокруг знака =,
        # если он используется для обозначения именованного аргумента
        # или значения параметров по умолчанию.'''
        for i in range(len(line)):
            if line[i] == '=':
                if line[i-1] == ' ' or line[i+1] == ' ':
                    ERRORS.append(Error(file_name, (i, line_number),
                                        ''))
    elif words[0] == 'import':
        if words[1].isupper():
            ERRORS.append(
                Error(file_name,
                      (line.find(words[1]+1), line_number),
                      'E0203'))
        if words[1].find(',') != -1:
            ERRORS.append(Error(file_name,
                                (line.find(words[0])+words[1].find(',')+1,
                                 line_number),
                                'E0301'))
    # Избегайте лишних пробелов вокруг скобок и знаков препинания
    previous_word = ''
    next_word = ''
    for i in range(len(words)):
        if i+1 < len(words):
            next_word = words[i+1]
        if words[i][-1] in OPENED_BRACKETS and\
                i+1 < len(words) and next_word not in BIN_IPERATORS:
            init_error = {
                '(': 'E0701',
                '[': 'E0704',
                '{': 'E0707',
            }
            ERRORS.append(Error(file_name,
                                (i+1, line_number),
                                init_error[words[i][-1]]))
        if words[i][0] in BRACKETS+PUNCTUATION_MARKS and\
                len(previous_word) > 0 and previous_word[-1] != ',' and\
                previous_word not in BIN_IPERATORS:
            init_error = {
                '(': 'E0702',
                ')': 'E0703',
                '[': 'E0705',
                ']': 'E0706',
                '{': 'E0708',
                '}': 'E0709',
                ',': 'E0710',
                ':': 'E0711',
                ';': 'E0712'
            }
            ERRORS.append(Error(file_name,
                                (i+1, line_number),
                                init_error[words[i][0]]))
        previous_word = words[i]

    #  В стадии разработки
    #  else:
    #      for operator in BIN_OPERATORS:
    #          i = line.find(operator)
    #          if i != -1:
    #              if (line[i-1] != ' ' or line[i+1] != ' ') and\
    #                      not line[i-1].isalpha() and\
    #                      not line[i+1].isalpha():
    #                  ERRORS.append(Error(file_name, (i, line_number),
    #                                      'missing whitespace around operator'))
    #              if line[i-2] == ' ' or line[i+2] == ' ':
    #                  ERRORS.append(Error(file_name, (i, line_number),
    #                                      'multiple spaces around operator'))

    # Не используйте составные инструкции
    for mark in PUNCTUATION_MARKS:
        i = line.find(mark)
        if mark == ',':
            i = -1
        if i != -1:
            if i+1 < len(line.rstrip()):
                    ERRORS.append(Error(file_name,
                                        (i, line_number),
                                        'E0302'))
    # Коментарии
    line = line.lstrip()
    i = line.find('#')
    if i != -1:
        if line[i+1] != ' ':
            ERRORS.append(Error(file_name,
                                (i, line_number),
                                'E0401'))
    # Не сравнивайте логические типы через ==
    for boolean in BOOL_TYPES:
        line_without_spaces = line.replace(' ', '')
        i = line_without_spaces.find(boolean)
        operators = ('==', '!=', 'is', 'isnot')
        if i != -1:
            for operator in operators:
                if line_without_spaces[i-2:i] == operator or\
                   line_without_spaces[i-5:i] == operator:
                    ERRORS.append(Error(file_name,
                                        (i, line_number),
                                        'E0501'))
    if len(line) > 79:
        ERRORS.append(Error(file_name,
                            (79, line_number),
                            'E0601'))


def get_error07(symbol, before=True):
    if before:
        if symbol == '(':
            return 'E702'
        elif symbol == ')':
            return


def is_start_with_tab(line):
    return line[0] == '\t'


def is_space_count_multiple_four(line):
    for (i, ch) in enumerate(line):
        if ch != ' ':
            return i % 4 == 0


def is_cap_word(word):
    return word[0].istitle() and word.find('_') == -1


if __name__ == '__main__':
    main()
