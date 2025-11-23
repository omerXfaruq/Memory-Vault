
## Requirements

- Python 3.12
- sqlite
- requirements

### Setup Virtual Environment

```bash
# Create virtual environment with Python 3.12
python3.12 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

## Run With Ngrok

Run without timeout limit:

```bash
# Make sure venv is activated
source venv/bin/activate

export NGROK_AUTH_TOKEN={TOKEN} 
export TELEGRAM_TOKEN={TOKEN} 
python3 -m src.__init__ ngrok
```

Run with timeout limit:

```bash
# Make sure venv is activated
source venv/bin/activate

export TELEGRAM_TOKEN={TOKEN} 
python3 -m src.__init__ ngrok
```

## Run With Public IP

Run with self-signed ssl certificate

```bash
# Make sure venv is activated
source venv/bin/activate

export TELEGRAM_TOKEN={TOKEN} 
python3 -m src.__init__ self-signed
```

Run with authority-signed ssl certificate

```bash
# Make sure venv is activated
source venv/bin/activate

export TELEGRAM_TOKEN={TOKEN} 
python3 -m src.__init__
```
