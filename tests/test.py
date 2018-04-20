import validator


class TestSearch():
    def test_of_identation(self):
        code = self.get_list('identation_test.txt')
        answer = validator.search_errors(code)[0].get_description()
        assert answer == 'Indentation is not a multiple of four'

    def test_imports(self):
        code = self.get_list('import_test.txt')
        answer = validator.search_errors(code)[0].get_description()
        assert answer == 'Every import should be on a separate line'

    def test_function_names(self):
        code = self.get_list('test_function_name')
        answer = validator.search_errors(code)
        for i in range(2):
            assert answer[i].get_description() == 'Wrong name of function'
        assert len(answer) == 2

    def test_class_names(self):
        code = self.get_list('test_class_name')
        answer = validator.search_errors(code)
        for i in range(3):
            assert answer[i].get_description() == 'Wrong name of class'
        assert len(answer) == 3

    def test_spaces_around_parameter(self):
        code = self.get_list('test_spaces_around_parameter')
        answer = validator.search_errors(code)[0].get_description()
        assert answer == 'Unexpected spaces around keyword / parameter equals'

    def test_long_line(self):
        code = self.get_list('long_line')
        answer = validator.search_errors(code)
        for i in range(2):
            assert answer[i].\
                       get_description() == 'Symbols in line over than 79'
        assert len(answer) == 2

    def test_spaces_around_brackets(self):
        code = self.get_list('test_spaces_around_brackets')
        answer = validator.search_errors(code)
        descriptions = []
        for error in answer:
            descriptions.append(error.get_description())
        assert descriptions[0] == 'whitespace after ('
        assert descriptions[1] == 'whitespace after ['
        assert descriptions[2] == 'whitespace before ]'
        assert descriptions[3] == 'whitespace after {'
        assert descriptions[4] == 'whitespace before }'
        assert descriptions[5] == 'whitespace before )'

    def test_spaces_before_punctuation(self):
        code = self.get_list('test_spaces_before_punctuation')
        answer = validator.search_errors(code)
        descriptions = []
        for error in answer:
            descriptions.append(error.get_description())
        assert descriptions[0] == 'whitespace before :'
        assert descriptions[1] == 'whitespace before ,'
        assert descriptions[2] == 'whitespace before ;'

    def test_multiple_statements(self):
        code = self.get_list('multiple_statements')
        answer = validator.search_errors(code)
        for i in range(2):
            assert answer[i].\
                       get_description() == 'multiple statements on one line'
        assert len(answer) == 2

    def test_comments(self):
        code = self.get_list('comments')
        answer = validator.search_errors(code)
        for i in range(2):
            assert answer[i].\
                get_description() == 'inline comment should start with "# "'
        assert len(answer) == 2

    def test_logical_conditions(self):
        code = self.get_list('logical_conditions')
        answer = validator.search_errors(code)
        for i in range(6):
            assert answer[i].\
                get_description() == 'Do not compare logical types through operators "==", "!=", "is", "is not"'
        assert len(answer) == 6

    def get_list(self, file):
        code = []
        with open(file) as content:
            for line in content:
                code.append(line)
        return code