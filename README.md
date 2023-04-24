<div align="center">
  <h1> Memory-Vault</h1> 
  <em> Click on the image to try it</em> 

  [<img src="img/memory_vault_pp.png" alt="memory-vault" width=400>](http://t.me/memory_vault_bot)<br>
  <em>Whisper to future, Digital sticky notes, Learning machine</em>
</div>



Memory Vault is a Telegram bot that you can store your notes, and get reminded random notes, everyday. It is the simplest and easiest learning/remembering machine. Think of it like Digital Sticky Notes, but much more simple. Never forget your notes!

<br>


<div align="center">
<img src="img/sticky-notes.png" alt="drawing" width="300"/><br>
<em>(Just an engineer, without any design skills :D)</em>
</div>

**Use Cases**

1. Habit Building
2. Language Learning
3. Learning the way of Entrepreneurship
4. Remembering names
5. Notetaking
6. Or, Anything Custom, Memory Vault is very flexible and general solution!


<img src="img/0.mv-quickstart.png" alt="drawing" width="500"/>

<img src="img/0.mv-quickstart1.png" alt="drawing" width="500"/>


# Introduction 

[https://farukozderim.github.io/Memory-Vault/](https://farukozderim.github.io/Memory-Vault/)




# Software 


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


