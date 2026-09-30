# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ._base_error import create_error


ExpectedStateError = create_error('ExpectedStateError')
ExpectedConditionError = create_error('ExpectedConditionError')
StateAlreadyExistsError = create_error('StateAlreadyExistsError')
StateNotFoundError = create_error('StateNotFoundError')
TransitionAlreadyExistsError = create_error('TransitionAlreadyExistsError')
TransitionNotFoundError = create_error('TransitionNotFoundError')
InitialStateNotSetError = create_error('InitialStateNotSetError')
StateMachineFrozenError = create_error('StateMachineFrozenError')
StateMachineNotFrozenError = create_error('StateMachinenNotFrozenError')
FinalStateNotFoundError = create_error('FinalStateNotFoundError')