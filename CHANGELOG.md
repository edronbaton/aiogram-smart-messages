# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-01-03

### Added
- **NotificatorService**: New high-level service for sending notifications to users
  - `notify_message()` method for text and smart message notifications
  - `notify_document()` method for sending document files
  - Full integration with SmartMessageRenderer
  - Automatic error logging
  - Type-safe API with comprehensive documentation

### Changed
- Created main `__init__.py` file for package-level exports
- Updated README.md with NotificatorService documentation and examples
- Added NotificatorService to Quick Start guide
- Reorganized README sections to accommodate new feature

### Documentation
- Added comprehensive docstrings to NotificatorService
- Created example usage script (`example_notificator.py`)
- Updated API Reference section in README
- Added use cases and benefits for NotificatorService

## [0.2.0] - Previous Release

### Features
- SmartMessageRenderer for JSON-based message templates
- MessageEngine for core message operations
- KeyboardBuilder for inline and reply keyboards
- MessageEngineMiddleware for automatic engine injection
- Error handling decorators
- Multi-language support
- Context formatting
- Smart message operations (send, edit, reply)

## [0.1.0] - Initial Release

### Added
- Basic message rendering functionality
- JSON template support
- Keyboard builder utilities
