#all imports
import json
import os
from asyncio import sleep

from dotenv import load_dotenv
from telethon import TelegramClient, events
from regex import is_valid_url, is_not_link
from demoo import scrape
from telethon.tl.types import PeerChat

load_dotenv()
# Replace these values with your own API ID, API HASH, and bot token

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

# Function to send a private message using a bot
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage())
async def main(event: events.newmessage.NewMessage.Event):
    if not event.is_private and event.text == '/start':
        await event.respond(f'''Salam, **{event.sender.first_name}** ! Zəhmət olmasa linki daxil edin.''')
    if not event.is_private and await is_valid_url(event.text):
        await event.respond("Baza yüklənir...")
        await sender(event)

async def meyar_changer(meyarr):
    global meyar
    meyar = meyarr

async def cavab_changer(value):
    global cavab
    cavab = value

async def sender(event):
    data, comments, meyar = await scrape(event.text)
    await event.respond("Baza yükləndi.")
    print(data.values())
    for key, value in data.items():
        await event.respond(key)
        await cavab_changer(value)
        if key in meyar:
            await meyar_changer(meyar[key])
        await sleep(10)
        await event.respond(value)
        if key in meyar:
            await event.respond(meyar[key])
        if key in comments:
            await event.respond(comments[key])
    await show_result(event)


async def show_result(event):
    user_data = []

    # Load JSON file
    with open("users.json", "r", encoding="utf-8") as users_file:
        user_data = json.load(users_file)

    os.remove("users.json")

    # Sort by points in descending order
    user_data.sort(key=lambda x: x['points'], reverse=True)

    # Prepare a message showing all results: username, points, and responses
    result = ""
    for user in user_data:
        result += f"Username: {user['username']}\nPoints: {user['points']}\nResponses: {', '.join(user['responses'])}\n\n"

    await event.respond(result)

@client.on(events.NewMessage())
async def check(event: events.newmessage.NewMessage.Event):
    if not event.is_private and await is_not_link(event.text):
        try:
            if event.text.lower() == cavab[7:].lower() or event.text in meyar:
                user_data = []

                if not os.path.exists("users.json"):
                    with open("users.json", "w", encoding="utf-8") as users_file:
                        json.dump(user_data, users_file, ensure_ascii=False, indent=4)

                with open("users.json", "r", encoding="utf-8") as users_file:
                    user_data = json.load(users_file)

                event_sender_username = event.sender.username  # Assuming you have the event object defined

                # Check if the response already exists in any user's responses
                response_exists_in_other_users = any(event.text in user.get('responses', []) for user in user_data)

                if not response_exists_in_other_users:
                    # Check if the user already exists in the user_data
                    existing_user = next((user for user in user_data if user['username'] == event_sender_username),
                                         None)

                    if existing_user:
                        # Check if the user has already given this response
                        if event.text not in existing_user.get('responses', []):
                            # If the response is new for this user, increment their points by 1
                            existing_user['points'] = existing_user.get('points', 0) + 1
                            existing_user.setdefault('responses', []).append(event.text)
                    else:
                        # If the user doesn't exist, add them with 1 point and the current response
                        new_user = {"username": event_sender_username, "points": 1, "responses": [event.text]}
                        user_data.append(new_user)

                    # Write the updated user_data to the JSON file
                    with open("users.json", "w", encoding="utf-8") as users_file:
                        json.dump(user_data, users_file, ensure_ascii=False, indent=4)
        except:
            pass


        # chat_id = -1001835831993
        # if event.text in data.values():




# group_entity = -1001835831993

client.run_until_disconnected()
