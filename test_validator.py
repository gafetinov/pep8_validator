from validator import Validator
NAME_STYLES = ['mixedCase',
               'UPPERCASE',
               'CapitalizedWords',
               'UPPERCASE_WITH_UNDERSCORES',
               'Capitalized_Words_With_Underscores',
               'lower_case_with_underscores',
               'lowercase']


class TestSearch():
    def test_of_indentation(self):
        checker = Validator(' a = 1')
        checker.search_errors()
        assert len(checker.errors_found) == 1
        assert checker.errors_found[0].err_code == 'E0101'

    def test_imports(self):
        checker = Validator('import sys, os')
        checker.search_errors()
        assert len(checker.errors_found) == 1
        assert checker.errors_found[0].err_code == 'E0301'

    def test_function_names(self):
        for i in range(5):
            checker = Validator('def '+NAME_STYLES[i])
            checker.search_errors()
            assert len(checker.errors_found) == 1
            assert checker.errors_found[0].err_code == 'E0202'
        for i in range(5, 7):
            checker = Validator('def ' + NAME_STYLES[i])
            checker.search_errors()
            assert len(checker.errors_found) == 0

    def test_class_names(self):
        correct_names_index = (1, 2)
        for i in range(len(NAME_STYLES)):
            checker = Validator('class '+NAME_STYLES[i])
            checker.search_errors()
            if i in correct_names_index:
                assert len(checker.errors_found) == 0
            else:
                assert len(checker.errors_found) == 1
                assert checker.errors_found[0].err_code == 'E0201'

    def test_import_names(self):
        correct_names_index = (5, 6)
        for i in range(len(NAME_STYLES)):
            checker = Validator('import '+NAME_STYLES[i])
            checker.search_errors()
            if i in correct_names_index:
                assert len(checker.errors_found) == 0
            else:
                assert len(checker.errors_found) == 1
                assert checker.errors_found[0].err_code == 'E0203'

    def test_spaces_around_parameter(self):
        checker = Validator('def complex(real, image = 0.0):')
        checker.search_errors()
        assert len(checker.errors_found) == 2
        for i in range(2):
            assert checker.errors_found[i].err_code == 'E0705'

    def test_long_line(self):
        checker = Validator("It's vvvvveeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
                            "rrrrrrrrrrrryyyyyyyyyylooooooo000000ong line")
        checker.search_errors()
        assert len(checker.errors_found) == 1
        assert checker.errors_found[0].err_code == 'E0601'

    def test_spaces_around_brackets(self):
        code_end = ['01', '01', '03', '01', '03', '03']
        checker = Validator('spam( ham[ 1 ], { eggs=2 } )')
        checker.search_errors()
        for i in range(len(code_end)):
            assert checker.errors_found[i].\
                       err_code == 'E07{}'.format(code_end[i])
        assert len(code_end) == len(checker.errors_found)

    def test_spaces_before_punctuation(self):
        checker = Validator('if x == 4 :')
        checker.search_errors()
        assert checker.errors_found[0].err_code == 'E0704'
        checker = Validator('x , y = 1, 2')
        checker.search_errors()
        assert checker.errors_found[0].err_code == 'E0704'
        checker = Validator('print(x, y) ;')
        checker.search_errors()
        assert checker.errors_found[0].err_code == 'E0704'

    def test_multiple_statements(self):
        checker = Validator('if foo == "b": do_b_thing()')
        checker.search_errors()
        assert checker.errors_found[0].err_code == 'E0302'
        checker = Validator('do_one(); do_two(); do_three()')
        checker.search_errors()
        assert checker.errors_found[0].err_code == 'E0302'

    def test_comments(self):
        checker = Validator('#Comments')
        checker.search_errors()
        assert checker.errors_found[0].err_code == 'E0401'

    def test_logical_conditions(self):
        strings = ['if greeting == True:',
                   'if greeting == False:',
                   'if condition is True:',
                   'if condition is not True:',
                   'if condition is False:',
                   'if condition is not False']
        for line in strings:
            checker = Validator(line)
            checker.search_errors()
            assert checker.errors_found[0].err_code == 'E0501'

    def test_non_using_lambda(self):
        checker = Validator('f = lambda x: 2*x')
        checker.search_errors()
        assert checker.errors_found[0].err_code == 'E0801'
