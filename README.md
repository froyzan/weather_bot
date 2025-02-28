# Telegram Weather Bot
Этот проект представляет собой Telegram-бота, который предоставляет информацию о текущей погоде в любом городе, используя API OpenWeather. Бот написан на Python с использованием библиотек aiogram и aiohttp.

## 🛠️ Требования
1. Python 3.9 и выше
2. Библиотеки Python:
  - aiogram
  - aiohttp
  - aiocache
  - python-dotenv
3. API-ключи:
  - Telegram Bot Token (получить у @BotFather).
  - OpenWeather API Key (зарегистрироваться на OpenWeather и получить ключ).

## 🚀 Установка и запуск
1. Установим зависимости
```bash
pip install -r requirements.txt
```
2. Настроим переменные окружения
Создайте файл .env в корневой директории проекта и добавьте следующие строки:
```text
BOT_TOKEN=ваш_токен_бота_из_BotFather
API_KEY=ваш_ключ_OpenWeather
```
3. Запустим бота
```bash
python3 weather_bot.py
```

## 🧑‍💻 Использование
1. В Telegram найдите вашего бота по имени, указанному при создании в BotFather.
2. Отправьте команду /start, чтобы начать взаимодействие.
3. Введите название города, чтобы получить текущую погоду.
Пример ответа:
```text
Погода в городе Москва:
Температура: 5°C
Ощущается как: 3°C
Давление: 760 мм.рт.
Описание: пасмурно ☁️
Влажность: 80%
Скорость ветра: 5 м/с
```

## Создание службы
1. Создадим пользователя `weather_bot` и зададим пароль
```bash
sudo useradd -m weather_bot
sudo passwd weather_bot
```
2. Создадим службу `weather_bot.service`
<details>
  <summary>Итоговая версия `/etc/systemd/system/weather_bot.service`</summary>
```bash
[Unit]
Description=Telegram Bot
After=network.target

[Service]
Type=simple
User=weather_bot
WorkingDirectory=/opt/weather_bot
ExecStart=/opt/weather_bot/venv/bin/python3 weather_bot.py
Restart=always
RestartSec=10s
StandardOutput=append:/var/log/weather_bot.log
StandardError=append:/var/log/weather_bot.log

[Install]
WantedBy=multi-user.target
```
</details>

3. Обновляем systemd и включаем сервис:
```bash
systemctl daemon-reload
systemctl enable weather_bot
systemctl start weather_bot
```
