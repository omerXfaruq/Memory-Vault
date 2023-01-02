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


# Contents

[0. Intro](#-memory-vault)

[1. Start](#start)

[2. Use Cases](#use-cases)

[3. Tutorials](#tutorials)

[4. Software Information](#software-information)





# Start
Hello Ömer Faruk 👋🏻

Keeping note of beautiful & important stuff that we come across throughout the life, and later remembering them is quite difficult isn't it 😔? Here is the Memory Vault for the rescue! Just take your notes, and I will randomly remind them everyday 😎

Unfortunately in this era our days&agendas are very busy and it is very hard to follow something consistently. Memory Vault helps us on this front by continuously reminding our notes daily, so that we won't ever forget them. 

❤️ Sincerely thanks to my dear wife Seyyide for the beautiful idea.


You can use it for

## Use Cases
1. Habit Building 
<img src="img/ex1.png" alt="drawing" width="500"/>
2. Language Learning
<img src="img/ex2.png" alt="drawing" width="500"/>
3. Developing Enterprenurship Vision
<img src="img/ex3.png" alt="drawing" width="500"/>
4. Learning new names
<img src="img/ex4.png" alt="drawing" width="500"/>
5. Anything Custom, Memory Vault is very flexible and general solution!

## [Try it from here!](https://t.me/Memory_Vault_Bot)

## Tutorials
1. 
<img src="img/0.start.png" alt="drawing" width="500"/>

2. 

<img src="img/1.tutorials.png" alt="drawing" width="500"/>

3.

<img src="img/2.tutorials.png" alt="drawing" width="500"/>

4. 
<img src="img/3.adds.png" alt="drawing" width="500"/>

5.
<img src="img/4.delete.png" alt="drawing" width="500"/>

6.
<img src="img/5.empty-a-vault.png" alt="drawing" width="500"/>

7.
<img src="img/6.schedule.png" alt="drawing" width="500"/>

8.
<img src="img/7.help.png" alt="drawing" width="500"/>


# Software Information


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


