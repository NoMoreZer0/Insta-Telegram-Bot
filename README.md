# Insta-Telegram Bot

Bot that will scan instagram account for new post and publish it to telegram channel/chat if it is not published.

## Requirements
1) Create telegram-bot via [BotFather](https://telegram.me/BotFather) and get the API key.
2) Set the api key, telegram chat id and instagram account

## Running locally

```bash
pip install --no-cache-dir -r requirements.txt
```

```bash
python main.py
```

## Running from docker

```bash
docker compose up --build -d
```
