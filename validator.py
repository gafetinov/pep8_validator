import sys
import argparse
from errors.error import Error

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


def is_in_quotes(line, index):
    in_single = False
    in_double = False
    for i in range(len(line)):
        symbol = line[i]
        if symbol == "'":
            in_single = not in_single
        if symbol == '"':
            in_double = not in_double
        if i == index:
            return in_single or in_double


def is_for_parameter(line, index):
    bracket_indicator = 0
    for i in range(len(line)):
        symbol = line[i]
        if not is_in_quotes(line, i):
            if symbol == '(':
                bracket_indicator += 1
            elif symbol == ')':
                bracket_indicator -= 1
        if i == index:
            return bracket_indicator > 0


def get_all_occurrences(sub, string):
    indexes = []
    start = 0
    while string.find(sub,  start) != -1:
        start = string.find(sub, start)+1
        indexes.append(start-1)
    return indexes


def check_error0101(line):
    result = []
    if not is_space_count_multiple_four(line):
        result.append((0, 'E0101'))
    return result


def check_error0201(line):
    result = []
    words = line.split()
    if words[0] == 'class':
        if len(words) == 1:
            result.append((line.find(words[0])+len('class'), 'E0201'))
        elif not is_cap_word(words[1]):
            result.append((line.find(words[1]), 'E0201'))
    return result


def check_error0202(line):
    result = []
    words = line.split()
    if words[0] == 'def':
        if len(words) == 1:
            result.append((line.find(words[0])+len('def'), 'E0202'))
        if not words[1].islower():
            result.append((line.find(words[1]), 'E0202'))
    return result


def check_error0203(line):
    result = []
    words = line.split()
    if words[0] == 'import':
        if not words[1].islower():
            result.append((line.find(words[1]), 'E0203'))
    return result


def check_error0301(line):
    result = []
    words = line.split()
    if words[0] == 'import':
        if len(words) > 2:
            result.append((line.find(words[2]), 'EO3O1'))
    return result


def check_error0302(line):
    result = []
    i = line.find(' lambda ')
    if i == -1:
        for mark in PUNCTUATION_MARKS:
            i = line.find(mark)
            if mark == ',':
                i = -1
            if i != -1:
                if i + 1 < len(line.rstrip()):
                    result.append((i, 'E0302'))
    return result


def check_error0401(line):
    result = []
    line = line.lstrip()
    i = line.find('#')
    if i != -1:
        if line[i+1] != ' ':
            result.append((i, 'E0401'))
    return result


def check_error0501(line):
    result = []
    for boolean in BOOL_TYPES:
        line_without_spaces = line.replace(' ', '')
        i = line_without_spaces.find(boolean)
        operators = ('==', '!=', 'is', 'isnot')
        if i != -1:
            for operator in operators:
                if line_without_spaces[i-2:i] == operator or\
                   line_without_spaces[i-5:i] == operator:
                    result.append((i, 'E0501'))
    return result


def check_error0601(line):
    result = []
    if len(line) > 79:
        result.append((79, 'E0601'))
    return result


def check_error0701(line):
    result = []
    words = line.split()
    next_word = ''
    for i in range(len(words)):
        if i+1 < len(words):
            next_word = words[i+1]
        if words[i][-1] in OPENED_BRACKETS and\
                i+1 < len(words) and next_word not in BIN_OPERATORS:
            result.append((i+1, 'E0701'))
    return result


def check_error0702(line):
    result = []
    words = line.split()
    previous_word = ''
    for i in range(len(words)):
        if words[i][0] in OPENED_BRACKETS and \
                len(previous_word) > 0 and previous_word[-1] != ',' and \
                previous_word not in BIN_OPERATORS:
            result.append((i+1, 'E0702'))
        previous_word = words[i]
    return result


def check_error0703(line):
    result = []
    words = line.split()
    previous_word = ''
    for i in range(len(words)):
        if words[i][0] in CLOSED_BRACKETS and \
                len(previous_word) > 0 and previous_word[-1] != ',' and \
                previous_word not in BIN_OPERATORS:
            result.append((i+1, 'E0703'))
        previous_word = words[i]
    return result


def check_error0704(line):
    result = []
    words = line.split()
    previous_word = ''
    for i in range(len(words)):
        if words[i][0] in PUNCTUATION_MARKS and \
                len(previous_word) > 0 and previous_word[-1] != ',' and \
                previous_word not in BIN_OPERATORS:
            result.append((i+1, 'E0704'))
        previous_word = words[i]
    return result


def check_error0705(line):
    # Unexpected spaces around keyword / parameter equals
    result = []
    indexes = get_all_occurrences('=', line)
    for index in indexes:
        if not is_in_quotes(line, index) and is_for_parameter(line, index):
            if line[index-1] == ' ':
                i = 2
                while line[index-i] == ' ':
                    i += 1
                result.append((index-i+2, '0705'))
            if line[index+1] == ' ':
                i = 2
                while line[index+i] == ' ':
                    i += 1
                result.append((index+i, 'E0705'))
    return result


def check_error0706(line):
    # Missing whitespace around operator
    result = []
    for operator in BIN_OPERATORS2:
        indexes = get_all_occurrences(operator, line)
        for index in indexes:
            if line[index] and not line[index-1].isalpha() and\
                    not line[index+len(operator)].isalpha() and\
                    line[index-1] not in ARITHMETIC_OPERATORS and\
                    not is_in_quotes(line, index):
                if line[index-1] != ' ':
                    result.append((index-1, 'E0706'))
                if line[index+len(operator)] != ' ':
                    result.append((index+len(operator), 'E0706'))
    for operator in BIN_OPERATORS1:
        indexes = get_all_occurrences(operator, line)
        for index in indexes:
            if line[index-1] not in ARITHMETIC_OPERATORS and\
                    not is_in_quotes(line, index) and\
                    not is_for_parameter(line, index):
                if line[index-1] != ' ':
                    result.append((index-1, 'E0706'))
                if line[index+len(operator)] != ' ':
                    result.append((index+len(operator)+1, 'E0706'))
    return result


def check_error0707(line):
    result = []
    for operator in BIN_OPERATORS:
        indexes = get_all_occurrences(operator, line)
        for index in indexes:
            if line[index-1] not in ARITHMETIC_OPERATORS and\
                    not is_in_quotes(line, index):
                if line[index-1] == ' ':
                    if line[index-2] == ' ':
                        i = 2
                        while line[index-i] == ' ':
                            i += 1
                        result.append((index-i+2, 'E0707'))
                if line[index+len(operator)] == ' ':
                    if line[index+len(operator)+1] == ' ':
                        i = len(operator)+1
                        while line[index+1] == ' ':
                            i += 1
                        result.append((index+i, 'E0707'))
    return result


def check_error0801(line):
    result = []
    indexes = get_all_occurrences(' lambda ', line)
    for i in indexes:
        result.append((i, 'E0801'))
    return result


class Error09:
    def __init__(self, file_name, lines):
        self.nesting = []
        self.file_name = file_name
        self.lines = lines
        self.errors = self.check()

    def check(self):
        err = []
        indent = 0
        previous_indent = indent
        for i in range(len(self.lines)):
            line = self.lines[i]
            words = line.split()
            if words:
                if words[0] == 'class':
                    indent = line.find('class')
                    if i > 2 and indent == previous_indent:
                        if self.lines[i-1] != '\n' or self.lines[i-2] != '\n':
                            err.append(Error(self.file_name,
                                             (i+1, line.find('class')), 'E0902'))
                        else:
                            if self.lines[i-3] == '\n':
                                err.append(Error(self.file_name,
                                                 (i+1, line.find('class')),
                                                 'E0902'))
                    self.nesting.append('class')
                elif words[0] == 'def':
                    indent = line.find('def')
                    if i > 2:
                        if indent == 0:
                            if self.lines[i-1] != '\n' or \
                                    self.lines[i-2] != '\n':
                                err.append(Error(self.file_name,
                                                 (i+1, line.find('def')),
                                                 'E0903'))
                            else:
                                if self.lines[i - 3] == '\n':
                                    err.append(Error(self.file_name,
                                                     (i + 1,
                                                      line.find('def')),
                                                     'E0903'))
                        else:
                            if indent <= previous_indent:
                                if self.lines[i-1] != '\n':
                                    err.append(Error(self.file_name,
                                                     (i+1, line.find('def')),
                                                     'E0904'))
                                elif self.lines[i-2] == '\n':
                                    err.append(Error(self.file_name,
                                                     (i+1, line.find('def')),
                                                     'E0904'))
                    self.nesting.append('def')
            previous_indent = indent
        if self.lines[-1] != '\n':
            err.append(Error(self.file_name,
                             (len(self.lines), len(self.lines[-1])), 'E0901'))
        return err


def main():
    errors = []
    parser = argparse.ArgumentParser(description='Check code for PEP8.')
    parser.add_argument('--files', nargs='*',
                        help='Check transferred files to PEP8')
    parser.add_argument('string', nargs='*')
    arguments = parser.parse_args()
    if arguments.files:
        for file_name in arguments.files:
            errors += search_errors(file_name)
    else:
        errors = search_errors(' '.join(arguments.string), is_file=False)
    if errors:
        for error in errors:
            error.write()
        sys.exit(1)


def search_errors(file_name='string', is_file=True):
    checkers = [check_error0101, check_error0201, check_error0202,
                check_error0203, check_error0301, check_error0302,
                check_error0401, check_error0501, check_error0601,
                check_error0701, check_error0702, check_error0703,
                check_error0704, check_error0705, check_error0706,
                check_error0707, check_error0801]
    errors = []
    if is_file:
        lines = []
        with open(file_name) as file:
            line_number = 1
            for line in file:
                lines.append(line)
                if line != '\n':
                    for checker in checkers:
                        result = checker(line)
                        for error in result:
                            errors.append(Error(file_name,
                                                (line_number, error[0]),
                                                error[1]))
                line_number += 1
        checker = Error09(file_name, lines)
        errors += checker.errors
    else:
        line = file_name
        for checker in checkers:
            result = checker(line)
            for error in result:
                errors.append(Error(file_name,
                                    (1, error[0]),
                                    error[1]))
    return errors


def is_space_count_multiple_four(line):
    for (i, ch) in enumerate(line):
        if ch != ' ':
            return i % 4 == 0


def is_cap_word(word):
    return word[0].istitle() and word.find('_') == -1


if __name__ == '__main__':
    main()
