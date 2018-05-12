import validator
NAME_STYLES = ['mixedCase',
               'UPPERCASE',
               'CapitalizedWords',
               'UPPERCASE_WITH_UNDERSCORES',
               'Capitalized_Words_With_Underscores',
               'lower_case_with_underscores',
               'lowercase']


class TestSearch():
    def test_of_indentation(self):
        assert validator.search_errors(' a = 1')[0].err_code == 'E0101'

    def test_imports(self):
        assert validator.search_errors('import sys, os')[0].\
                   err_code == 'E0301'

    def test_function_names(self):
        for i in range(5):
            assert validator.search_errors('def '+NAME_STYLES[i])[0].\
                 err_code == 'E0202'
        for i in range(5, 7):
            err = validator.search_errors('def '+NAME_STYLES[i])
            assert len(err) == 0

    def test_class_names(self):
        correct_names_index = (1, 2)
        for i in range(len(NAME_STYLES)):
            err = validator.search_errors('class '+NAME_STYLES[i])
            if i in correct_names_index:
                assert len(err) == 0
            else:
                assert err[0].err_code == 'E0201'

    def test_import_names(self):
        correct_names_index = (5, 6)
        for i in range(len(NAME_STYLES)):
            err = validator.search_errors('import '+NAME_STYLES[i])
            if i in correct_names_index:
                assert len(err) == 0
            else:
                assert err[0].err_code == 'E0203'

    def test_spaces_around_parameter(self):
        assert validator.search_errors('def complex(real, imag = 0.0):')[0].\
                   err_code == 'E0713'

    def test_long_line(self):
        assert validator.search_errors("It's vvvvveeeeeeeeeeee"
                                       "eeeeeeeeeeeeeeeeeeeeee"
                                       "rrrrrrrrrrrryyyyyyyyyy"
                                       "looooooo000000ong line")[0].\
                   err_code == 'E0601'

    def test_spaces_around_brackets(self):
        code_end = ['01', '04', '06', '07', '09', '03']
        errors = validator.search_errors('spam( ham[ 1 ], { eggs=2 } )')
        for i in range(len(code_end)):
            assert errors[i].err_code == 'E07{}'.format(code_end[i])
        assert len(code_end) == len(errors)

    def test_spaces_before_punctuation(self):
        assert validator.search_errors('if x == 4 :')[0].err_code == 'E0711'
        assert validator.search_errors('x , y = 1, 2')[0].err_code == 'E0710'
        assert validator.search_errors('print(x, y) ;')[0].err_code == 'E0712'

    def test_multiple_statements(self):
        assert validator.search_errors('if foo == "b": do_b_thing()')[0].\
                   err_code == 'E0302'
        assert validator.search_errors('do_one(); do_two(); do_three()')[0].\
                   err_code == 'E0302'

    def test_comments(self):
        assert validator.search_errors('#Comments')[0].err_code == 'E0401'

    def test_logical_conditions(self):
        strings = ['if greeting == True:',
                   'if greeting == False:',
                   'if condition is True:',
                   'if condition is not True:',
                   'if condition is False:',
                   'if condition is not False']
        for line in strings:
            assert validator.search_errors(line)[0].err_code == 'E0501'

    def test_non_using_lambda(self):
        string = 'f = lambda x: 2*x'
        assert validator.search_errors(string)[0].err_code == 'E0801'
