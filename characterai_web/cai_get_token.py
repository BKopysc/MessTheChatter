from characterai import aiocai, sendCode, authUser
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def main():
    email = os.getenv('CAI_EMAIL')

    code = sendCode(email)

    link = input('LINK FRON MAIL: ')

    token = authUser(link, email)

    print(f'YOUR CAI_TOKEN (copy it to .env): {token}')

asyncio.run(main())