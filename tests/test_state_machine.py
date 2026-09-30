# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from collections.abc import Iterable
import pytest
from state_machine import (
    State,
    Condition,
    StateMachine
)
from state_machine.errors import (
    ExpectedStateError,
    ExpectedConditionError,
    StateAlreadyExistsError,
    StateNotFoundError,
    TransitionAlreadyExistsError
)



class Foo1(str): pass
class Foo2: pass

@pytest.mark.parametrize(
    "name",
    [
        pytest.param("test", id="add-state-test-1"),
        pytest.param(" test", id="add-state-test-2"),
        pytest.param(" test ", id="add-state-test-3"),
        pytest.param(" test!1", id="add-state-test-4"),
        pytest.param("tes t@", id="add-state-test-5"),
        pytest.param("TEST", id="add-state-test-6"),
        pytest.param(["TEST", "TEST2", "TEST3"], id="add-state-test-7")
    ]
)
def test_add_state(name) -> None:
    sm = StateMachine()

    if isinstance(name, str):
        s = State(name)
    else:
        s = [State(i) for i in name]

    sm.add_state(s)

    if isinstance(name, str):
        assert s in sm.transitions
    else:
        for i in s:
            assert i in sm.transitions



@pytest.mark.parametrize(
    "name1, name2, name3",
    [
        pytest.param("test1", "test2", "condition1", id="add-transition-test-1")
    ]
)
def test_add_transition(name1, name2, name3) -> None:
    s1 = State(name1)
    s2 = State(name2)
    c1 = Condition(name3)
    sm = StateMachine()
    sm.add_state(s1)
    sm.add_state(s2)
    sm.add_transition(s1, s2, c1)
    assert c1 in sm.transitions[s1]



@pytest.mark.parametrize(
    "name",
    [
        pytest.param("test", id="remove-state-test-1"),
        pytest.param(" test", id="remove-state-test-2"),
        pytest.param(" test ", id="remove-state-test-3"),
        pytest.param(" test!1", id="remove-state-test-4"),
        pytest.param("tes t@", id="remove-state-test-5"),
        pytest.param("TEST", id="remove-state-test-6")
    ]
)
def test_remove_state(name) -> None:
    s = State(name)
    sm = StateMachine()
    sm.add_state(s)
    sm.remove_state(s)
    assert s not in sm.transitions



@pytest.mark.parametrize(
    "name1, name2, name3",
    [
        pytest.param("test1", "test2", "condition1", id="remove-transition-test-1")
    ]
)
def test_remove_transition(name1, name2, name3) -> None:
    s1 = State(name1)
    s2 = State(name2)
    c1 = Condition(name3)
    sm = StateMachine()
    sm.add_state(s1)
    sm.add_state(s2)
    sm.add_transition(s1, s2, c1)
    sm.remove_transition(s1, c1)
    assert c1 not in sm.transitions[s1]



@pytest.mark.parametrize(
    "states, init_state_idx",
    [
        pytest.param([State("test1"), State("test2"), State("test3")], 2)
    ]
)
def test_set_initial_state(states, init_state_idx) -> None:
    sm = StateMachine()
    for s in states:
        sm.add_state(s)
    sm.set_initial_state(states[init_state_idx])
    assert sm.initial_state is states[init_state_idx]



def test_move() -> None:
    sm = StateMachine()
    s1 = State("test1")
    s2 = State("test2")
    c1 = Condition("condition1")
    sm.add_state(s1)
    sm.add_state(s2)
    sm.add_transition(s1, s2, c1)
    sm.set_initial_state(s1)
    sm.freeze()
    sm.move(c1)
    assert sm.current_state is s2



@pytest.mark.parametrize(
    "names, state_to_search",
    [
        pytest.param(["test1", "test2", "test3"], "test2"),
        pytest.param(["test1", "test2", "test3"], "test4")
    ]
)
def test_get_state(names, state_to_search) -> None:
    sm = StateMachine()
    s2s = None
    for n in names:
        s = State(n)
        if n == state_to_search:
            s2s = s
        sm.add_state(s)
    assert sm.get_state(state_to_search) is s2s



@pytest.mark.parametrize(
    "state_names, condition_names, condition_to_search",
    [
        pytest.param(["test1", "test2", "test3", "test4"], ["condition1", "condition2", "condition3"], "condition2"),
        pytest.param(["test1", "test2", "test3", "test4"], ["condition1", "condition2", "condition3"], "condition4")
    ]
)
def test_get_condition(state_names, condition_names, condition_to_search) -> None:
    sm = StateMachine()
    s2s = None
    for n in state_names:
        sm.add_state(State(n))

    for n1, n2, n3 in zip(sm.states[:-1], sm.states[1:], condition_names):
        c1 = Condition(n3)
        if n3 == condition_to_search:
            s2s = c1
        sm.add_transition(n1, n2, c1)

    assert sm.get_condition(condition_to_search) is s2s



@pytest.mark.parametrize(
    "names, state_to_search",
    [
        pytest.param(["test1", "test2", "test3"], "test2"),
        pytest.param(["test1", "test2", "test3"], "test4")
    ]
)
def test_has_state(names, state_to_search) -> None:
    sm = StateMachine()
    s2s = False
    for n in names:
        s = State(n)
        if n == state_to_search:
            s2s = True
        sm.add_state(s)
    assert sm.has_state(state_to_search) is s2s



@pytest.mark.parametrize(
    "state_names, condition_names, condition_to_search",
    [
        pytest.param(["test1", "test2", "test3", "test4"], ["condition1", "condition2", "condition3"], "condition2"),
        pytest.param(["test1", "test2", "test3", "test4"], ["condition1", "condition2", "condition3"], "condition4")
    ]
)
def test_has_condition(state_names, condition_names, condition_to_search) -> None:
    sm = StateMachine()
    s2s = False
    for n in state_names:
        sm.add_state(State(n))

    for n1, n2, n3 in zip(sm.states[:-1], sm.states[1:], condition_names):
        c1 = Condition(n3)
        if n3 == condition_to_search:
            s2s = True
        sm.add_transition(n1, n2, c1)

    assert sm.has_condition(condition_to_search) is s2s



@pytest.mark.parametrize(
    "names, state_to_initial",
    [
        pytest.param(["test1", "test2", "test3"], "test2")
    ]
)
def test_set_initial_state(names, state_to_initial) -> None:
    sm = StateMachine()
    s2i = None
    for n in names:
        s = State(n)
        if n == state_to_initial:
            s2i = s
        sm.add_state(s)
    sm.set_initial_state(sm.get_state(state_to_initial))
    assert sm.initial_state is s2i



@pytest.mark.parametrize(
    "obj, expected_error",
    [
        pytest.param(123, ExpectedStateError, id="invalid-state-expectederror-1"),
        pytest.param(1.0, ExpectedStateError, id="invalid-state-expectederror-2"),
        pytest.param(lambda x: x, ExpectedStateError, id="invalid-state-expectederror-3"),
        pytest.param([1, 2], ExpectedStateError, id="invalid-state-expectederror-4"),
        pytest.param((1, 2), ExpectedStateError, id="invalid-state-expectederror-5"),
        pytest.param(Foo2(), ExpectedStateError, id="invalid-state-expectederror-6"),
        pytest.param(Foo1(), ValueError, id="invalid-state-expectederror-7"),
        pytest.param("", ValueError, id="invalid-state-expectederror-8"),
        pytest.param(Condition("test"), ExpectedStateError, id="invalid-state-expectederror-9"),
        pytest.param(StateMachine(), ExpectedStateError, id="invalid-state-expectederror-10"),
        pytest.param(ExpectedStateError(), ExpectedStateError, id="invalid-state-expectederror-11"),
        pytest.param(State("test"), StateAlreadyExistsError, id="invalid-state-alreadyexists-1")
    ]
)
def test_invalid_states(obj, expected_error) -> None:
    sm = StateMachine()
    sm.add_state(State("test"))
    with pytest.raises(expected_error) as error:
        sm.add_state(obj)


@pytest.mark.parametrize(
    "states_add, states_delete, expected_error",
    [   
        pytest.param(["test1", "test2", "test3"], "test4", StateNotFoundError),
        pytest.param(["test1", "test2", "test3"], [], ValueError),
        pytest.param(["test1", "test2", "test3"], set(["test4"]), ExpectedStateError),
        pytest.param(["test1", "test2", "test3"], Foo2(), ExpectedStateError)
    ]
)
def test_invalid_ways_to_delete_states(states_add, states_delete, expected_error) -> None:
    sm = StateMachine()
    for i in states_add:
        sm.add_state(State(i))

    with pytest.raises(expected_error) as error:
        if isinstance(states_delete, Iterable) and not isinstance(states_delete, str):
            sm.remove_state(states_delete)

        elif isinstance(states_delete, Iterable) and isinstance(states_delete, str):
            s = State(states_delete)
            sm.remove_state(s)

        else:
            sm.remove_state(states_delete)



@pytest.mark.parametrize(
    "state1, state2, condition, expected_error, test_condition",
    [
        pytest.param(State("test1"), State("test2"), Condition("condition1"), StateNotFoundError, False),
        pytest.param(State("test1"), State("test2"), Condition("condition1"), TransitionAlreadyExistsError, True),
        pytest.param(State("test1"), State("test2"), Foo2(), ExpectedConditionError, True),
        pytest.param(State("test1"), Foo2(), Condition("condition1"), ExpectedStateError, True)
    ]
)
def test_invalid_trasitions(
    state1, 
    state2, 
    condition, 
    expected_error, 
    test_condition
) -> None:
    sm = StateMachine()
    with pytest.raises(expected_error) as error:
        if test_condition:
            sm.add_state(state1)
            sm.add_state(state2)
            sm.add_transition(state1, state2, condition)

        sm.add_transition(state1, state2, condition)



@pytest.mark.parametrize(
    "names, state_to_initial, expected_error, not_exist_initial",
    [
        pytest.param(["test1", "test2", "test3"], "test4", ExpectedStateError, False),
        pytest.param(["test1", "test2", "test3"], "test4", StateNotFoundError, True)
    ]
)
def test_invalid_initial_state(names, state_to_initial, expected_error, not_exist_initial) -> None:
    sm = StateMachine()
    s2i = None
    for n in names:
        s = State(n)
        if n == state_to_initial:
            s2i = s
        sm.add_state(s)

    with pytest.raises(expected_error) as error:
        if not_exist_initial and s2i is None:
            s2i = State(state_to_initial)
        else:
            sm.set_initial_state(s2i)

        sm.set_initial_state(s2i)
