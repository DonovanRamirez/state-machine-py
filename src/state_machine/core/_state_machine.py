# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ._condition import Condition
from typing import (
    cast,
    List,
    Dict,
    Collection,
    Any
)
from . import (State, Condition)
from ..errors import (
    ExpectedStateError,
    ExpectedConditionError,
    StateAlreadyExistsError,
    StateNotFoundError,
    TransitionAlreadyExistsError,
    TransitionNotFoundError,
    InitialStateNotSetError,
    StateMachineFrozenError,
    StateMachineNotFrozenError,
    FinalStateNotFoundError
)



class StateMachine:
    def __init__(self) -> None:
        self.__transitions = {}
        self.__initial_state: State | None = None
        self.__final_state: set[State] = set()
        self.__current_state: State | None = None
        self.__is_frozen = False
        self.__requieres_final_state = False

    
    def __str__(self) -> str:
        output = ""
        for s in self.transitions:
            row = f"{s}"
            info = []
            if s is self.initial_state:
                info.append("Initial")

            if s in self.final_state:
                info.append("Final")

            if s is self.current_state:
                info.append("Current")

            if info:
                row = f"[{', '.join(info)}] {row}"

            row += "\n"

            for c in self.transitions[s]:
                row += f" ├─{c} ─> {self.transitions[s][c]}\n"
            
            output += row

        if self.current_state is None:
            output += "StateMachine NOT STARTED"

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

    
    def __validate_collection(self, collec_objt: Collection[Any]) -> None:
        '''
        Raise an error if objecto is not a Collection type
        '''
        if not isinstance(collec_objt, Collection):
            raise TypeError(f"Object must be a `Collection`, but got {type(collec_objt)}")
    

    def __validate_empty_collection(self, collec_obj: Collection[Any]) -> None:
        '''
        Raise an error if collection is empty
        '''
        self.__validate_collection(collec_obj)

        if len(collec_obj) == 0:
            raise ValueError(f"Collection ({type(collec_obj).__name__}) cannot be empty")


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


    def __validate_existing_initial_state(self) -> None:
        '''
        Raise an error if `initial_state` has not been set
        '''
        if not self.__has_initial_state():
            raise InitialStateNotSetError(
                "`initial_state` has not been set"
            )

    
    def __validate_is_frozen(self) -> None:
        '''
        Raise an error if `StateMachine` is frozen.
        '''
        if self.__is_frozen:
            raise StateMachineFrozenError(
                "`StateMachine` is frozen, you cannot modify `StateMachine` while is frozen. \
                Use `StateMachine.unfreeze()` to unfrozen `StateMachine"
            )
    

    def __validate_is_not_frozen(self) -> None:
        '''
        Raise an error if `StateMachine` is not frozen
        '''
        if not self.__is_frozen:
            raise StateMachineNotFrozenError(
                "`StateMachine` is not frozen, you can not execute `StateMachine` while is not frozen. \
                Use `StateMachine.freeze()` to execute `StateMachine`"
            )

    
    def __validate_is_requiered_final_state(self) -> None:
        '''
        Raise an error if `requieres_final_state` is True and lenght of `final_state`is 0
        '''
        if self.__requieres_final_state and len(self.final_state):
            raise FinalStateNotFoundError("`final_state` not found in `StateMachine`")
        

    def __has_state(self, state: State) -> bool:
        return state in self.__transitions or \
            (self.__search_state(state.name) is not None)

    
    def __has_transition(self, from_state: State, condition: Condition) -> bool:
        return condition in self.__transitions[from_state]


    def __has_initial_state(self) -> bool:
        return self.__initial_state is not None


    def __has_current_state(self) -> bool:
        return self.__current_state is not None


    def __search_state(self, name: str) -> State | None:
        for s in self.transitions:
            if s.name == name:
                return s


    def __search_condition(self, name: str) -> Condition | None:
        for s in self.transitions:
            for c in self.transitions[s]:
                if c.name == name:
                    return c

    
    def __restart_final_state(self) -> None:
        self.__final_state = set()


    @property
    def states(self) -> List[State]:
        return list(self.__transitions.keys())


    @property
    def transitions(self) -> Dict[State, Dict[Condition, State]]:
        return self.__transitions


    @property
    def initial_state(self) -> State | None:
        return self.__initial_state


    @property
    def final_state(self) -> set[State]:
        return self.__final_state


    @property
    def current_state(self) -> State | None:
        return self.__current_state

    
    @property
    def is_frozen(self) -> bool:
        return self.__is_frozen

    
    @property
    def requieres_final_state(self) -> bool:
        return self.__requieres_final_state


    @requieres_final_state.setter
    def requieres_final_state(self, c: bool) -> None:
        if not isinstance(c, bool):
            raise ValueError(f"`requiereS_final_state` can only be boolean, but got {type(c)}")
        self.__requieres_final_state = c
        

    def add_state(self, state: State | Collection[State]) -> None:
        """
        Add one or multiples States to StateMachine.

        Parameters
        ----------
        state : State | Collection[State]
            State to add

        Raises
        ------
        ExpectedStateError:
            Object to add is not State

        StateMachineFrozenError:
            Try to modify the StateMachine when it's frozen
        
        TypeError:
            Object is not a Collection

        ValueError:
            Collection is empty
        """
        self.__validate_is_frozen()

        if not isinstance(state, Collection):
            state = [state]

        self.__validate_empty_collection(state)
        
        for s in state:
            self.__validate_new_state(s)

        for s in state:
            self.__transitions[s] = {}

    
    def remove_state(self, state: State | Collection[State]) -> None:
        """
        Remove one or multiples States from StateMachine and all its transitions.

        Parameters
        ----------
        state : State | Collection[State]
            State to remove

        Raises
        ------
        ExpectedStateError:
            Object is not State

        StateNotFoundError:
            State does not exist in StateMachine

        TypeError:
            Object is not a Collection

        ValueError:
            Collection is empty
        """
        self.__validate_is_frozen()

        if not isinstance(state, Collection):
            state = [state]
        
        self.__validate_empty_collection(state)
        
        for s in state:
            self.__validate_existing_state(s)

        for s in state:
            del self.__transitions[s]


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
        self.__validate_is_frozen()
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
        self.__validate_is_frozen()
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

        StateMachineFrozenError:
            Try to modify the StateMachine when it's frozen
        """
        self.__validate_is_frozen()
        self.__validate_existing_state(state)

        self.__initial_state = state

    
    def set_final_state(self, state: State | Collection[State]) -> None:
        """
        Set final state in StateMachine.

        Parameters
        ----------
        state : State | Collection[State]
            State to be final.

        Raises
        ------
        ExpectedStateError:
            Object is not State

        StateNotFoundError:
            State does not exist in StateMachine

        InitialStateAlreadySetError:
            `initial_state` already set
        """
        self.__validate_is_frozen()
        self.__restart_final_state()

        if isinstance(state, State):
            state = [state]
        
        self.__validate_empty_collection(state)

        for s in state:
            self.__validate_existing_state(s)
        
        for s in state:
            self.__final_state.add(s)


    def freeze(self) -> None:
        """
        Freeze the `StateMachine` and make it ready to use 
        (for example moving between states with `StateMachine.move`).

        WARNING
        -------
        Once frozen, the `StateMachine` cannot be modified.
        The only way to revert this is using `StateMachine.unfreeze()`

        Raises
        ------
        FinalStateNotFoundError:
            `final_state` not defined yet or is empty

        InitialStateNotSetError:
            `initial_state` has not been set
        """
        self.__validate_is_requiered_final_state()
        self.__validate_existing_initial_state()
        self.__is_frozen = True
        self.__current_state = self.__current_state if self.__has_current_state() else self.initial_state

    
    def unfreeze(self) -> None:
        """
        Unfreeze `StateMachine` to make it editable (for example,
        adding o removing states with `StateMachine.add` and
        `StatesMachine.remove`)

        WARNING
        -------
        Once unfrozen, the `StateMachine` cannot use to operate.
        The only way to revert this is using `StateMachine.freeze()`
        """
        self.__is_frozen = False


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

        StateMachineNotFrozenError:
            Cannot use `.move` while StateMachine is not frozen
        """
        self.__validate_is_not_frozen()
        self.__validate_condition(condition)
        self.__validate_existing_transition(cast(State, self.current_state), condition)

        self.__current_state = self.transitions[cast(State, self.current_state)][condition]


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