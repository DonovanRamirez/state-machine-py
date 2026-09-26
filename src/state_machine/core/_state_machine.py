# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ._condition import Condition
from typing import (
    List,
    Dict
)
from . import (State, Condition)
from ..errors import (
    ExpectedStateError,
    ExpectedConditionError,
    StateAlreadyExistsError,
    StateNotFoundError,
    InitialStateAlreadySetError,
    TransitionAlreadyExistsError,
    TransitionNotFoundError,
    InitialStateNotSetError
)



class StateMachine:
    def __init__(self) -> None:
        self.__transitions = {}
        self.__initial_state: State | None = None
        self.__current_state: State | None = None

    
    def __str__(self) -> str:
        output = ""
        for s in self.transitions:
            output += f"{s}" + ("*\n" if s is self.current_state else "\n")
            for c in self.transitions[s]:
                output += f" ├─{c} ─> {self.transitions[s][c]}\n"
        return output

    
    def __repr__(self) -> str:
        return self.__str__()


    def __validate_name(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError(f"`name` must be str, but got {type(name)}")
        
        if len(name) == 0:
            raise ValueError(f"`name` cannot be empty")
    

    def __validate_state(self, state: State) -> None:
        '''
        Raise an error if `state` is not a State class
        '''
        if not isinstance(state, State):
            raise ExpectedStateError(f"`state` must be State, but got {type(state)}")

    
    def __validate_condition(self, condition: Condition) -> None:
        '''
        Raise an error if `condition` is not a Condition class
        '''
        if not isinstance(condition, Condition):
            raise ExpectedConditionError(f"`condition` must be Condition, but got {type(condition)}")


    def __validate_new_state(self, state: State) -> None:
        '''
        Raise an error if `state` already exists
        '''
        self.__validate_state(state)

        if self.__has_state(state):
            raise StateAlreadyExistsError(f"{state} already exists in StateMachine")

    
    def __validate_existing_state(self, state: State) -> None:
        '''
        Raise an error if `state` does not exist
        '''
        self.__validate_state(state)

        if not self.__has_state(state):
            raise StateNotFoundError(f"{state} does not exist in StateMachine")

    
    def __validate_new_transition(self, from_state: State, condition: Condition) -> None:
        '''
        Raise an error if the transition already exists
        '''
        if self.__has_transition(from_state, condition):
            raise \
                TransitionAlreadyExistsError(
                    f"Transition from {from_state} with "
                    f"condition {condition} already exists"
                )

    
    def __validate_existing_transition(self, from_state: State, condition: Condition) -> None:
        '''
        Raise an error if the transition does not exist
        '''
        if not self.__has_transition(from_state, condition):
            raise \
            TransitionNotFoundError(
                f"Transition from {from_state} with condition "
                f"{condition} does not exist in StateMachine"
            )

    
    def __validate_new_initial_state(self) -> None:
        '''
        Raise an error if `initial_state` has already been set
        '''
        if self.__has_initial_state():
            raise InitialStateAlreadySetError(
                "`initial_state` has already been set"
            )


    def __validate_existing_initial_state(self) -> None:
        '''
        Raise an error if `initial_state` has not been set
        '''
        if not self.__has_initial_state():
            raise InitialStateNotSetError(
                "`initial_state` has not been set"
            )


    def __has_state(self, state: State) -> bool:
        return state in self.__transitions or \
            (self.__search_state(state.name) is not None)

    
    def __has_transition(self, from_state: State, condition: Condition) -> bool:
        return condition in self.__transitions[from_state]


    def __has_initial_state(self) -> bool:
        return self.__initial_state is not None


    def __search_state(self, name: str) -> State | None:
        for s in self.transitions:
            if s.name == name:
                return s


    def __search_condition(self, name: str) -> Condition | None:
        for s in self.transitions:
            for c in self.transitions[s]:
                if c.name == name:
                    return c


    @property
    def states(self) -> List[State]:
        return list(self.__transitions.keys())


    @property
    def transitions(self) -> Dict[State, Dict[Condition, State]]:
        return self.__transitions


    @property
    def initial_state(self) -> State:
        self.__validate_existing_initial_state()
        return self.__initial_state


    @property
    def current_state(self) -> State:
        self.__validate_existing_initial_state()
        return self.__current_state
        

    def add_state(self, state: State) -> None:
        """
        Add a State to StateMachine.

        Parameters
        ----------
        state : State
            State to add

        Raises
        ------
        ExpectedStateError:
            Object is not State

        StateAlreadyExistsError:
            State already exists in StateMachine
        """
        self.__validate_new_state(state)

        self.__transitions[state] = {}

    
    def remove_state(self, state: State) -> None:
        """
        Remove a State from StateMachine and all its transitions.

        Parameters
        ----------
        state : State
            State to remove

        Raises
        ------
        ExpectedStateError:
            Object is not State

        StateNotFoundError:
            State does not exist in StateMachine
        """
        self.__validate_existing_state(state)

        del self.__transitions[state]


    def add_transition(self, from_state: State, to_state: State, condition: Condition) -> None:
        """
        Create a transition between `from_state` and `to_state` with the condition `condition`.

        Parameters
        ----------
        from_state : State
            State to start transition.
        to_state : State
            State to end transition.
        condition : Condition
            The condition to make the transition.

        Raises
        ------
        ExpectedStateError:
            Object is not State

        StateNotFoundError:
            State does not exist in StateMachine

        ExpectedConditionError:
            Object is not Condition

        TransitionAlreadyExistsError:
            Transition already exists in StateMachine
        """
        self.__validate_existing_state(from_state)
        self.__validate_existing_state(to_state)
        self.__validate_condition(condition)
        self.__validate_new_transition(from_state, condition)

        self.__transitions[from_state][condition] = to_state

    
    def remove_transition(self, from_state: State, condition: Condition) -> None:
        """
        Remove a transition from StateMachine

        Parameters
        ----------
        from_state : State
            State to start transition.
        condition : Condition
            The condition to make the transition.

        Raises
        ------
        ExpectedStateError:
            Object is not State

        StateNotFoundError:
            State does not exist in StateMachine

        ExpectedConditionError:
            Object is not Condition

        TransitionNotFoundError:
            Transition does not exist in StateMachine
        """
        self.__validate_existing_state(from_state)
        self.__validate_condition(condition)
        self.__validate_existing_transition(from_state, condition)

        del self.__transitions[from_state][condition]
    

    def set_initial_state(self, state: State) -> None:
        """
        Set initial state in StateMachine.

        Parameters
        ----------
        state : State
            State to be initial.

        Raises
        ------
        ExpectedStateError:
            Object is not State

        StateNotFoundError:
            State does not exist in StateMachine

        InitialStateAlreadySetError:
            `initial_state` already set
        """
        self.__validate_existing_state(state)
        self.__validate_new_initial_state()

        self.__initial_state = state
        self.__current_state = state


    def move(self, condition: Condition) -> None:
        """
        Move the `current_state` using condition.

        Parameters
        ----------
        condition : Condition
            Condition to move.

        Raises
        ------
        ExpectedConditionError:
            Object is not Condition
        
        TransitionNotFoundError:
            Transition does not exist in StateMachine
        """
        self.__validate_condition(condition)
        self.__validate_existing_transition(self.current_state, condition)

        self.__current_state = self.transitions[self.current_state][condition]


    def get_state(self, name: str) -> State | None:
        """
        Get State by a name.

        Parameters
        ----------
        name : str
            Name to search.

        Returns
        -------
        State | None
            - State: if found a State with the name
            - None: if not exists

        Raises
        ------
        TypeError:
            Name is not str

        ValueError:
            Name can not be empty
        """
        self.__validate_name(name)
        return self.__search_state(name)


    def get_condition(self, name: str) -> Condition | None:
        """
        Get Condition by a name.

        Parameters
        ----------
        name : str
            Name to search.

        Returns
        -------
        Condition | None
            - Condition: if found a Condition with the name
            - None: if not exists

        Raises
        ------
        TypeError:
            Name is not str

        ValueError:
            Name can not be empty
        """
        self.__validate_name(name)
        return self.__search_condition(name)
    

    def has_state(self, name: str) -> bool:
        """
        Check if a State with name `name` exists.

        Parameters
        ----------
        name : str
            Name to search.

        Returns
        -------
        bool
            - True: if found a State with the name
            - False: if not exists

        Raises
        ------
        TypeError:
            Name is not str

        ValueError:
            Name can not be empty
        """
        self.__validate_name(name)
        return self.__search_state(name) is not None


    def has_condition(self, name: str) -> bool:
        """
        Check if a Condition with name `name` exists.

        Parameters
        ----------
        name : str
            Name to search.

        Returns
        -------
        bool
            - True: if found a Condition with the name
            - False: if not exists

        Raises
        ------
        TypeError:
            Name is not str

        ValueError:
            Name can not be empty
        """
        self.__validate_name(name)
        return self.__search_condition(name) is not None

    
    def has_transition(self, state: State, condition: Condition) -> bool:
        """
        Check if exist a transition from `state` with `condition`.

        Parameters
        ----------
        state : State
            State to check

        condition : Condition
            Condition to check

        Returns
        -------
        bool
            - True: if found a transition
            - False: if not exists

        Raises
        ------
        ExpectedStateError:
            Object is not State

        StateNotFoundError:
            State does not exist in StateMachine

        ExpectedConditionError:
            Object is not Condition
        """
        try:
            self.__validate_existing_state(state)
            self.__validate_condition(condition)
            self.__validate_existing_transition(state, condition)
            return True
        except TransitionNotFoundError:
            return False