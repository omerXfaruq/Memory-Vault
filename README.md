# Memory-Vault
Take your notes and let memory vault remind them to you.

Hello 👋🏻
Memory Vault is a telegram bot that stores your notes in the Vault and reminds random memories every day.

Keeping note of beautiful & important stuff that we come across throughout the life, and later remembering them is quite difficult isn't it 😔?
Here is the Memory Vault for the rescue! Memory Vault solves this problem with a very simple and easy to use method 😎. Because, complex methods makes it harder to keep them in our life.
Here is the catch, I will definitely send you each memory you give to me one day. And you don't need to think over when I will send it.
Sincerely thanks to my dear wife Seyyide for the beautiful idea.

## [Try it!](https://t.me/Memory_Vault_Bot)

<img src="img/memory_vault_pp.png" alt="drawing" width="200"/>

## Functionalities

```
Memory Vault will send you random memories from your memory vault, at the hours in your schedule every day.
- /help or *help* to get help message
- /join or *join* to activate daily memory sending
- /leave or *leave* to deactivate daily sending
- /send or *send* to get a random memory
- *send number* to get multiple random memories
- /status or *status* to get your status information
- /list or *list* to list memories

- *add Memory* to add a memory to your memory vault
Example:
*add Time never does come back*

- *delete id* to delete a memory. You can learn the memory ids with the command, *list* or /list
Example:
*delete 2*

- *gmt timezone* to set your timezone,  the default timezone is *GMT0*
Examples:
GMT+3: *gmt 3*
GMT0: *gmt 0*
GMT-5: *gmt -5*

- /support or *support* to learn how to support me
- *feedback Sentence* to send your thoughts and feedbacks about the bot

*Schedule related commands:*
I send memories according to the hours in your schedule. Default schedule hours are *8,20*. I will send you a memory at 8:00 and 20:00 everyday.
You can create your own daily schedule. Furthermore you can add an hour multiple times to receive multiple memories at that hour.
- /schedule or *schedule* to display your current schedule
- *schedule reset* to reset your schedule to the default schedule
- *schedule add hour1 hour2 hour3* to add hours to your schedule
Example:
*schedule add 1 3 9 11*
- *schedule remove hour* to remove an hour from your schedule
Example:
*schedule remove 8*

- You can *use me in groups* as well, just add me to a group and promote me to admin there. If you don't want to make me an admin, you can reply to my messages in the group to use my commands.
- Furthermore *you can have multiple memory vaults* by using different groups. For example I would serve you well in a *language learning group*, where you add words you want to remember to your memory vault.
- Example group: @PrayersFromQuran
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

Run with self-signed ssl certificate

```
export TELEGRAM_TOKEN={TOKEN} 
python3 -m src.__init__ self-signed
```

Run with authority-signed ssl certificate

```
export TELEGRAM_TOKEN={TOKEN} 
python3 -m src.__init__
```


