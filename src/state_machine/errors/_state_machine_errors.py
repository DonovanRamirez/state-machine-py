from ._base_error import create_error


ExpectedStateError = create_error('ExpectedStateError')
ExpectedConditionError = create_error('ExpectedConditionError')
StateAlreadyExistsError = create_error('StateAlreadyExistsError')
StateNotFoundError = create_error('StateNotFoundError')
InitialStateAlreadySetError = create_error('InitialStateAlreadySetError')
TransitionAlreadyExistsError = create_error('TransitionAlreadyExistsError')
TransitionNotFoundError = create_error('TransitionNotFoundError')
InitialStateNotSetError = create_error('InitialStateNotSetError')