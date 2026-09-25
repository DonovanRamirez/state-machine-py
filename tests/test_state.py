from state_machine import State
import pytest



class Foo1(str): pass
class Foo2: pass


@pytest.mark.parametrize(
    "name, expected_name",
    [
        pytest.param("test", "test", id="basic-name-test"),
        pytest.param(" test", "test", id="del-space-name-test"),
        pytest.param(" test ", "test", id="del-spaces-name-test"),
        pytest.param(" test!1", "test!1", id="del-space-special-char-name-test"),
        pytest.param("tes t@", "tes t@", id="del-space-special-char-name-test-2"),
        pytest.param("TEST", "TEST", id="mayus-name-test"),
        pytest.param(Foo1("TEST"), "TEST", id="class-str-name-test")
    ]
)
def test_create_state(name, expected_name) -> None:
    assert State(name).name == expected_name


@pytest.mark.parametrize(
    "name, expected_error",
    [
        pytest.param(123, TypeError),
        pytest.param(1.0, TypeError),
        pytest.param(lambda x: x, TypeError),
        pytest.param([1, 2], TypeError),
        pytest.param((1, 2), TypeError),
        pytest.param(Foo2(), TypeError),
        pytest.param(Foo1(), ValueError),
        pytest.param("", ValueError)
    ], 
)
def test_invalid_names(name, expected_error) -> None:
    with pytest.raises(expected_error) as error:
        State(name)
