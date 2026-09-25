from __future__ import annotations



class Condition:
    __slots__ = ("__name", )

    def __init__(self, name: str) -> None:
        self.__validate_name(name=name)
        name = name.strip()
        self.__name = name


    def __eq__(self, other: Condition) -> bool:
        if not isinstance(other, Condition):
            raise TypeError(
                f"Condition only can be compared with Restul, but got {type(other)}"
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
