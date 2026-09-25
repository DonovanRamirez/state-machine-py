from __future__ import annotations



class State:
    def __init__(self, name: str):
        self.__validate_name(name)
        name = name.strip()
        self.__name = name    
    
    
    def __str__(self) -> str:
        return f"State({self.name!r})"


    def __repr__(self):
        return self.__str__()

    
    def __validate_name(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError(f"`name` must be str, but got {type(name)}")

        if len(name) == 0:
            raise ValueError(f"`name` cannot be empty")

    
    @property
    def name(self) -> str:
        return self.__name
    