# Memory-Vault

This project stores your memories in the memory vault and sends a random memory at each midday.

Keeping note of beautiful & important sentences that we come across throughout the life and reminding those memories to ourselves is a hard task to accomplish.
This bot solves this problem with a very simple approach, as complex methods makes it harder to keep it them in our life.

Sincerely thanks to my wife for the idea.

## Requirements
```
pip3 install -r requirements.txt
```

## Run
```
export TELEGRAM_TOKEN={TOKEN}
python3 -m src.__init__
```

## Functionalities
```
This bot will send you a random memory at every midday from your memory vault."
- You can join my system by writing, *join*
- You leave my system by writing, *leave*
- You can get a random memory by writing, *send*
- You can add memories to your memory vault with command,  *add Sentence*
*Example*:
*add Time does not come back*
- You can set your timezone with command, *gmt timezone*. Default timezone is GMT0."
*Examples*:"
GMT+3: *gmt 3*"
GMT0: *gmt 0*"
GMT-5: *gmt -5*"
```
