# "The Official Pyromax Library (available on PyPI)".

# Pyromax 🚀

**Асинхронный, модульный и современный фреймворк для создания юзерботов в MAX Messenger.**

![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Alpha-orange)

`Pyromax` создан для тех, кто устал от "лапши" в одном файле. Мы перенесли лучшие практики из **aiogram 3.x** в мир MAX: роутеры, строгая типизация и удобная архитектура.

## 🔥 Почему Pyromax?

В отличие от других библиотек, мы ставим **Developer Experience (DX)** на первое место:

- **📦 Система Роутеров (Routers):** Разбивайте бота на файлы и плагины. Никаких файлов на 2000 строк.
- **⚡ Скорость:** Полностью асинхронное ядро на `aiohttp` и `websockets`.
- **clean_code:** Архитектура, вдохновленная `aiogram`. Если вы писали ботов для Telegram, вы будете чувствовать себя как дома.
- **🛠 Гибкость:** Встроенный Dispatcher и Observer паттерн.

---

## 📦 Установка

Библиотека поддерживает современные менеджеры пакетов, включая `uv`.

### Через pip
```bash
pip install pyromax
```


## 🚀 Быстрый старт
### Простой эхо-бот:

```python
import asyncio
import logging
import os
from pyromax.api import MaxApi
from pyromax.api.observer import Dispatcher as MaxDispatcher
from pyromax.types import Message

# Инициализация диспетчера
dp = MaxDispatcher()


# Регистрация хендлера (обрабатываем все сообщения, включая свои)
@dp.message(pattern=lambda update: True, from_me=True)
async def echo_handler(update: Message, max_api: MaxApi):
    # Отвечаем на сообщение тем же текстом и вложениями
    await update.reply(text=update.text, attaches=update.attaches)



async def main():
    logging.basicConfig(level=logging.INFO)

    # Создаем экземпляр API
    bot = await MaxApi()

    # Запускаем бота с диспетчером
    await bot.reload_if_connection_broke(dp)


if __name__ == "__main__":
    asyncio.run(main())
```

## 🧩 Модульность и Роутеры (Killer Feature)
### 1. Создайте модуль (например, handlers/admin.py)

```python
from pyromax.api import MaxApi
from pyromax.api.observer import Router
from pyromax.filters import Command, CommandStart, CommandObject
from pyromax.types import Message

# Создаем отдельный роутер
router = Router()


# Регистрируем хендлер в роутер
@router.message(Command('ping'), from_me=True)
async def ping_handler(message: Message, max_api: MaxApi):
    await message.reply("Pong! 🏓")


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(text='Ну начинаем?')
    
@router.message(Command('sum'), from_me=True)
async def sum_handler(message: Message, command: CommandObject) -> None:
    """
    В чате:
        >>>/sum 8 8
        
        >>>Ответ: 16
        
        
        >>>/sum 3 string
        
        >>>В аргументах могут быть только цифры
    """
    if command.args is None:
        return
    args = command.args.split()
    nums = []
    for arg in args:
        if not arg.isdigit():
            await message.reply(text = 'В аргументах могут быть только цифры')
            return
        nums.append(int(arg))
    await message.reply(text = f'Ответ: {sum(nums)}')


```
### 2. Подключите его в главном файле (main.py)

```python
from pyromax.api.observer import Dispatcher as MaxDispatcher
from handlers.admin import router as admin_router


dp = MaxDispatcher()

# Подключаем роутер к главному диспетчеру
dp.include_router(admin_router)
# ... далее запуск бота как в примере выше
```

### New: Теперь можно использовать форматирование текста в ответе
```python
@dp.message(Command('lyric'), from_me=True)
async def lyric(msg: Message):
    await msg.answer(text='<STRONG>They tell me, "keep it simple"</STRONG>'
                             '<QUOTE>I tell them, "take it slow"</QUOTE>'
                             '<STRIKETHROUGH>I feed a water an idea so I let it grow </STRIKETHROUGH> \n'
                             '<UNDERLINE>I tell them, "take it easy"</UNDERLINE> \n'
                             '<EMPHASIZED>They laugh and tell me, "No"</EMPHASIZED> \n'
                             '<LINK url="https://www.youtube.com/watch?v=9Zj0JOHJR-s">its cool...</LINK>'
                     )
```

### Теперь ваш код чист, структурирован и легко масштабируется!

## 🗺 Roadmap (Планы развития)

Мы активно развиваем библиотеку и стремимся сделать её стандартом для MAX.

### 📍 Текущий статус (Alpha)
- [x] **Core:** Полностью асинхронное ядро (`MaxApi`, `Dispatcher`).
- [x] **Routers:** Модульная система (разбиение бота на файлы).
- [x] **Types:** Строгая типизация всех объектов (Update, Message, Attachments).
- [x] **Observer:** Система паттернов и фильтров для хендлеров.

### 🚧 В разработке
- [ ] **FSM (Finite State Machine):** Машина состояний для создания сценариев (опросы, диалоги, формы).
- [ ] **Middlewares:** Перехват событий до хендлеров (логирование, анти-флуд, базы данных).
- [ ] **Magic Filters:** Удобный синтаксис фильтров (как `F.text.startswith("!")`).

### 🔮 Планы на будущее
- [ ] **Документация:** Полноценный сайт с документацией и примерами.
- [ ] **Плагины:** Готовые модули для администрирования чатов.

---

## 📞 Контакты
Telegram разработчика: [ТЫК](https://t.me/Nonamegodman)

## 🤝 Contributing

Мы рады любой помощи! Если вы хотите предложить фичу или исправить баг:
1. Форкните репозиторий.
2. Создайте ветку (`git checkout -b feature/NewFeature`).
3. Откройте Pull Request.

## 📄 Лицензия
MIT License. Свободно используйте в своих проектах.
