
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
