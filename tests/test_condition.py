# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from state_machine import Condition
import pytest



class Foo1(str): pass
class Foo2: pass


@pytest.mark.parametrize(
    "name, expected_name",
    [
        pytest.param("test", "test", id="basic-condition-test"),
        pytest.param(" test", "test", id="del-space-condition-test"),
        pytest.param(" test ", "test", id="del-spaces-condition-test"),
        pytest.param(" test!1", "test!1", id="del-space-special-char-condition-test"),
        pytest.param("tes t@", "tes t@", id="del-space-special-char-condition-test-2"),
        pytest.param("TEST", "TEST", id="mayus-condition-test"),
        pytest.param(Foo1("TEST"), "TEST", id="class-str-condition-test")
    ]
)
def test_create_condition(name, expected_name) -> None:
    assert Condition(name).name == expected_name


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
def test_invalid_conditions(name, expected_error) -> None:
    with pytest.raises(expected_error) as error:
        Condition(name)
