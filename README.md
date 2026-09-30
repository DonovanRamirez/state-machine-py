# state-machine-py

Classic state machine for Python

## Installation

```bash
git clone https://github.com/DonovanRamirez/state-machine-py.git
cd state-machine-py
python -m pip install .
```

## Quick start

```python
from state_machine import StateMachine, State, Condition

# define state_machine, states and transition condition
sm = StateMachine()
s1 = State("s1")
s2 = State("s2")
c1 = Condition("c1")

# add states and transition from s1 to s2 with condition c1
sm.add_state(s1)
sm.add_state(s2)
sm.add_transition(s1, s2, c1)

# set initial state
sm.set_initial_state(s1)

# print all state_machine
print(sm)
```

## Usage

### Defining states

**Example**

```python
from state_machine import State

s1 = State("state1")
```

**Parameters**
```python
State(name)
```
- `name` (str): Name or ID to State

**Attributes**
- `name` (str, read-only): State name/id

### Defining conditions

The `Condition` object defines the rule that must be satisfied to move between states.

**Example**

```python
from state_machine import Condition

c1 = Condition("condition1")
```

**Parameters**
```python
Condition(name)
```
- `name` (str): Name or ID to Condition

**Attributes**
- `name` (str, read-only): Condition name/id

### Building a StateMachine

#### **Add State to StateMachine**

**Example**

```python
from state_machine import StateMachine, State

sm = StateMachine()
s1 = State("state1")
s2 = State("state2")

sm.add_state(s1)
sm.add_state(s2)
```

**Parameters**

```python
StateMachine.add_state(state)
```
- `state` (`State` | `Collection[State]`): State to add.

#### **Set initial state**

**Example**

```python
from state_machine import StateMachine, State

sm = StateMachine()
s1 = State("state1")
s2 = State("state2")

sm.add_state(s1)
sm.add_state(s2)
sm.set_initial_state(s1)
print(sm)

[Initial] State('s1')
State('s2')
```
**Parameters**

```python
StateMachine.set_initial_state(state)
```
- `state` (`State`): State to be Initial.

#### **Set final state**

**Example**

```python
from state_machine import StateMachine, State

sm = StateMachine()
s1 = State("state1")
s2 = State("state2")

sm.add_state(s1)
sm.add_state(s2)
sm.set_initial_state(s1)
sm.set_final_state(s1)
print(sm)

[Initial] State('s1')
[Final] State('s2')
```

**Parameters**

```python
StateMachine.set_final_state(state)
```
- `state` (`State` | `Collection[State]`): State to be Final.

#### **Defining a transition**

To create a transition between 2 states requires a `Condition` object. 

**Example**

```python
from state_machine import StateMachine, State, Condition

sm = StateMachine()
s1 = State("state1")
s2 = State("state2")
c1 = Condition("condition1")

sm.add_state(s1)
sm.add_state(s2)
sm.add_transition(s1, s2, c1)
```

This is equivalent to:
```python
{
    "state1":
        {"condition1": "state2"}
    "state2":
        None
}
```

**Parameters**

```python
StateMachine.add_transition(from_state, to_state, condition)
```
- `from_state` (`State`): This is where transition starts.
- `to_state` (`State`): End of transition.
- `condition` (`Condition`): The condition for making a transition.


#### **Print StateMachine**


**Example**

```python
from state_machine import StateMachine, State, Condition

sm = StateMachine()
s1 = State("state1")
s2 = State("state2")
s3 = State("state3")
c1 = Condition("condition1")
c2 = Condition("condition2")

sm.add_state([s1, s2, s3])
sm.set_initial_state(s1)
sm.set_final_state([s2, s3])
sm.add_transition(s1, s2, c1)
sm.add_transition(s1, s3, c2)
sm.freeze()
print(sm)
```
```
[Initial, Current] State('state1')
 ├─Condition('condition1') ─> State('state2')
 ├─Condition('condition2') ─> State('state3')
[Final] State('state2')
[Final] State('state3')
```
> [!WARNING]
> To print the StateMachine, `initial_state` must be set first.

#### **Move to next state**

The `move` method attempts to transition the `StateMachine` from `current_state` to another, using the matching `Condition`. To use `move`, you first need to call `StateMachine.freeze`.

**Example**

```python
from state_machine import StateMachine, State, Condition

sm = StateMachine()
s1 = State("state1")
s2 = State("state2")
c1 = Condition("condition1")

sm.add_state(s1)
sm.add_state(s2)
sm.set_initial_state(s1)
sm.add_transition(s1, s2, c1)
sm.freeze()
print(sm)
sm.move(c1)
print(sm)
```
```
# previous to move
[Initial, Current] State('state1')
 ├─Condition('condition1') ─> State('state2')
State('state2')
```
```
# moved
[Initial] State('state1')
 ├─Condition('condition1') ─> State('state2')
[Current] State('state2')
```

**Parameters**

```python
StateMachine.move(condition)
```
- `condition` (`Condition`): The condition that matches an existing transition from the `current_state`.

### Handling errors

**Example**

```python
from state_machine import StateMachine
from state_machine.errors import ExpectedStateError

sm = StateMachine()
try:
    sm.add_state("test")
except ExpectedStateError as error:
    print(error)
```
```
>>> ExpectedStateError: `state` must be State, but got <class 'str'>
```

| Exception | Raised when |
|---|---|
|`ExpectedStateError`| Get an object that is not a `State`|
|`ExpectedConditionError`| Get an object that is not a `Condition`|
|`StateAlreadyExistsError`| Attempting to add a `State` that already exists|
|`StateNotFoundError`| The `State` not exist in the machine|
|`TransitionAlreadyExistsError`| Attempting to create a transition, but it already exists|
|`TransitionNotFoundError`| The `Condition` not exist in the machine|
|`InitialStateNotSetError`| Attempting to call `initial_state`, but has not yet been set|
|`FinalStateNotFoundError`| `StateMachine.requires_final_state` is True and tries to call `final_state`|
|`StateMachineFrozenError`| Attempting to modify `StateMachine` while is frozen|
|`StateMachineNotFrozenError`| Attempting to execute or test `StateMachine` while is not frozen|


## Testing

This project uses [pytest](https://docs.pytest.org/) for testing.

Install the development dependencies and run the test suite:

```bash
git clone https://github.com/DonovanRamirez/state-machine-py.git
cd state-machine-py
python -m pip install -e .
python -m pytest
```

## Contributing

Contributions are welcome. Please open an issue or pull request.

## License

This project is licensed under the MPL-2.0 License — see the [LICENSE](LICENSE) file for details.
