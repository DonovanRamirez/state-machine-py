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
            raise ValueError(f"`name` must be str, but got {type(name)}")
    

    def __validate_state(self, state: State) -> None:
        '''
        Raise a error if `state` is not a State class
        '''
        if not isinstance(state, State):
            raise ExpectedStateError(f"`state` must be State, but got {type(state)}")

    
    def __validate_condition(self, condition: Condition) -> None:
        '''
        Raise a error if `condition` is not a Condition class
        '''
        if not isinstance(condition, Condition):
            raise ExpectedConditionError(f"`condition` must be Condition, but got {type(condition)}")


    def __validate_new_state(self, state: State) -> None:
        '''
        Raise a error if `state` already exist
        '''
        self.__validate_state(state)

        if self.__has_state(state):
            raise StateAlreadyExistsError(f"{state} already exist in StateMachine")

    
    def __validate_existing_state(self, state: State) -> None:
        '''
        Raise a error if `state` does not exist
        '''
        self.__validate_state(state)

        if not self.__has_state(state):
            raise StateNotFoundError(f"{state} does not exist in StateMachine")

    
    def __validate_new_transition(self, from_state: State, condition: Condition) -> None:
        '''
        Raise a error if `trasition` already exist
        '''
        if self.__has_transition(from_state, condition):
            raise \
                TransitionAlreadyExistsError(
                    f"Transition from {from_state} with "
                    f"condition {condition} already exist"
                )

    
    def __validate_existing_transition(self, from_state: State, condition: Condition) -> None:
        '''
        Raise a error if `trasition` does not exist
        '''
        if not self.__has_transition(from_state, condition):
            raise \
            TransitionNotFoundError(
                f"Transition from {from_state} with condition "
                f"{condition} does not exist in StateMachine"
            )

    
    def __validate_new_initial_state(self) -> None:
        '''
        Raise a error if `initial_state` has already been set
        '''
        if self.__has_initial_state():
            raise InitialStateAlreadySetError(
                "`initial_state` has already been set"
            )


    def __validate_existing_initial_state(self) -> None:
        '''
        Raise a error if `initial_state` has not been set
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
        self.__validate_new_state(state)

        self.__transitions[state] = {}

    
    def remove_state(self, state: State) -> None:
        self.__validate_existing_state(state)

        del self.__transitions[state]


    def add_transition(self, from_state: State, to_state: State, condition: Condition) -> None:
        self.__validate_existing_state(from_state)
        self.__validate_existing_state(to_state)
        self.__validate_condition(condition)
        self.__validate_new_transition(from_state, condition)

        self.__transitions[from_state][condition] = to_state

    
    def remove_transition(self, from_state: State, condition: Condition) -> None:
        self.__validate_existing_state(from_state)
        self.__validate_condition(condition)
        self.__validate_existing_transition(from_state, condition)

        del self.__transitions[from_state][condition]
    

    def set_initial_state(self, state: State) -> None:
        self.__validate_existing_state(state)
        self.__validate_new_initial_state()

        self.__initial_state = state
        self.__current_state = state


    def move(self, condition: Condition) -> None:
        self.__validate_condition(condition)
        self.__validate_existing_transition(self.current_state, condition)

        self.__current_state = self.transitions[self.current_state][condition]


    def get_state(self, name: str) -> State | None:
        self.__validate_name(name)
        return self.__search_state(name)


    def get_condition(self, name: str) -> Condition | None:
        self.__validate_name(name)
        return self.__search_condition(name)
    

    def has_state(self, name: str) -> bool:
        self.__validate_name(name)
        return self.__search_state(name) is not None


    def has_condition(self, name: str) -> bool:
        self.__validate_name(name)
        return self.__search_condition(name) is not None

    
    def has_transition(self, state: State, condition: Condition) -> bool:
        try:
            self.__validate_existing_transition(state, condition)
            return True
        except TransitionNotFoundError as e:
            return False