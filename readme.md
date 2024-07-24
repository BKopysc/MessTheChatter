# MessTheChatter </br>
[![PyPI status](https://img.shields.io/pypi/status/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)</br>
![Google Chrome](https://img.shields.io/badge/Google%20Chrome-4285F4?style=for-the-badge&logo=GoogleChrome&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)</br>
<span style="font-size:20px">CharacterAI chatbot integration with the Me$$enger app. Built with Python and Chrome Webdriver.</span>

## Features
- Send messages to a specific chat from chatbot
- Gather messages from a specific chat and resend them to chatbot
- Queue mechanism

## Results
![image](https://github.com/user-attachments/assets/d0627cf3-fcac-4394-8b62-b818eefc07e4)


## How to use
1. Create venv <br/>
```python -m venv venv```

2. Activate venv<br/>
```venv\Scripts\activate``` (Windows)<br/>
```source venv/bin/activate``` (Linux)

3. Install requirements<br/>
```pip install -r requirements.txt```

4. Manually modify .env file (check the [configuration section](##Configuration))

4. Run the main script<br/>
```python main.py```

## Configuration
To configure the script check and modify the .env file.</br>
<i>Note: your Me$$enger credentials is stored only on your local machine</i>

### Me$$enger credentials
- MESS_EMAIL - your email
- MESS_PASS - your password
- MESS_URL - URL of the me$$enger site
- MESS_CHATNAME - name of the chat you want to interact with
- MESS_SEND_MSG_TEXT - text of the send keyword in your language. Example: "Send"

### CharacterAI credentials
- CAI_CHARACTER_ID - ID of the character you want to use (you can get it from the URL on the character page)
- CAI_TOKEN - your personal authentication token (check the [token section](####How-to-obtain-the-CharacterAI-token))
- CAI_EMAIL - your email

#### How to obtain the CharacterAI token
1. Run the script</br>
```python characterai_web/cai_get_token.py``` 
2. You will receive a link in the mail from CharacterAI. Copy this URL and paste it in the console.
3. The token will appear in the console.
4. Copy the token and paste it in the .env file.

## Used libraries
- Selenium 
- [aiocai](https://github.com/kramcat/CharacterAI) (unofficial API for CharacterAI)

