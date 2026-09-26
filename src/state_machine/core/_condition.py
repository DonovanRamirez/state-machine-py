# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations



class Condition:
    __slots__ = ("__name", )

    def __init__(self, name: str) -> None:
        """
        Condition to make a transition between 2 states.

        Parameters
        ----------
        name : str
            Name and ID for Condition.

        Raises
        ------
        TypeError:
            Name is not str

        ValueError:
            Name can not be empty

        Example
        -------
        >>> from state_machine import StateMachine, State, Condition
        >>> s1 = State("s1")
        >>> s2 = State("s2")
        >>> c1 = Condition("condition1")
        >>> sm = StateMachine()
        >>> sm.add_state(s1)
        >>> sm.add_state(s2)
        >>> sm.add_transition(s1, s2, c1)
        >>> sm.set_initial_state(s1)
        >>> sm
        State('s1')*
        ├─Condition('condition1') ─> State('s2')
        State('s2')
        """
        self.__validate_name(name=name)
        name = name.strip()
        self.__name = name


    def __eq__(self, other: Condition) -> bool:
        if not isinstance(other, Condition):
            raise TypeError(
                f"Condition can only be compared with Condition, but got {type(other)}"
            )

        return self.__name == other.__name


    def __hash__(self) -> int:
        return hash(self.__name)


    def __str__(self) -> str:
        return f"Condition({self.__name!r})"


    def __repr__(self) -> str:
        return f"Condition({self.__name!r})"

    
    def __validate_name(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError(f"`name` must be str, but got {type(name)}")

        if len(name) == 0:
            raise ValueError(f"`name` cannot be empty")
    

    @property
    def name(self) -> str:
        return self.__name
