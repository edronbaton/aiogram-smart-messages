#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example usage of NotificatorService from aiogram-smart-messages library.

This example demonstrates how to use NotificatorService for sending
notifications to users in various scenarios.
"""

import asyncio
from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram_smart_messages import NotificatorService


async def main():
    # Initialize bot (replace with your token)
    bot = Bot(token="YOUR_BOT_TOKEN_HERE")
    user_id = 123456789  # Replace with actual user ID

    # Create notificator instance for specific user
    notificator = NotificatorService(user_id=user_id, bot=bot)

    # Example 1: Simple text notification
    print("Sending simple text notification...")
    await notificator.notify_message(
        text="Hello! This is a simple notification from the bot."
    )

    # Example 2: Smart message notification with JSON template
    print("Sending smart message notification...")
    await notificator.notify_message(
        smart_data={
            "role": "user",
            "namespace": "shop",
            "menu_file": "orders",
            "block_key": "order_complete",
            "lang": "en",
            "context": {
                "order_id": "12345",
                "total": 99.99,
                "items_count": 3
            }
        }
    )

    # Example 3: Document notification
    print("Sending document notification...")
    # Note: You need to have an actual file for this to work
    # doc = FSInputFile("path/to/your/document.pdf")
    # await notificator.notify_document(
    #     document=doc,
    #     caption="Your invoice for order #12345"
    # )

    # Example 4: Batch notifications to multiple users
    print("Sending batch notifications...")
    user_ids = [123456789, 987654321]  # Replace with actual user IDs

    for uid in user_ids:
        user_notificator = NotificatorService(user_id=uid, bot=bot)
        await user_notificator.notify_message(
            text=f"Important update for user {uid}!"
        )
        await asyncio.sleep(0.1)  # Rate limiting

    print("All notifications sent successfully!")

    # Close bot session
    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
