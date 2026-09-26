# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations



class State:
    def __init__(self, name: str) -> None:
        """
        State for a StateMachine

        Parameters
        ----------
        name : str
            Name and ID for State.

        Raises
        ------
        TypeError:
            Name is not str

        ValueError:
            Name can not be empty

        Example
        -------
        >>> from state_machine import State
        >>> s = State("example_name")
        >>> s
        State('example_name')
        
        """
        self.__validate_name(name)
        name = name.strip()
        self.__name = name    
    
    
    def __str__(self) -> str:
        return f"State({self.name!r})"


    def __repr__(self) -> str:
        return self.__str__()

    
    def __validate_name(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError(f"`name` must be str, but got {type(name)}")

        if len(name) == 0:
            raise ValueError(f"`name` cannot be empty")

    
    @property
    def name(self) -> str:
        return self.__name