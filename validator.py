def main():
    file_name = input()
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
            if not is_space_count_multiple_four(line):
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
            elif words[0] == 'import':
                if words[1].isupper():
                    errors.append(
                        Error((str.find(line, words[0]), line_number),
                              'Wrong name of module'))
                if words[1].find(',') != -1:
                    errors.append('Every import should be on a separate line')
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
        print(error)


def is_start_with_tab(line):
    if line[0] == '\t':
        return True


def is_space_count_multiple_four(line):
    if line[0] == ' ':
        space_count = 1
        for symbol in line:
            if symbol == ' ':
                space_count += 1
            else:
                break
        if space_count % 4 != 0:
            return True


def is_cap_word(word):
    if word.istitle() or word.find('_') != -1:
        return True


def get_file_content(file_name):
    file = open(file_name)
    content = read(file)
    file.close()
    return content


class Error():
    def __init__(self, coordinte, description):
        pass
