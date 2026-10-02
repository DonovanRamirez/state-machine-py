# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Documented missing `Raises` entries for `freeze` and `move`.

## [0.2.0] - 2026-09-29

### Added

- Attribute `StateMachine.is_freeze`
- Attribute `StateMachine.final_state`
- Attribute `StateMachine.requires_final_state`
- Method `StateMachine.freeze`
- Method `StateMachine.unfreeze`
- Method `StateMachine.set_final_state`
- Error `StateMachineFrozenError`
- Error `StateMachinenNotFrozenError`
- Error `FinalStateNotFoundError`

### Changed

- `StateMachine.add_state` now supports a `Collection` object.
- `StateMachine.remove_state` now supports a `Collection` object.
- `StateMachine.set_initial_state` now overwrite previus `StateMachine.initial_state` instead of raise an error.
- tests files
- Visual print of `StateMachine`

### Remove

- `InitialStateAlreadySetError`

## [0.1.0] - 2026-09-26

### Added

- Initial release.
- `State` class to represent a state.
- `Condition` class to define transition rules.
- `StateMachine` class to build and manage states, transitions, and the
  current/initial state.
- Custom exception hierarchy in `state_machine.errors`
  (`ExpectedStateError`, `ExpectedConditionError`, `StateAlreadyExistsError`,
  `StateNotFoundError`, `InitialStateAlreadySetError`,
  `TransitionAlreadyExistsError`, `TransitionNotFoundError`,
  `InitialStateNotSetError`).
