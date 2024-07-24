from characterai import aiocai
import asyncio
import nest_asyncio
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK

nest_asyncio.apply()

async def main():
    char = 'YntB_ZeqRq2l_aVf2gWDCZl4oBttQzDvhj9cXafWcF8' # replace with whatever characters token you want but it works as is
    client = aiocai.Client('TOKEN')

    me = await client.get_me()
    chat_history = []

    while True:
        try:
            async with await client.connect() as chat:
                new, answer = await chat.new_chat(char, me.id)
                print(f'{answer.name}: {answer.text}')
                chat_history.append((answer.name, answer.text))

                if chat_history:
                    # Summarize the chat history
                    history_text = '\n'.join([f'{name}: {text}' for name, text in chat_history])
                    summary_prompt = f"Here is the conversation so far:\n{history_text}\nPlease summarize it."

                    message = await chat.send_message(char, new.chat_id, summary_prompt)
                    print(f'{message.name}: {message.text}')

                while True:
                    text = input('YOU: ')
                    message = await chat.send_message(char, new.chat_id, text)
                    print(f'{message.name}: {message.text}')
                    chat_history.append(('YOU', text))
                    chat_history.append((message.name, message.text))

        except (ConnectionClosedError, ConnectionClosedOK) as e:
            print("Connection was closed. Attempting to reconnect...")
            print(f"Error: {e}")
            await asyncio.sleep(2)  # Wait for 2 seconds before reconnecting

await main()