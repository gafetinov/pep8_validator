import sys
import argparse
import re
import configparser
import errors.error as err
from errors.error import Error
from collections import deque

BIN_OPERATORS1 = ('==', '=', '+=', '-=', '*=', '/=', '<=', '>=', '<', '>')
BIN_OPERATORS2 = ('in', 'is', 'and', 'or', 'not')
BIN_OPERATORS = BIN_OPERATORS1 + BIN_OPERATORS2
ARITHMETIC_OPERATORS = ('=', '+', '-', '*', '/')
PUNCTUATION_MARKS = (',', ';', ':')
BOOL_TYPES = ('True', 'False')
OPENED_BRACKETS = ('(', '[', '{')
CLOSED_BRACKETS = (')', ']', '}')
BRACKETS = OPENED_BRACKETS + CLOSED_BRACKETS
START_WORDS = ('def', 'class', 'if', 'while', 'for')
QUOTES = ('"', "'")


class Validator:
    def __init__(self, text, is_file=False):
        self.text = text
        self.is_file = is_file
        self.inline_checkers = [self.check_error0101, self.check_error0102,
                                self.check_error0201, self.check_error0202,
                                self.check_error0203, self.check_error0301,
                                self.check_error0302, self.check_error0401,
                                self.check_error0501, self.check_error0601,
                                self.check_error0701, self.check_error0702,
                                self.check_error0703, self.check_error0704,
                                self.check_error0705, self.check_error0706,
                                self.check_error0707, self.check_error0801,
                                self.check_error0903, self.check_error0904,
                                self.check_error0906]
        self.global_checkers = [self.check_error0901, self.check_error0905]
        self.line_number = 1
        self.errors_found = []
        self.bracket_stack = []
        self.in_class = False
        self.previous_lines = deque()

    def search_errors(self):
        if self.is_file:
            try:
                with open(self.text) as file:
                    for line in file:
                        for checker in self.inline_checkers:
                            checker(line)
                        self.previous_lines.append(line)
                        if len(self.previous_lines) > 3:
                            self.previous_lines.popleft()
                        self.line_number += 1
            except FileNotFoundError:
                print('No such file: "{}"'.format(self.text))
                sys.exit(1)
            except Exception:
                print('May be your code in file {} have some syntax errors'
                      .format(self.text))
        else:
            for checker in self.inline_checkers:
                checker(self.text)
        for checker in self.global_checkers:
            checker()
        self.errors_found.sort(key=lambda x: x.coordinates)

    def get_space_count(self, line):
        for (i, ch) in enumerate(line):
            if ch != ' ' and ch not in QUOTES:
                return i

    def is_in_quotes(self, line, index):
        in_single = False
        in_double = False
        for i in range(len(line)):
            symbol = line[i]
            if symbol == "'" and not in_double:
                in_single = not in_single
            if symbol == '"' and not in_single:
                in_double = not in_double
            if i == index:
                return in_single or in_double

    def is_in_quadratic_bracket(self, line, index):
        in_bracket = False
        for i in range(len(line)):
            symbol = line[i]
            if symbol == "[":
                in_bracket = True
            if symbol == ']':
                in_bracket = False
            if i == index:
                return in_bracket

    def is_in_bracket(self, line, index):
        in_bracket = False
        for i in range(len(line)):
            symbol = line[i]
            if symbol == "(":
                in_bracket = True
            if symbol == ')':
                in_bracket = False
            if i == index:
                return in_bracket

    def is_for_parameter(self, line, index):
        bracket_indicator = 0
        for i in range(len(line)):
            symbol = line[i]
            if not self.is_in_quotes(line, i):
                if symbol == '(':
                    bracket_indicator += 1
                elif symbol == ')':
                    bracket_indicator -= 1
            if i == index:
                return bracket_indicator > 0

    def get_all_occurrences(self, sub, string):
        indexes = []
        start = 0
        while string.find(sub, start) != -1:
            start = string.find(sub, start) + 1
            indexes.append(start - 1)
        return indexes

    def check_error0101(self, line):
        if not is_space_count_multiple_four(line) and \
                len(self.bracket_stack) == 0:
            self.errors_found.append(Error((self.line_number, 1), 'E0101'))

    def check_error0102(self, line):
        if self.bracket_stack:
            spaces = self.get_space_count(line)
            sub = line.lstrip()
            if sub[0] in QUOTES:
                spaces -= 1
            index = -1
            if self.bracket_stack[-1] != spaces-1:
                if spaces-1 == line[:re.search('\S', line).start()]\
                        .count(' ')+4:
                    self.errors_found.append(Error((self.line_number, spaces),
                                                   'E0102'))
        for i in range(len(line)):
            symbol = line[i]
            if symbol in OPENED_BRACKETS and not self.is_in_quotes(line, i):
                self.bracket_stack.append(i)
            elif symbol in CLOSED_BRACKETS and \
                    not self.is_in_quotes(line, i):
                self.bracket_stack.pop()

    def check_error0201(self, line):
        words = line.split()
        if words and words[0] == 'class':
            if len(words) == 1:
                self.errors_found.append(Error((self.line_number,
                                                line.find(words[0]) +
                                                len('class')),
                                               'E0201'))
            elif not is_cap_word(words[1]):
                self.errors_found.append(Error((self.line_number,
                                                line.find(words[1])),
                                               'E0201'))

    def check_error0202(self, line):
        words = line.split()
        if words and words[0] == 'def':
            if len(words) == 1:
                self.errors_found.append(Error((self.line_number,
                                                line.find(words[0]) +
                                                len('def')),
                                               'E0202'))
            if not words[1].islower():
                self.errors_found.append(Error((self.line_number,
                                                line.find(words[1])),
                                               'E0202'))

    def check_error0203(self, line):
        words = line.split()
        if words and words[0] == 'import':
            if not words[1].islower():
                self.errors_found.append(Error((self.line_number,
                                                line.find(words[1])),
                                               'E0203'))

    def check_error0301(self, line):
        words = line.split()
        if words and words[0] == 'import':
            if len(words) > 2:
                if words[2] != 'as':
                    self.errors_found.append(Error((self.line_number,
                                                    line.find(words[2])),
                                                   'E0301'))

    def check_error0302(self, line):
        i = line.find(' lambda ')
        if i == -1:
            for mark in PUNCTUATION_MARKS:
                i = line.find(mark)
                if mark == ',':
                    i = -1
                if i != -1:
                    if not self.is_in_quotes(line, i) and \
                            not self.is_in_quadratic_bracket(line, i) and \
                            i + 1 < len(line.rstrip()) \
                            and not self.is_in_bracket(line, i):
                        self.errors_found.append(Error((self.line_number, i),
                                                       'E0302'))

    def check_error0401(self, line):
        line = line.lstrip()
        i = line.find('#')
        if i != -1:
            if line[i + 1] != ' ' and not self.is_in_quotes(line, i):
                self.errors_found.append(Error((self.line_number, i),
                                               'E0401'))

    def check_error0501(self, line):
        for boolean in BOOL_TYPES:
            line_without_spaces = line.replace(' ', '')
            i = line_without_spaces.find(boolean)
            operators = ('==', '!=', 'is', 'isnot')
            if i != -1:
                for operator in operators:
                    if line_without_spaces[i - 2:i] == operator or \
                            line_without_spaces[i - 5:i] == operator:
                        self.errors_found.append(Error((self.line_number, i),
                                                       'E0501'))

    def check_error0601(self, line):
        if len(line) > 79:
            self.errors_found.append(Error((self.line_number, 79), 'E0601'))

    def check_error0701(self, line):
        words = line.split()
        next_word = ''
        symbol_index = len(line)-len(line.lstrip())
        for i in range(len(words)):
            if i + 1 < len(words):
                next_word = words[i + 1]
            if words[i][-1] in OPENED_BRACKETS and \
                    i + 1 < len(words) and next_word not in BIN_OPERATORS:
                self.errors_found.append(Error((self.line_number,
                                                symbol_index+len(words[i])+1),
                                               'E0701'))
            symbol_index += len(words[i])+1

    def check_error0702(self, line):
        words = line.split()
        previous_word = ''
        symbol_index = len(line)-len(line.lstrip())
        for i in range(len(words)):
            index = line.find(words[i])
            if words[i][0] == OPENED_BRACKETS and \
                    not self.is_in_quotes(line, index) and \
                    len(previous_word) > 0 and previous_word[-1] != ',' and \
                    previous_word not in BIN_OPERATORS:
                self.errors_found.append(Error((self.line_number,
                                                symbol_index+len(words[i])+1),
                                               'E0702'))
            previous_word = words[i]
            symbol_index += len(words[i])+1

    def check_error0703(self, line):
        words = line.split()
        previous_word = ''
        symbol_index = len(line)-len(line.lstrip())
        for i in range(len(words)):
            if words[i][0] in CLOSED_BRACKETS and \
                    len(previous_word) > 0 and previous_word[-1] != ',' and \
                    previous_word not in BIN_OPERATORS:
                self.errors_found.append(Error((self.line_number,
                                                symbol_index+len(words[i])+1),
                                               'E0703'))
            previous_word = words[i]
            symbol_index += len(words[i])+1

    def check_error0704(self, line):
        words = line.split()
        previous_word = ''
        symbol_index = len(line) - len(line.lstrip())
        for i in range(len(words)):
            if words[i][0] in PUNCTUATION_MARKS and \
                    len(previous_word) > 0 and previous_word[-1] != ',' and \
                    previous_word not in BIN_OPERATORS:
                self.errors_found.append(Error((self.line_number,
                                                symbol_index+len(words[i])+1),
                                               'E0704'))
            previous_word = words[i]

    def check_error0705(self, line):
        # Unexpected spaces around keyword / parameter equals
        indexes = self.get_all_occurrences('=', line)
        for index in indexes:
            if not self.is_in_quotes(line, index) and \
                    self.is_for_parameter(line, index) and\
                    line[index-1] != '=' and line[index-1] != '!' and\
                    line[index+1] != '=':
                if line[index - 1] == ' ':
                    i = 2
                    while line[index - i] == ' ':
                        i += 1
                    self.errors_found.append(Error((self.line_number,
                                                    index - i + 2),
                                                   'E0705'))
                if line[index + 1] == ' ':
                    i = 2
                    while line[index + i] == ' ':
                        i += 1
                    self.errors_found.append(Error((self.line_number,
                                                    index + i),
                                                   'E0705'))

    # Missing whitespace around operator
    def check_error0706(self, line):
        for operator in BIN_OPERATORS2:
            indexes = self.get_all_occurrences(operator, line)
            for index in indexes:
                if line[index] and not line[index - 1].isalpha() and \
                        not line[index + len(operator)].isalpha() and \
                        line[index - 1] not in ARITHMETIC_OPERATORS and \
                        not self.is_in_quotes(line, index):
                    if (line[index - 1] == ')' or line[index - 1] == '(')\
                            and line[index:index+3] != 'not':
                        self.errors_found.append(Error((self.line_number,
                                                        index - 1),
                                                       'E0706'))
                    if line[index + len(operator)] == ')' or \
                            line[index + len(operator)] == ')':
                        self.errors_found.append(Error((self.line_number,
                                                        index+len(operator)),
                                                       'E0706'))
        for operator in BIN_OPERATORS1:
            indexes = self.get_all_occurrences(operator, line)
            for index in indexes:
                if line[index - 1] not in ARITHMETIC_OPERATORS and \
                        line[index - 1] != '!' and \
                        line[index - 1] != '>' and \
                        line[index - 1] != '<' and \
                        line[index - 1] != '=' and \
                        line[index + 1] != '=' and \
                        not self.is_in_quotes(line, index) and \
                        not self.is_for_parameter(line, index) and \
                        len(self.bracket_stack) > 0:
                    if line[index - 1] != ' ':
                        self.errors_found.append(Error((self.line_number,
                                                        index - 1),
                                                       'E0706'))
                    if line[index + len(operator)] != ' ':
                        self.errors_found.append(Error((self.line_number,
                                                        index +
                                                        len(operator) + 1),
                                                       'E0706'))

    def check_error0707(self, line):
        line = line.lstrip()
        for operator in BIN_OPERATORS:
            indexes = self.get_all_occurrences(operator, line)
            for index in indexes:
                if line[index - 1] not in ARITHMETIC_OPERATORS and \
                        not self.is_in_quotes(line, index):
                    if line[index - 1] == ' ':
                        if line[index - 2] == ' ':
                            i = 2
                            while line[index - i] == ' ':
                                i += 1
                            self.errors_found.append(Error((self.line_number,
                                                            i),
                                                           'E0707'))
                    if line[index + len(operator)] == ' ':
                        if line[index + len(operator) + 1] == ' ':
                            i = len(operator) + 1
                            while line[index + 1] == ' ':
                                i += 1
                            self.errors_found.append(Error((self.line_number,
                                                            index + i),
                                                           'E0707'))

    def check_error0801(self, line):
        indexes = self.get_all_occurrences(' lambda ', line)
        for i in indexes:
            if not self.is_in_quotes(line, i):
                self.errors_found.append(Error((self.line_number, i),
                                               'E0801'))

    def check_error0901(self):
        if self.is_file and self.previous_lines[-1][-1] != '\n':
            self.errors_found.append(Error((self.line_number, 0), 'E0901'))

    def check_error0902(self, line):
        if line.startswith('class') and \
                len(self.previous_lines) >= self.line_number:
            if self.previous_lines[self.line_number - 1] != ' ' and \
                    self.previous_lines[self.line_number - 2] != ' ' and \
                    self.previous_lines[self.line_number - 3] == ' ':
                self.errors_found.append(Error((self.line_number,
                                                line.find('class')), 'E0902'))

    def check_error0903(self, line):
        if (line.startswith('def') or line.startswith('class'))\
                and self.line_number > 2:
            if not (self.previous_lines[-1].isspace() and
                    self.previous_lines[-2].isspace()):
                self.errors_found.append(Error((self.line_number, 1),
                                               'E0903'))
            elif self.line_number > 3 and self.previous_lines[-3].isspace():
                self.errors_found.append(Error((self.line_number, 1),
                                               'E0903'))

    def check_error0904(self, line):
        if (line.lstrip().startswith('def') and self.line_number > 2 and
                not self.previous_lines[-1].lstrip().startswith('class') and
                not self.previous_lines[-1].lstrip().startswith('def') and
                not self.previous_lines[-1].lstrip().startswith('#') and
                re.match('\s', line)):
            if not self.previous_lines[-1].isspace() or\
                    self.previous_lines[-2].isspace():
                self.errors_found.append(Error((self.line_number,
                                                str.find('def', line)+1),
                                               'E0904'))

    def check_error0905(self):
        if self.is_file and self.previous_lines[-1] == '\n' and \
                self.previous_lines[-2][-1] == '\n':
            self.errors_found.append(Error((self.line_number, 1), 'E0905'))

    def check_error0906(self, line):
        if (re.match('\S', line.lstrip()) and self.line_number > 2 and
                self.previous_lines[-1].isspace() and
                self.previous_lines[-2].isspace()):
            if re.match('\s', line):
                self.errors_found.append(Error((self.line_number, 1),
                                               'E0906'))
            elif self.line_number > 3 and self.previous_lines[-3].isspace():
                self.errors_found.append(Error((self.line_number, 1),
                                               'E0906'))


def main():
    errors = {}
    parser = argparse.ArgumentParser(description='Check code for PEP8.')
    parser.add_argument('--files', nargs='*',
                        help='Check transferred files to PEP8')
    parser.add_argument('string', nargs='*')
    parser.add_argument('--language', nargs=1,
                        help='You can choose language: english')
    arguments = parser.parse_args()

    config = configparser.ConfigParser()
    config.read('errors/settings.ini')
    settings = config['Languages']
    if arguments.language:
        language = arguments.language[0]
        if language in err.__LANGUAGES:
            settings['Language'] = language
        else:
            print("I don't know this language: \"{}\"".format(language))
            settings['Language'] = 'english'
    else:
        settings['Language'] = 'english'
    with open('errors/settings.ini', 'w') as file:
        config.write(file)

    if arguments.files:
        for file_name in arguments.files:
            validator = Validator(file_name, is_file=True)
            try:
                validator.search_errors()
            except Exception:
                print('May be your code in file "{}" have some syntax errors'
                      .format(file_name))
            errors[file_name] = validator.errors_found
    else:
        validator = Validator(' '.join(arguments.string))
        try:
            validator.search_errors()
        except Exception:
            print('May be your string "{}" have some syntax errors'
                  .format(' '.join(arguments.string)))
        errors['string'] = validator.errors_found
    errors_is_found = False
    if errors:
        for file in errors:
            print('{}:'.format(file))
            if errors[file]:
                errors_is_found = True
                for error in errors[file]:
                    error.write()
            else:
                print('OK')
            print('\n')
    if errors_is_found:
        sys.exit(1)


def is_space_count_multiple_four(line):
    for (i, ch) in enumerate(line):
        if ch != ' ':
            return i % 4 == 0


def is_cap_word(word):
    return word[0].istitle() and word.find('_') == -1


if __name__ == '__main__':
    main()
