# -*- coding: utf-8 -*-
"""
aiogram-smart-messages
~~~~~~~~~~~~~~~~~~~~~~

Smart message renderer for Aiogram with keyboard builder and JSON loader.

This library provides high-level abstractions for building sophisticated
Telegram bots with JSON-based message templates, dynamic keyboards, and
robust error handling.

Main components:
    - SmartMessageRenderer: Main class for rendering and sending messages
    - MessageEngine: Core engine for message operations
    - NotificatorService: High-level service for user notifications
    - KeyboardBuilder: Utility for building keyboards
    - MessageEngineMiddleware: Middleware for automatic engine injection
    - Decorators: Error handling and retry decorators
    - Logger: Logging utilities

Basic usage:
    >>> from aiogram import Bot
    >>> from aiogram_smart_messages import (
    ...     SmartMessageRenderer,
    ...     MessageEngine,
    ...     NotificatorService
    ... )
    >>>
    >>> bot = Bot(token="YOUR_BOT_TOKEN")
    >>> engine = MessageEngine(bot)
    >>>
    >>> # Using SmartMessageRenderer
    >>> await SmartMessageRenderer.send(
    ...     engine=engine,
    ...     source=message,
    ...     role="user",
    ...     namespace="main",
    ...     menu_file="welcome",
    ...     block_key="greeting",
    ...     lang="en"
    ... )
    >>>
    >>> # Using NotificatorService
    >>> notificator = NotificatorService(user_id=123456789, bot=bot)
    >>> await notificator.notify_message(text="Hello!")

:copyright: (c) 2025 by Kriva
:license: MIT, see LICENSE for more details.
"""

__version__ = "0.3.0"
__author__ = "Kriva"
__license__ = "MIT"

from .message_engine import MessageEngine, SmartMessage
from .renderer import SmartMessageRenderer
from .builder import KeyboardBuilder
from .notificator import NotificatorService
from .middlewares import MessageEngineMiddleware
from .decorators import with_error_logging
from .logger import get_logger
from .loader import load_message_json

__all__ = [
    # Core classes
    "MessageEngine",
    "SmartMessage",
    "SmartMessageRenderer",
    "KeyboardBuilder",
    "NotificatorService",

    # Middleware
    "MessageEngineMiddleware",

    # Utilities
    "load_message_json",
    "with_error_logging",
    "get_logger",

    # Metadata
    "__version__",
    "__author__",
    "__license__",
]
