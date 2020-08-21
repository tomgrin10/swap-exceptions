from swap_exceptions import swap_exceptions


def test__swap_exceptions__context_manager():
    # Arrange
    mapping = {ValueError: KeyError("AAAA")}
    exc_to_raise = ValueError()
    expected_raised_exc = mapping[type(exc_to_raise)]

    # Act
    raised_exc = None
    try:
        with swap_exceptions(mapping):
            raise exc_to_raise
    except Exception as e:
        raised_exc = e

    # Assert
    assert raised_exc is expected_raised_exc


def test__swap_exceptions__decorator():
    # Arrange
    mapping = {ValueError: KeyError("AAAA")}
    exc_to_raise = ValueError()
    expected_raised_exc = mapping[type(exc_to_raise)]

    @swap_exceptions(mapping)
    def foo():
        raise exc_to_raise

    # Act
    raised_exc = None
    try:
        foo()
    except Exception as e:
        raised_exc = e

    # Assert
    assert raised_exc is expected_raised_exc


def test__swap_exceptions__lambda_exception_target():
    # Arrange
    mapping = {ValueError: lambda e: KeyError(e)}
    exc_to_raise = ValueError()
    expected_raised_exc = mapping[type(exc_to_raise)](exc_to_raise)

    # Act
    raised_exc = None
    try:
        with swap_exceptions(mapping):
            raise exc_to_raise
    except Exception as e:
        raised_exc = e

    # Assert
    assert type(raised_exc) is type(expected_raised_exc)
    assert raised_exc.args == expected_raised_exc.args
