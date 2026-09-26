# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from typing import Type


class BaseError(Exception):
    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.args[0]}"

    def __repr__(self) -> str:
        return self.__str__()


def create_error(name: str) -> Type[BaseError]:
    return type(name, (BaseError,), {})


if __name__ == '__main__':
    TestError = create_error("TestError")
    raise TestError("error de ejemplo")
from ._base_error import create_error


ExpectedStateError = create_error('ExpectedStateError')
ExpectedConditionError = create_error('ExpectedConditionError')
StateAlreadyExistsError = create_error('StateAlreadyExistsError')
StateNotFoundError = create_error('StateNotFoundError')
InitialStateAlreadySetError = create_error('InitialStateAlreadySetError')
TransitionAlreadyExistsError = create_error('TransitionAlreadyExistsError')
TransitionNotFoundError = create_error('TransitionNotFoundError')
InitialStateNotSetError = create_error('InitialStateNotSetError')