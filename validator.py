previous_line = None
errors = []
with open('input.txt') as code:
    line_number = 1
    start = None
    for line in code:
        line_length = len(line)
        if line[0] == '\t':
            errors.append('Use spaces instead of tabs')
        if line[0] == ' ':
            space_count = 1
            for symbol in line:
                if symbol == ' ':
                    space_count += 1
                else:
                    break
            if space_count % 4 != 0:
                errors.append('Indentation is not a multiple of four')
        words = line.split(' ')
        if words[0] == 'class':
            if not words[1].istitle() or words[1].find('_') != -1:
                errors.append(str(line_number) + ':7 ' 'Wrong name of class')
        elif words[0] == 'def':
            if words[1].isupper():
                errors.append(
                    str(line_number) + ':5 ' + 'Wrong name of function')
        elif words[0] == 'import':
            if words[1].isupper():
                errors.append(
                    str(line_number) + ':8 ' + 'Wrong name of module')
            if words[1].find(',') != -1:
                errors.append('Every import should be on a separate line')
        if line.endswith(':'):
            start = '    '
        else:
            start = None
        if line_length > 79:
            errors.append(str(len) + ': Many symbols!')
        line_number += 1
        previous_line = line
last_line = previous_line
if last_line != '\n':
    errors.append('No new line in the end of file')
for error in errors:
    print(error)
