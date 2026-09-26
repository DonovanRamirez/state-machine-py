# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
