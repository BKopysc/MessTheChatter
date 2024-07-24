import multiprocessing
from characterai import aiocai
import asyncio
import os
from dotenv import load_dotenv
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
import nest_asyncio


load_dotenv(override=True)

nest_asyncio.apply()

async def run(users_queue: multiprocessing.Queue, bot_queue: multiprocessing.Queue):
    char = os.getenv('CAI_CHARACTER_ID')

    client = aiocai.Client(os.getenv('CAI_TOKEN'))

    me = await client.get_me()
    last_user_message = ""

    while True:
        try: 
            async with await client.connect() as chat:
                new, answer = await chat.new_chat(
                    char, me.id
                )

                print(f"@@@ CHATBOT STARTED WTIH #{answer.name} @@@")
                #print(f'{answer.name}: {answer.text}')

                if last_user_message != "":

                    message = await chat.send_message(
                        char, new.chat_id, last_user_message
                    )

                    bot_queue.put(message.text)
                
                while True:
                    if not users_queue.empty():
                        last_user_message = users_queue.get()

                        message = await chat.send_message(
                            char, new.chat_id, last_user_message
                        )

                        bot_queue.put(message.text)
                        last_user_message = ""

        except (ConnectionClosedError, ConnectionClosedOK) as e:
            print("Connection to CAI was closed. Attempting to reconnect...")
            print(f"Error: {e}")

            await asyncio.sleep(2)  # Wait for 2 seconds before reconnecting

def main(users_queue: multiprocessing.Queue, bot_queue: multiprocessing.Queue):
    asyncio.run(run(users_queue, bot_queue))