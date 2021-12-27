# Memory-Vault

Welcome onboard;

This bot stores your memories in the memory vault and sends a random memory every day.

Keeping note of beautiful & important stuff that we come across throughout the life and remembering those memories is quite challenging. This bot solves this problem with a very simple approach, as complex methods makes it harder
to keep it them in our life. Sincerely thanks to my wife Seyyide for the beautiful idea.

## [Try it!](https://t.me/Memory_Vault_Bot)

## Functionalities

```
This bot will send you a random memory at every day from your memory vault.
- You can join my system by writing, join
- You leave my system by writing, leave
- You can get a random memory by writing, send
- You can list memories by writing, list
- You delete a memory by writing, delete id. You can get the memory id with the command, list
Example:
delete 2
- You can add memories to your memory vault with command,  add Sentence
Example:
add Time does not come back

- You can set your timezone with command, gmt timezone. Default timezone is GMT0.
Examples:
GMT+3: gmt 3
GMT0: gmt 0
GMT-5: gmt -5

You can use me in groups as well, just can add me to the group and make me admin. Also you can have multiple memory vaults by using groups.```
```

## Requirements

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


