bin_operators = ('=', '+=', '-=', '*=', '/=',
                 '==', '<', '>', '<=', '>=',
                 'in', 'not in', 'is', 'is not',
                 'and', 'or', 'not')
assignment_operators = ('=', '+=', '-=', '*=', '/=')
punctuation_marks = (',', ';', ':')
bool_types = ('True', 'False')
opened_brackets = ('(', '[', '{')
closed_brackets = (')', ']', '}')
brackets = opened_brackets+closed_brackets
start_words = ('def', 'class', 'if', 'while', 'for')


def main():
    file_name = 'input.txt'
    errors = []
    line_number = 1
    previous_line = None
    with open(file_name) as code:
        start = None
        for line in code:
            line_length = len(line)
            if is_start_with_tab(line):
                errors.append(
                    Error((1, line_number), 'Use spaces instead of tabs'))
            if is_space_count_multiple_four(line):
                    errors.append(
                        Error((1, line_number),
                              'Indentation is not a multiple of four'))
            words = line.split(' ')
            if words[0] == 'class':
                if not is_cap_word(words[0]):
                    errors.append(
                        Error((str.find(line, words[0]), line_number),
                              'Wrong name of class'))
            elif words[0] == 'def':
                if words[1].isupper():
                    errors.append(
                        Error((str.find(line, words[0]), line_number),
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
                        Error((str.find(line, words[0]), line_number),
                              'Wrong name of module'))
                if words[1].find(',') != -1:
                    errors.append(Error((1, line_number),
                                        'Every import should be on a separate line'))
            # Избегайте лишних пробелов вокруг скобок и знаков препинания
            previous_word = ''
            for word in words:
                if word[-1] in opened_brackets:
                    errors.append(Error((1, line_number),
                                        'whitespace after ' + word[-1]))
                if word[0] in brackets+punctuation_marks and\
                        previous_word[-1] != ',':
                    errors.append(Error((1, line_number),
                                        'whitespace before ' + word[0]))
                previous_word = word
            # Не используйте пробелы вокруг знака =,
            # если он используется для обозначения именованного аргумента
            # или значения параметров по умолчанию.'''
            if words[0] == 'def':
                for i in range(line_length):
                    if line[i] == '=':
                        if line[i-1] == ' ' or line[i+1] == ' ':
                            errors.append(Error((i, line_number),
                                                'unexpected spaces around keyword / parameter equals'))
            else:
                for operator in bin_operators:
                    i = line.find(operator)
                    if i != -1:
                        if (line[i-1] != ' ' or line[i+1] != ' ') and\
                                not line[i-1].isalpha() and\
                                not line[i+1].isalpha():
                            errors.append(Error((i, line_number),
                                                'missing whitespace around operator'))
                        if line[i-2] == ' ' or line[i+2] == ' ':
                            errors.append(Error((i, line_number),
                                                'multiple spaces around operator'))
            # Не используйте составные инструкции
            for mark in punctuation_marks:
                i = line.find(mark)
                if mark == ',':
                    i = -1
                if i != -1:
                    if words[0] in start_words:
                        if line[i+1] != '\n':
                            errors.append(Error((i, line_number),
                                                'multiple statements on one line'))
            # Коментарии
            i = line.find('#')
            if i != -1:
                if line[i+1] != ' ' or line[i+2] == ' ':
                    errors.append(Error((i, line_number),
                                        'inline comment should start with "# "'))
            # Не сравнивайте логические типы через ==
            for boolean in bool_types:
                line_without_spaces = line.replace(' ', '')
                i = line_without_spaces.find(boolean)
                operators = ('==', '!=', 'is', 'isnot')
                if i != -1:
                    for operator in operators:
                        if line_without_spaces[i-2:i] == operator or\
                           line_without_spaces[i-5:i] == operator:
                            errors.append(Error((i,line_number),
                                                'Do not compare logical types through operators "==", "!=", "is", "is not"'))
            if line_length > 79:
                errors.append(Error((79, line_number),
                                    'Symbols in line over than 79'))
            line_number += 1
            previous_line = line
    last_line = previous_line
    if last_line != '\n':
        errors.append(Error((len(last_line), line_number),
                            'No new line in the end of file'))
    for error in errors:
        error.write()


def is_start_with_tab(line):
    if line[0] == '\t':
        return True


def is_space_count_multiple_four(line):
    space_count = 0
    if line[0] == ' ':
        space_count += 1
        for symbol in line:
            if symbol == ' ':
                space_count += 1
            else:
                break
        if space_count % 4 == 0:
            return True
    return False


def is_cap_word(word):
    if word.istitle() or word.find('_') != -1:
        return True


def get_file_content(file_name):
    file = open(file_name)
    content = read(file)
    file.close()
    return content


class Error():
    def __init__(self, coordintes, description):
        self.coordinates = coordintes
        self.description = description

    def write(self):
        print(str(self.coordinates) + ':' + self.description)


if __name__ == '__main__':
    main()
