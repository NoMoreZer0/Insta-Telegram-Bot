import asyncio
import os
import time

import db

from dotenv import load_dotenv
from telegram import Bot, InputMediaPhoto, InputMediaVideo
from telegram.error import TimedOut, TelegramError

import insta

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
USERNAME = os.getenv('INSTA_USERNAME')
CHANNEL_ID = os.getenv('CHANNEL_ID')

bot = Bot(API_TOKEN)

db.create_db()

if db.count_posts() == 0:
    posts = insta.get_latest_posts(USERNAME, 3)
    for post in posts:
        db.save_post_id(post.shortcode)


async def send_photo(url, caption=None):
    async with bot:
        await bot.send_photo(chat_id=CHANNEL_ID, photo=url, caption=caption)


async def send_message(msg):
    async with bot:
        await bot.send_message(chat_id=CHANNEL_ID, text=msg)


async def send_video(video_url, caption=None):
    async with bot:
        await bot.send_video(chat_id=CHANNEL_ID, video=video_url, caption=caption)


async def send_media_group(media_group, caption=None):
    async with bot:
        await bot.send_media_group(chat_id=CHANNEL_ID, media=media_group, caption=caption)


async def send_post_to_telegram(post, is_long_caption=False):
    if db.is_post_published(post.mediaid):
        return
    try:
        if post.typename == 'GraphImage':
            if is_long_caption:
                await send_photo(post.url)
                await send_message(post.caption)
            else:
                await send_message(post.caption)
        elif post.typename == 'GraphVideo':
            if is_long_caption:
                await send_video(post.video_url)
                await send_message(post.caption)
            else:
                await send_video(post.video_url, post.caption)
        elif post.typename == 'GraphSidecar':
            media_group = [
                InputMediaPhoto(media=node.display_url) if not node.is_video else InputMediaVideo(media=node.video_url)
                for node in post.get_sidecar_nodes()
            ]
            if is_long_caption:
                await send_media_group(media_group)
                await send_message(post.caption)
            else:
                await send_media_group(media_group, post.caption)
        if not db.is_post_published(post.shortcode):
            db.save_post_id(post.shortcode)
    except TimedOut as e:
        time.sleep(20)
        print(f"Timed out: {e}. Retrying...")
        await retry(send_post_to_telegram, post)
    except TelegramError as e:
        if e.message == 'Message caption is too long':
            time.sleep(20)
            await send_post_to_telegram(post, True)
        else:
            error_message = f"ERROR: {e}\nurl: https://www.instagram.com/p/{post.shortcode}"
            print(error_message)
        if not db.is_post_published(post.shortcode):
            db.save_post_id(post.shortcode)


async def retry(func, *args, retries=3, delay=2):
    for i in range(retries):
        try:
            await func(*args)
            break
        except TimedOut as e:
            if i < retries - 1:
                await asyncio.sleep(delay * (2 ** 5))
            else:
                print(f"Failed after {retries} retries. Error: {e}")


async def main():
    posts = insta.get_latest_posts(USERNAME, 3)
    for post in posts:
        if not db.is_post_published(post.shortcode):
            await send_post_to_telegram(post)
            time.sleep(20)


async def main_loop():
    print("Started listening to instagram..")
    while True:
        try:
            await main()
            time.sleep(30)
        except asyncio.CancelledError:
            break


if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
