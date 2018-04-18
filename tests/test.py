import validator
import pytest


class TestValidator:

    def test_type_error(self):
        with pytest.raises(TypeError):
            list(validator.Error((1, 1), 'Indentation is not a multiple of four'))

    def test_identation(self):
        assert [validator.Error((1, 1), 'Indentation is not a multiple of four')] == validator.search_errors(' class Super:\n')
