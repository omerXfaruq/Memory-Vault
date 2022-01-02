# Memory-Vault

Welcome onboard;

This bot stores your memories in the memory vault and sends random memories every day according to your decided schedule.

Keeping note of beautiful & important stuff that we come across throughout the life and remembering those memories is quite challenging. This bot solves this problem with a very simple approach, as complex methods makes it harder
to keep it them in our life. 

Sincerely thanks to my wife Seyyide for the beautiful idea.

## [Try it!](https://t.me/Memory_Vault_Bot)

## Functionalities

```
This bot will send you random memories every day from your memory vault.
- You can activate daily memory sending by writing, join or /join
- Deactivate daily sending by, leave or /leave
- Get a random memory by, send or /send
- Get multiple random memories by, send number
- Get your status information by, status or /status
- List memories by, list or /list
- Learn how to support me by, support or /support
- Delete a memory with command, delete id, you can get the memory id with the command, list or /list
Example:
delete 2
- Add memories to your memory vault with command,  add Sentence
Example:
add Time does not come back
- Give feedback about the bot with command,  feedback Sentence

- Set your timezone with command, gmt timezone. Default timezone is GMT0.
Examples:
GMT+3: gmt 3
GMT0: gmt 0
GMT-5: gmt -5

Schedule related commands:
The default scheduled hours are 8,20. You can add an hour multiple times to receive multiple memories
-Show your current schedule by, schedule or /schedule
-Reset your schedule to the default schedule by, schedule reset
-Adds hours to your schedule by, schedule add hour1 hour2 hour3
Example:
schedule add 1 3 9 11
-Removes hour from your schedule by schedule remove hour
Example:
schedule remove 8

You can use me in groups as well, just can add me to the group and make me admin.
Also you can have multiple memory vaults by using groups.
For example I would serve you well in a language learning group, where you add words to your memory vault.
```

## Requirements

- sqlite
- requirements
```
pip3 install -r requirements.txt
```

## Run With Ngrok

Run without timeout limit:

```
export NGROK_AUTH_TOKEN={TOKEN} 
export TELEGRAM_TOKEN={TOKEN} 
python3 -m src.__init__ ngrok
```

Run with timeout limit:

```
export TELEGRAM_TOKEN={TOKEN} 
python3 -m src.__init__ ngrok
```

## Run With Public IP

```
export TELEGRAM_TOKEN={TOKEN} 
python3 -m src.__init__
```


