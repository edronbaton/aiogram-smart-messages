# aiogram-smart-messages

**Smart message renderer for Aiogram** - A powerful toolkit for building sophisticated Telegram bots with JSON-based message templates, dynamic keyboards, and robust error handling.

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://img.shields.io/pypi/v/aiogram-smart-messages.svg)](https://pypi.org/project/aiogram-smart-messages/)
[![Downloads](https://img.shields.io/pypi/dm/aiogram-smart-messages.svg)](https://pypi.org/project/aiogram-smart-messages/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Aiogram](https://img.shields.io/badge/aiogram-3.x-blue.svg)](https://docs.aiogram.dev/)

## ✨ Features

- 🎯 **JSON-based message templates** - Organize messages by namespace, role, and language
- ⌨️ **Advanced keyboard builder** - Create inline and reply keyboards with WebApp support
- 🔄 **Smart message operations** - Send, edit, reply with automatic method selection
- 🌍 **Multi-language support** - Built-in localization system
- 🎨 **Context formatting** - Dynamic message content with variable substitution
- 🛡️ **Error handling** - Comprehensive logging with customizable decorators
- 📦 **Type-safe** - Full type hints for better IDE support
- ⚡ **Async-first** - Built for modern async/await patterns
- 🔌 **Middleware support** - Easy integration with Aiogram dispatcher

## 📋 Requirements

- Python 3.10+
- aiogram 3.x

## 🚀 Installation

```bash
pip install aiogram-smart-messages
```

Or install from source:

```bash
git clone https://github.com/yourusername/aiogram-smart-messages.git
cd aiogram-smart-messages
pip install -e .
```

## 📚 Quick Start

### 1. Basic Setup with Middleware (Recommended)

```python
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram_smart_messages.middleware import MessageEngineMiddleware
from aiogram_smart_messages.renderer.bot_messages import SmartMessageRenderer
from aiogram_smart_messages.logger import get_logger

# Initialize bot and dispatcher
bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher()
logger = get_logger("my_bot")

# Register middleware
dp.message.middleware(MessageEngineMiddleware(bot))
dp.callback_query.middleware(MessageEngineMiddleware(bot))

# Now msg_engine is automatically available in handlers
@dp.message(commands=["start"])
async def cmd_start(message: Message, msg_engine):
    await SmartMessageRenderer.send(
        engine=msg_engine,
        source=message,
        role="user",
        namespace="main",
        menu_file="welcome",
        block_key="greeting",
        lang="en",
        context={"username": message.from_user.first_name}
    )
```

### 2. Alternative: Manual Setup

```python
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram_smart_messages.message_engine import MessageEngine
from aiogram_smart_messages.renderer.bot_messages import SmartMessageRenderer

# Initialize bot and engine manually
bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher()
engine = MessageEngine(bot)

@dp.message(commands=["start"])
async def cmd_start(message: Message):
    await SmartMessageRenderer.send(
        engine=engine,
        source=message,
        role="user",
        namespace="main",
        menu_file="welcome",
        block_key="greeting",
        lang="en",
        context={"username": message.from_user.first_name}
    )
```

### 3. JSON Message Structure

Create message files in your project structure:
```
my_bot/
├── messages/
│   ├── user/
│   │   ├── en/
│   │   │   └── welcome.json
│   │   └── ru/
│   │       └── welcome.json
│   └── admin/
│       └── ...
```

Example `welcome.json`:
```json
{
  "greeting": {
    "text": "Hello, {username}! Welcome to our bot.",
    "buttons": [
      [
        {"type": "callback", "text": "Get Started", "data": "start"},
        {"type": "url", "text": "Help", "data": "https://example.com/help"}
      ],
      [
        {"type": "webapp", "text": "Open App", "data": "https://app.example.com"}
      ]
    ]
  },
  "main_menu": {
    "text": "Choose an option:",
    "photo": "menu_photo.jpg",
    "caption": "Main Menu",
    "buttons": [
      [
        {"type": "callback", "text": "Settings ⚙️", "data": "settings"},
        {"type": "callback", "text": "Profile 👤", "data": "profile"}
      ]
    ]
  }
}
```

### 4. Using Middleware in All Handlers

```python
from aiogram.types import CallbackQuery
from aiogram_smart_messages.decorators import with_error_logging

# Message handler with middleware
@dp.message(commands=["profile"])
async def show_profile(message: Message, msg_engine):
    user_data = await get_user_data(message.from_user.id)
    
    await SmartMessageRenderer.send(
        engine=msg_engine,
        source=message,
        role="user",
        namespace="main",
        menu_file="profile",
        block_key="view",
        lang="en",
        context={
            "username": user_data["name"],
            "balance": user_data["balance"],
            "level": user_data["level"]
        }
    )

# Callback handler with middleware
@dp.callback_query(lambda c: c.data == "settings")
async def show_settings(callback: CallbackQuery, msg_engine):
    await SmartMessageRenderer.edit(
        engine=msg_engine,
        source=callback,
        role="user",
        namespace="main",
        menu_file="settings",
        block_key="main",
        lang="en"
    )
    await callback.answer()

# Error handling with decorator
@with_error_logging(logger=logger, error_label="WELCOME_MESSAGE")
async def send_personalized_welcome(message: Message, msg_engine, user_data: dict):
    await SmartMessageRenderer.send(
        engine=msg_engine,
        source=message,
        role="user",
        namespace="main",
        menu_file="welcome",
        block_key="greeting",
        lang=user_data.get("language", "en"),
        context={
            "username": user_data["name"],
            "balance": user_data["balance"]
        }
    )
```

### 5. Advanced Usage

#### Edit Messages

```python
@dp.callback_query(lambda c: c.data == "settings")
async def show_settings(callback: CallbackQuery, msg_engine):
    await SmartMessageRenderer.edit(
        engine=msg_engine,
        source=callback,
        role="user",
        namespace="main",
        menu_file="settings",
        block_key="main",
        lang="en"
    )
    await callback.answer()
```

#### Smart Edit or Send

Automatically decides whether to edit or resend based on media content:

```python
@dp.callback_query(lambda c: c.data.startswith("view_"))
async def view_item(callback: CallbackQuery, msg_engine):
    item_id = callback.data.split("_")[1]
    
    await SmartMessageRenderer.smart_edit_or_send(
        engine=msg_engine,
        source=callback,
        role="user",
        namespace="shop",
        menu_file="catalog",
        block_key="item_details",
        lang="en",
        context={"item_id": item_id}
    )
```

#### Reply to Messages

```python
@dp.message(lambda m: m.text and "help" in m.text.lower())
async def help_reply(message: Message, msg_engine):
    await SmartMessageRenderer.reply(
        engine=msg_engine,
        source=message,
        role="user",
        namespace="main",
        menu_file="help",
        block_key="quick_help",
        lang="en"
    )
```

#### Send Documents

```python
from aiogram.types import FSInputFile

@dp.callback_query(lambda c: c.data == "download_report")
async def send_report(callback: CallbackQuery, msg_engine):
    doc = FSInputFile("reports/monthly_report.pdf")
    
    await SmartMessageRenderer.send_document(
        engine=msg_engine,
        source=callback.message.chat.id,
        document=doc,
        caption="Your monthly report"
    )
    await callback.answer("Report sent!")
```

### 6. Building Keyboards Manually

```python
from aiogram_smart_messages.builder import KeyboardBuilder

# Inline keyboard
inline_buttons = [
    [
        {"type": "callback", "text": "Option 1", "data": "opt1"},
        {"type": "callback", "text": "Option 2", "data": "opt2"}
    ],
    [
        {"type": "url", "text": "Visit Website", "data": "https://example.com"}
    ]
]
inline_kb = KeyboardBuilder.build_inline_keyboard(inline_buttons)

# Reply keyboard
reply_buttons = [
    [{"text": "Main Menu"}, {"text": "Settings"}],
    [{"type": "webapp", "text": "Open App", "data": "https://app.example.com"}]
]
reply_kb = KeyboardBuilder.build_reply_keyboard(
    reply_buttons,
    resize_keyboard=True,
    one_time_keyboard=True
)
```

### 7. Using Decorators

#### Error Logging Decorator

```python
from aiogram_smart_messages.decorators import with_error_logging

@with_error_logging(
    logger=logger,
    fallback=None,
    error_label="DATABASE_ERROR"
)
async def get_user_data(user_id: int):
    # Your database logic here
    data = await db.fetch_user(user_id)
    return data

# With re-raise for critical operations
@with_error_logging(
    logger=logger,
    reraise=True,
    error_label="CRITICAL_PAYMENT"
)
async def process_payment(amount: float):
    # Critical operation that should fail loudly
    await payment_gateway.charge(amount)
```

#### Retry Decorator

```python
from aiogram_smart_messages.decorators import with_retry

@with_retry(
    max_attempts=3,
    delay=1.0,
    backoff=2.0,
    logger=logger
)
async def fetch_external_api():
    # Will retry up to 3 times with exponential backoff
    response = await http_client.get("https://api.example.com/data")
    return response.json()
```

### 8. Logger Configuration

```python
from aiogram_smart_messages.logger import get_logger
import logging

# Basic logger
logger = get_logger("my_bot")

# Custom configuration
logger = get_logger(
    name="my_bot",
    level=logging.DEBUG,
    format_string="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Use logger
logger.info("Bot started")
logger.warning("Rate limit approaching")
logger.error("Failed to send message")
logger.debug("Processing callback: %s", callback_data)
```

### 9. Advanced Features

#### Extra Keyboard Buttons

Add dynamic buttons to existing keyboard layouts:

```python
extra_buttons = [
    {"type": "callback", "text": "🔙 Back", "data": "back"}
]

await SmartMessageRenderer.send(
    engine=msg_engine,
    source=message,
    role="user",
    namespace="main",
    menu_file="menu",
    block_key="main",
    lang="en",
    extra_kb=extra_buttons,
    extra_kb_position="bottom"  # or "top"
)
```

#### Override Block Data

Send messages without loading from JSON:

```python
custom_block = {
    "text": "Dynamic message",
    "buttons": [
        [{"type": "callback", "text": "OK", "data": "ok"}]
    ]
}

await SmartMessageRenderer.send(
    engine=msg_engine,
    source=message,
    role="user",
    override_block=custom_block
)
```

#### Custom Keyboard Markup

Use your own pre-built keyboards:

```python
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

custom_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Custom", callback_data="custom")]
])

await SmartMessageRenderer.send(
    engine=msg_engine,
    source=message,
    role="user",
    namespace="main",
    menu_file="menu",
    block_key="main",
    lang="en",
    custom_markup=custom_keyboard
)
```

## 🔌 Middleware

### MessageEngineMiddleware

The library includes a convenient middleware that automatically injects `MessageEngine` into your handlers.

```python
from aiogram_smart_messages.middleware import MessageEngineMiddleware

# Register for messages
dp.message.middleware(MessageEngineMiddleware(bot))

# Register for callback queries
dp.callback_query.middleware(MessageEngineMiddleware(bot))

# Now use msg_engine in handlers
@dp.message(commands=["start"])
async def cmd_start(message: Message, msg_engine):
    await SmartMessageRenderer.send(
        engine=msg_engine,
        source=message,
        # ... other parameters
    )
```

**Benefits:**
- ✅ No need to create `MessageEngine` manually in each handler
- ✅ Cleaner code organization
- ✅ Consistent engine instance across all handlers
- ✅ Easy to test and mock

## 🎯 Supported Button Types

### Inline Keyboards
- `callback` - Callback query button
- `url` - URL button (opens link)
- `webapp` - Web App button
- `switch_inline_query` - Inline query switch

### Reply Keyboards
- Regular text button (default)
- `webapp` - Web App button

## 📁 Project Structure Example

```
my_bot/
├── main_bot/
│   ├── messages/
│   │   ├── user/
│   │   │   ├── en/
│   │   │   │   ├── welcome.json
│   │   │   │   ├── menu.json
│   │   │   │   └── settings.json
│   │   │   └── ru/
│   │   │       └── ... (same structure)
│   │   └── admin/
│   │       └── ... (admin messages)
│   ├── photos/
│   │   ├── user/
│   │   │   ├── en/
│   │   │   │   └── menu_photo.jpg
│   │   │   └── ru/
│   │   │       └── menu_photo.jpg
│   │   └── admin/
│   │       └── ...
├── main.py
└── requirements.txt
```

## 🔧 Configuration

The library uses the following configuration structure:
- `module` - Top-level module name (default: "main_bot")
- `namespace` - Feature namespace (e.g., "main", "admin_panel", "shop")
- `role` - User role (e.g., "user", "admin", "common")
- `lang` - Language code (e.g., "en", "ru", "es")

**File paths:**
- Messages: `{module}/messages/{role}/{lang}/{menu_file}.json`
- Photos: `{module}/{namespace}/photos/{role}/{lang}/{photo_file}`

## 🐛 Error Handling

The library provides comprehensive error handling with clear labels:

```python
# Labels used in SmartMessageRenderer:
# - SEND_SMART_MESSAGE
# - EDIT_SMART_MESSAGE  
# - REPLY_SMART_MESSAGE
# - SEND_DOCUMENT
# - LOAD_JSON
# - PARSE_TO_SMART

# Custom error handling
@with_error_logging(
    logger=logger,
    fallback={"status": "error"},
    error_label="CUSTOM_OPERATION"
)
async def my_operation():
    # Your code here
    pass
```

## 📖 API Reference

### SmartMessageRenderer

Main class for message rendering operations.

#### Methods:
- `load_json()` - Load message block from JSON file
- `parse_to_smart()` - Parse JSON block to SmartMessage object
- `send()` - Send a new message
- `edit()` - Edit existing message
- `smart_edit_or_send()` - Smart decision: edit or resend
- `reply()` - Reply to a message
- `send_document()` - Send document file

### MessageEngine

Core engine for message operations.

#### Methods:
- `send_smart_message()` - Send SmartMessage
- `edit_smart_message()` - Edit SmartMessage
- `reply_smart_message()` - Reply with SmartMessage
- `send_document()` - Send document

### MessageEngineMiddleware

Middleware for automatic MessageEngine injection.

```python
class MessageEngineMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        # Initializes MessageEngine with bot instance
```

### KeyboardBuilder

Utility for building keyboards.

#### Methods:
- `build_inline_keyboard()` - Build inline keyboard
- `build_reply_keyboard()` - Build reply keyboard

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License © 2025 Kriva

## 🔗 Links

- [PyPI Package](https://pypi.org/project/aiogram-smart-messages/)
- [Aiogram Documentation](https://docs.aiogram.dev/)
- [Telegram Bot API](https://core.telegram.org/bots/api)

## 💡 Tips

1. **Use middleware** - Register `MessageEngineMiddleware` for cleaner code
2. **Organize messages by feature** - Use namespaces to separate different bot sections
3. **Use context variables** - Make messages dynamic and personalized
4. **Leverage smart_edit_or_send** - Let the library decide the best update method
5. **Add error labels** - Make debugging easier with descriptive error labels
6. **Cache static content** - Messages without context are automatically cached
7. **Use type hints** - Full type support for better IDE experience

## 🎓 Examples

Check out more examples in the `/examples` directory:
- Basic bot setup with middleware
- Multi-language support
- E-commerce bot
- Admin panel
- WebApp integration

---

Made with ❤️ for the Aiogram community