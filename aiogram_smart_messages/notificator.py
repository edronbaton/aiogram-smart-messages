# -*- coding: utf-8 -*-
"""
Notificator service for sending notifications to Telegram users.

This module provides a high-level service for sending various types of
notifications to users with support for smart messages and documents.
"""

import logging
from typing import Optional

from aiogram import Bot
from aiogram.types import (
    FSInputFile,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)

from .renderer import SmartMessageRenderer
from .message_engine import MessageEngine
from .decorators import with_error_logging
from .logger import get_logger

logger = get_logger()


class NotificatorService:
    """
    High-level service for sending notifications to Telegram users.

    NotificatorService provides convenient methods for sending messages and documents
    to users. It integrates with SmartMessageRenderer for advanced message handling
    and supports both simple text messages and complex smart messages with keyboards.

    The service handles:
    - Simple text message notifications
    - Smart message notifications with JSON templates
    - Document notifications with captions and keyboards
    - Automatic error logging

    Attributes:
        bot: Aiogram Bot instance used for sending messages.
        engine: MessageEngine instance for message operations.
        user_id: Telegram user ID to send notifications to.

    Example:
        >>> bot = Bot(token="YOUR_BOT_TOKEN")
        >>> notificator = NotificatorService(user_id=123456789, bot=bot)
        >>>
        >>> # Send simple text message
        >>> await notificator.notify_message(text="Hello, user!")
        >>>
        >>> # Send smart message
        >>> await notificator.notify_message(
        ...     smart_data={
        ...         "role": "user",
        ...         "namespace": "main",
        ...         "menu_file": "welcome",
        ...         "block_key": "greeting",
        ...         "lang": "en"
        ...     }
        ... )
    """

    def __init__(self, user_id: int, bot: Bot) -> None:
        """
        Initialize NotificatorService with user ID and bot instance.

        Args:
            user_id: Telegram user ID to send notifications to.
            bot: Aiogram Bot instance for sending messages.
        """
        self.bot: Bot = bot
        self.engine: MessageEngine = MessageEngine(self.bot)
        self.user_id: int = user_id

    @with_error_logging(logger=logger, error_label="NOTIFY_MESSAGE")
    async def notify_message(
        self,
        text: Optional[str] = None,
        smart_data: Optional[dict] = None
    ) -> None:
        """
        Send a notification message to the user.

        This method supports two modes:
        1. Simple text message: Pass text parameter
        2. Smart message: Pass smart_data dict with SmartMessageRenderer parameters

        Smart message mode uses SmartMessageRenderer.send() under the hood and
        supports all its features: JSON templates, keyboards, photos, etc.

        Args:
            text: Plain text message to send. Used if smart_data is not provided.
            smart_data: Dictionary of parameters for SmartMessageRenderer.send().
                       Should contain keys like: role, namespace, menu_file,
                       block_key, lang, context, etc.

        Returns:
            None

        Raises:
            ValueError: If neither text nor smart_data is provided.
            TelegramBadRequest: On Telegram API errors.

        Example:
            >>> # Simple text notification
            >>> await notificator.notify_message(
            ...     text="Your order has been processed"
            ... )
            >>>
            >>> # Smart message notification
            >>> await notificator.notify_message(
            ...     smart_data={
            ...         "role": "user",
            ...         "namespace": "shop",
            ...         "menu_file": "orders",
            ...         "block_key": "order_complete",
            ...         "lang": "en",
            ...         "context": {"order_id": "12345"}
            ...     }
            ... )

        Note:
            - If both text and smart_data are provided, smart_data takes precedence
            - Smart messages support all SmartMessageRenderer features
            - Errors are automatically logged with NOTIFY_MESSAGE label
        """
        if smart_data:
            await SmartMessageRenderer.send(
                engine=self.engine,
                source=self.user_id,
                **smart_data
            )
            logger.info(f"Smart message sent to user {self.user_id}")
            return

        if text:
            await self.bot.send_message(
                chat_id=self.user_id,
                text=text
            )
            logger.info(f"Simple message sent to user {self.user_id}")

    @with_error_logging(logger=logger, error_label="NOTIFY_DOCUMENT")
    async def notify_document(
        self,
        document: FSInputFile,
        caption: str = "",
        custom_markup: Optional[InlineKeyboardMarkup | ReplyKeyboardMarkup] = None,
    ) -> None:
        """
        Send a document notification to the user.

        Sends a document file to the user with optional caption and keyboard.
        Uses SmartMessageRenderer.send_document() for enhanced functionality.

        Args:
            document: FSInputFile object containing the document to send.
                     Can be any file type (PDF, DOCX, images, etc.).
            caption: Optional caption text for the document. Defaults to empty string.
            custom_markup: Optional keyboard markup (inline or reply) to attach
                          to the document message.

        Returns:
            None

        Raises:
            TelegramBadRequest: On Telegram API errors (file too large, etc.).
            FileNotFoundError: If document file doesn't exist.

        Example:
            >>> from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
            >>>
            >>> # Simple document
            >>> doc = FSInputFile("report.pdf")
            >>> await notificator.notify_document(
            ...     document=doc,
            ...     caption="Your monthly report"
            ... )
            >>>
            >>> # Document with keyboard
            >>> keyboard = InlineKeyboardMarkup(inline_keyboard=[
            ...     [InlineKeyboardButton(text="View Details", callback_data="details")]
            ... ])
            >>> await notificator.notify_document(
            ...     document=FSInputFile("invoice.pdf"),
            ...     caption="Invoice #12345",
            ...     custom_markup=keyboard
            ... )

        Note:
            - Maximum file size: 50 MB for bots
            - All file types are supported
            - Document preserves original filename
            - Errors are automatically logged with NOTIFY_DOCUMENT label
        """
        await SmartMessageRenderer.send_document(
            engine=self.engine,
            source=self.user_id,
            document=document,
            caption=caption,
            custom_markup=custom_markup,
        )

        logger.info(f"Document sent to user {self.user_id}")
