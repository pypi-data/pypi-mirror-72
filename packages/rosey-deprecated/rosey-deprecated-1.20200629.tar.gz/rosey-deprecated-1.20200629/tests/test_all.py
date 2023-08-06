import pytest
from rosey_deprecated import DeprecatedError, Deprecated, deprecated


@Deprecated('This is just an error message')
class ClassIsDeprecated:
    def __init__(self, *args):
        print(*args)


def test_deprecate_function():
    with pytest.raises(DeprecatedError):
        new_print = deprecated(print)
        new_print('This should fail!')


def test_deprecated_class():
    with pytest.warns(DeprecationWarning):
        new_print = ClassIsDeprecated('this should warn!')
